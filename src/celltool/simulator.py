"""DFN simulator wrapper (the validated physics layer).

Takes a design (the same thickness/porosity knobs the calculator uses) and
returns the performance the calculator cannot predict: rate capability and
temperature rise. Built on the validated Chen2020 DFN (see
docs/validation_chen2020.md), with a lumped thermal model so high-rate self-
heating is captured.

Trust tier: directional (uncalibrated literature parameters). Used for relative
ranking of designs, not absolute promises.
"""

from dataclasses import dataclass

import pybamm

MESH = {"x_n": 32, "x_s": 32, "x_p": 32, "r_n": 32, "r_p": 32}  # converged, see convergence_dfn.py
AMBIENT_K = 298.15

# Map the calculator's design knobs onto PyBaMM parameter names.
DESIGN_TO_PYBAMM = {
    "cathode.thickness_um": ("Positive electrode thickness [m]", 1e-6),
    "cathode.porosity": ("Positive electrode porosity", 1.0),
    "anode.thickness_um": ("Negative electrode thickness [m]", 1e-6),
    "anode.porosity": ("Negative electrode porosity", 1.0),
}


@dataclass
class SimMetrics:
    rate_capability: float       # capacity at the spec rate / capacity at C/2
    temp_rise_C: float           # max temperature rise at the spec rate
    mean_voltage_V: float        # mean terminal voltage at the spec rate
    cap_ref_Ah: float            # capacity delivered at C/2 (reference)
    cap_rate_Ah: float           # capacity delivered at the spec rate
    ok: bool = True


def _base_params(design):
    params = pybamm.ParameterValues("Chen2020")
    for path, value in design.items():
        if path in DESIGN_TO_PYBAMM:
            name, scale = DESIGN_TO_PYBAMM[path]
            params[name] = value * scale
    return params


def _discharge(params, c_rate, thermal):
    options = {"thermal": "lumped"} if thermal else None
    model = pybamm.lithium_ion.DFN(options=options)
    params = params.copy()
    params["Ambient temperature [K]"] = AMBIENT_K
    params["Initial temperature [K]"] = AMBIENT_K
    experiment = pybamm.Experiment([f"Discharge at {c_rate}C until 2.5 V"])
    sim = pybamm.Simulation(model, parameter_values=params, experiment=experiment, var_pts=MESH)
    sol = sim.solve(initial_soc=1.0)
    cap = sol["Discharge capacity [A.h]"].entries[-1]
    volt = sol["Terminal voltage [V]"].entries
    if thermal:
        temp = sol["Volume-averaged cell temperature [K]"].entries
        temp_rise = float(temp.max() - AMBIENT_K)
    else:
        temp_rise = 0.0
    return cap, float(volt.mean()), temp_rise


def evaluate_design(design, spec_c_rate):
    """Run the reference and spec-rate discharges; return performance metrics.

    C-rate is defined against each design's OWN capacity (measured first at a
    near-equilibrium rate), so a thicker, higher-capacity electrode is stressed
    proportionally, not let off easy by a fixed nominal reference.
    """
    try:
        params = _base_params(design)
        # measure this design's actual capacity near equilibrium, then anchor
        # the C-rate to it so all designs are compared at the same relative stress
        q_actual, _, _ = _discharge(params, 0.05, thermal=False)
        params = params.copy()
        params["Nominal cell capacity [A.h]"] = q_actual
        cap_ref, _, _ = _discharge(params, 0.5, thermal=False)
        cap_rate, mean_v, temp_rise = _discharge(params, spec_c_rate, thermal=True)
        return SimMetrics(
            rate_capability=cap_rate / cap_ref,
            temp_rise_C=temp_rise,
            mean_voltage_V=mean_v,
            cap_ref_Ah=cap_ref,
            cap_rate_Ah=cap_rate,
            ok=True,
        )
    except pybamm.SolverError:
        # A design the solver cannot converge on is a failed evaluation, not a
        # crash. The validation layer (later) screens most of these out first.
        return SimMetrics(0.0, float("inf"), 0.0, 0.0, 0.0, ok=False)
