"""DFN simulator wrapper (the validated physics layer, tier-3 directional).

Contract: this layer returns RELATIVE, geometry-independent metrics only --
rate capability (a ratio) and a temperature rise measured at a fixed depth of
discharge. It does NOT report the cell's absolute capacity or energy; those come
from the calculator (tier-1). Rate capability is governed by electrode
microstructure (thickness, porosity, areal current density), which is scale-
independent, so it is valid for the calculator's full cell even though the DFN
runs a single Chen2020 stack. Built on the validated Chen2020 DFN (see
docs/validation_chen2020.md).

Takes an already-realized cell (anode co-balanced via calculator.realize_design).
The DFN runs Chen2020 electrochemistry on the design's GEOMETRY (thickness,
porosity); it shares the geometry with the calculator but NOT the exact
electrochemistry. The DFN's own electrode balance is set by Chen2020 stoichiometry,
so its internal N/P is not the calculator's quoted 1.10 -- which is fine because
this layer only outputs a relative rate ranking, not absolute capacity or N/P.

temp_rise_C is a relative self-heating proxy: it runs on Chen2020's single-stack
cooling geometry, so its absolute value is not the configured pouch's temperature.
All designs share the same cooling, so it ranks designs correctly; a calibrated
absolute cell temperature needs a pack/cell thermal model (future work).
"""

from dataclasses import dataclass

import numpy as np
import pybamm

from . import constants

# Temperature is read at this fraction of the C/2 reference capacity, so a design
# that hits cutoff early (low rate capability) cannot masquerade as "cool". Set
# below typical feasible rate-capability so feasible designs all reach it.
TEMP_CHECKPOINT_FRACTION = 0.40
# A spec-rate discharge delivering less than this fraction of the reference is a
# failed (non-viable) evaluation, not a valid low-performance design.
MIN_USABLE_FRACTION = 0.05


@dataclass
class SimMetrics:
    rate_capability: float       # capacity at spec rate / capacity at C/2 (dimensionless)
    temp_rise_C: float           # rise at a fixed DoD checkpoint (relative/directional)
    mean_voltage_V: float        # capacity-weighted mean discharge voltage at spec rate
    reached_checkpoint: bool     # whether the thermal checkpoint DoD was reached
    ok: bool = True
    error: str = ""


def _base_params(cell):
    """Chen2020 parameters with the realized cell's electrode design applied.

    Porosity is coupled to the active-material volume fraction so the solid+void
    budget stays at 1 (active = (1 - porosity) * solid_active_ratio); overriding
    porosity alone would otherwise leave a physically impossible electrode.
    """
    params = pybamm.ParameterValues("Chen2020")
    ratio_pos = params["Positive electrode active material volume fraction"] / (1 - params["Positive electrode porosity"])
    ratio_neg = params["Negative electrode active material volume fraction"] / (1 - params["Negative electrode porosity"])

    cath, anode = cell["cathode"], cell["anode"]
    params["Positive electrode thickness [m]"] = cath["thickness_um"] * 1e-6
    params["Positive electrode porosity"] = cath["porosity"]
    params["Positive electrode active material volume fraction"] = (1 - cath["porosity"]) * ratio_pos
    params["Negative electrode thickness [m]"] = anode["thickness_um"] * 1e-6
    params["Negative electrode porosity"] = anode["porosity"]
    params["Negative electrode active material volume fraction"] = (1 - anode["porosity"]) * ratio_neg

    params["Ambient temperature [K]"] = constants.AMBIENT_K
    params["Initial temperature [K]"] = constants.AMBIENT_K
    return params


def _discharge(params, c_rate, thermal):
    """One constant-current discharge from full charge. Returns arrays."""
    options = {"thermal": "lumped"} if thermal else None
    model = pybamm.lithium_ion.DFN(options=options)
    experiment = pybamm.Experiment([f"Discharge at {c_rate}C until {constants.DISCHARGE_CUTOFF_V} V"])
    sim = pybamm.Simulation(model, parameter_values=params, experiment=experiment, var_pts=constants.CONVERGED_MESH)
    sol = sim.solve(initial_soc=1.0)
    cap = sol["Discharge capacity [A.h]"].entries
    if cap.size == 0:
        raise RuntimeError("empty solution")
    volt = sol["Terminal voltage [V]"].entries
    temp = sol["Volume-averaged cell temperature [K]"].entries if thermal else None
    return cap, volt, temp


def evaluate_design(cell, spec_c_rate):
    """Return relative performance metrics for an already-realized cell.

    Any single design that the solver cannot handle degrades to ok=False rather
    than crashing the optimizer (THE_IDEA step 9: a failure costs a retry, never
    the run).
    """
    try:
        params = _base_params(cell)
        # Anchor the C-rate to this design's own near-equilibrium capacity so all
        # designs are stressed at the same relative rate.
        q_actual, _, _ = _discharge(params, 0.05, thermal=False)
        params = params.copy()
        params["Nominal cell capacity [A.h]"] = q_actual[-1]

        cap_ref, _, _ = _discharge(params, 0.5, thermal=False)
        cap_s, volt_s, temp_s = _discharge(params, spec_c_rate, thermal=True)
        cap_ref = cap_ref[-1]
        cap_rate = cap_s[-1]

        if cap_ref <= 0 or cap_rate / cap_ref < MIN_USABLE_FRACTION:
            return SimMetrics(0.0, float("inf"), 0.0, False, ok=False, error="non_viable")

        rate_capability = cap_rate / cap_ref
        mean_v = float(np.trapezoid(volt_s, cap_s) / (cap_s[-1] - cap_s[0]))

        # Temperature at a fixed DoD, not the cutoff-truncated peak. If the design
        # dies before the checkpoint (poor rate), its peak temp is not comparable to
        # designs measured at the checkpoint, so report it as inf (non-comparable)
        # rather than a misleadingly-low truncated value. Such designs already fail
        # the rate constraint, so this only hardens the infeasible region.
        checkpoint = TEMP_CHECKPOINT_FRACTION * cap_ref
        if cap_s[-1] >= checkpoint:
            temp_rise = float(np.interp(checkpoint, cap_s, temp_s)) - constants.AMBIENT_K
            reached = True
        else:
            temp_rise = float("inf")
            reached = False

        return SimMetrics(rate_capability, temp_rise, mean_v, reached, ok=True)
    except Exception as e:
        # Broad by design: any solver/model/arithmetic failure on one candidate
        # must not kill a batch. Type is recorded for a future fixer agent.
        return SimMetrics(0.0, float("inf"), 0.0, False, ok=False, error=type(e).__name__)
