"""Validation: PyBaMM DFN vs Chen2020 experimental discharge data.

Compares the DFN (Chen2020 parameters, isothermal 25 C, 32-pt converged mesh)
against the real LG M50 discharge curves from Zenodo 4032561, at C/10, C/2, 1C,
and 1.5C. Reports RMSE and max error in mV per rate, and overlays each curve.

Isothermal baseline (rule 6): this quantifies where the literature-parameter
model is strong (low rate) and weak (high rate, end of discharge). It is a
directional/design-guidance check on PyBaMM's own machinery, not a claim about
IBC cells.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pybamm

DATA = "data/LGM50_cell02.csv"
MESH = {"x_n": 32, "x_s": 32, "x_p": 32, "r_n": 32, "r_p": 32}
# (label, discharge current [A]) for the from-full characterization discharges
RATES = [("C/10", 0.5), ("C/2", 2.5), ("1C", 5.0), ("1.5C", 7.5)]


def load_discharge(csv_path, current_A, tol=0.1):
    """Extract one from-full constant-current discharge segment.

    Picks the discharge step (Md == 'D') whose mean current matches current_A
    and that starts above 3.5 V (excludes the preconditioning discharge).
    Returns discharged capacity [Ah] (integrated from step start) and voltage.
    """
    df = pd.read_csv(csv_path, skiprows=13)
    disch = df[df["Md"] == "D"]
    for step, d in disch.groupby("Step"):
        if abs(d["Current [A]"].mean() - current_A) < tol and d["Voltage [V]"].iloc[0] > 3.5:
            t = d["Step Time [s]"].to_numpy()
            i = d["Current [A]"].to_numpy()
            v = d["Voltage [V]"].to_numpy()
            # discharged capacity in Ah = integral of current over time
            cap = np.concatenate([[0.0], np.cumsum(np.diff(t) * (i[:-1] + i[1:]) / 2)]) / 3600.0
            return cap, v
    raise ValueError(f"no from-full discharge near {current_A} A in {csv_path}")


def simulate_discharge(current_A):
    """Isothermal DFN discharge from a full (100% SOC) charge at constant current."""
    model = pybamm.lithium_ion.DFN()
    params = pybamm.ParameterValues("Chen2020")
    experiment = pybamm.Experiment([f"Discharge at {current_A} A until 2.5 V"])
    sim = pybamm.Simulation(model, parameter_values=params, experiment=experiment, var_pts=MESH)
    sol = sim.solve(initial_soc=1.0)
    cap = sol["Discharge capacity [A.h]"].entries
    volt = sol["Terminal voltage [V]"].entries
    return cap, volt


fig, axes = plt.subplots(2, 2, figsize=(12, 9))
print(f"{'rate':>6} {'cap_err[%]':>11} {'IR_err[mV]':>11} {'bias[mV]':>10} {'scatter[mV]':>12}")
results = []
for ax, (label, amps) in zip(axes.flat, RATES):
    cap_exp, v_exp = load_discharge(DATA, amps)
    cap_sim, v_sim = simulate_discharge(amps)

    # 1) capacity error: total delivered Ah, sim vs experiment
    cap_err = 100.0 * (cap_sim[-1] - cap_exp[-1]) / cap_exp[-1]
    # 2) IR / start-voltage error: agreement of the initial overpotential
    ir_err = 1000.0 * (v_sim[0] - v_exp[0])
    # 3) shape error on normalized depth-of-discharge (capacity offset and the
    #    near-vertical knee removed). Split into bias (mean signed offset, which
    #    calibration removes) and scatter (std about the mean, the irreducible
    #    shape error of the uncalibrated model).
    dod_exp = cap_exp / cap_exp[-1]
    dod_sim = cap_sim / cap_sim[-1]
    grid = np.linspace(0.0, 0.97, 400)  # 0-97% DoD, excludes the cutoff knee
    diff_mV = (np.interp(grid, dod_sim, v_sim) - np.interp(grid, dod_exp, v_exp)) * 1000.0
    bias = np.mean(diff_mV)
    scatter = np.std(diff_mV)
    results.append((label, cap_err, ir_err, bias, scatter))
    print(f"{label:>6} {cap_err:>+10.2f} {ir_err:>+10.0f} {bias:>+9.0f} {scatter:>12.1f}")

    ax.plot(cap_exp, v_exp, color="#1f77b4", linewidth=2.2, label="experiment")
    ax.plot(cap_sim, v_sim, color="#ff5a69", linewidth=1.8, linestyle="--", label="DFN (sim)")
    ax.set_title(f"{label}: cap {cap_err:+.1f}%, IR {ir_err:+.0f} mV, bias {bias:+.0f} / scatter {scatter:.0f} mV")
    ax.set_xlabel("Discharge capacity [Ah]")
    ax.set_ylabel("Terminal voltage [V]")
    ax.legend()
    ax.grid(True, alpha=0.3)

fig.suptitle("DFN vs Chen2020 experiment (LG M50, uncalibrated, isothermal 25 C)", fontsize=14)
fig.tight_layout()
os.makedirs("results", exist_ok=True)
out = "results/validate_chen2020.png"
fig.savefig(out, dpi=130)
print(f"\nsaved: {out}")
