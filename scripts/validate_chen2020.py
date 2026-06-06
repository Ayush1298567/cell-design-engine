"""Validation: PyBaMM DFN vs Chen2020 experimental discharge data.

Compares the uncalibrated DFN (Chen2020 parameters, isothermal 25 C, converged
mesh) against the real LG M50 discharge curves from Zenodo 4032561, at C/10, C/2,
1C, and 1.5C. Reports, per rate:
  - capacity error (%)
  - start-voltage error (mV)  [NOT a clean IR: carries the OCV/SOC offset]
  - shape bias/scatter on normalized DoD  AND on the raw-capacity axis
  - the experimental cell temperature excursion (the high-rate confound)

Trust tier: directional (uncalibrated literature parameters). It checks PyBaMM's
DFN machinery, not IBC cells.
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pybamm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from celltool import constants  # noqa: E402

DATA = "data/LGM50_cell02.csv"
RATES = [("C/10", 0.5), ("C/2", 2.5), ("1C", 5.0), ("1.5C", 7.5)]


def load_discharge(csv_path, current_A, tol=0.1):
    """One from-full constant-current discharge: capacity [Ah], voltage, cell temp."""
    df = pd.read_csv(csv_path, skiprows=13)
    disch = df[df["Md"] == "D"]
    for step, d in disch.groupby("Step"):
        if abs(d["Current [A]"].mean() - current_A) < tol and d["Voltage [V]"].iloc[0] > 3.5:
            t = d["Step Time [s]"].to_numpy()
            i = d["Current [A]"].to_numpy()
            v = d["Voltage [V]"].to_numpy()
            temp = d["Temperature Cell [degC]"].to_numpy()
            cap = np.concatenate([[0.0], np.cumsum(np.diff(t) * (i[:-1] + i[1:]) / 2)]) / 3600.0
            return cap, v, temp
    raise ValueError(f"no from-full discharge near {current_A} A in {csv_path}")


def simulate_discharge(current_A):
    """Isothermal DFN discharge from a full (100% SOC) charge at constant current."""
    model = pybamm.lithium_ion.DFN()
    params = pybamm.ParameterValues("Chen2020")
    experiment = pybamm.Experiment([f"Discharge at {current_A} A until {constants.DISCHARGE_CUTOFF_V} V"])
    sim = pybamm.Simulation(model, parameter_values=params, experiment=experiment, var_pts=constants.CONVERGED_MESH)
    sol = sim.solve(initial_soc=1.0)
    return sol["Discharge capacity [A.h]"].entries, sol["Terminal voltage [V]"].entries


def bias_scatter(grid, x_sim, v_sim, x_exp, v_exp):
    diff_mV = (np.interp(grid, x_sim, v_sim) - np.interp(grid, x_exp, v_exp)) * 1000.0
    return np.mean(diff_mV), np.std(diff_mV)


fig, axes = plt.subplots(2, 2, figsize=(12, 9))
hdr = f"{'rate':>5} {'cap%':>6} {'startV':>7} {'bias_dod':>9} {'scat_dod':>9} {'bias_raw':>9} {'scat_raw':>9} {'Tmean':>6} {'Trise':>6}"
print(hdr)
for ax, (label, amps) in zip(axes.flat, RATES):
    cap_exp, v_exp, temp_exp = load_discharge(DATA, amps)
    cap_sim, v_sim = simulate_discharge(amps)

    cap_err = 100.0 * (cap_sim[-1] - cap_exp[-1]) / cap_exp[-1]
    startv_err = 1000.0 * (v_sim[0] - v_exp[0])  # NOT clean IR: see doc

    # DoD-normalized (endpoints forced to coincide -> removes the capacity offset)
    grid = np.linspace(0.0, 0.97, 400)
    bias_dod, scat_dod = bias_scatter(grid, cap_sim / cap_sim[-1], v_sim, cap_exp / cap_exp[-1], v_exp)
    # raw-capacity axis (honest residual, keeps the capacity offset in)
    grid_raw = np.linspace(0.0, 0.97 * min(cap_sim[-1], cap_exp[-1]), 400)
    bias_raw, scat_raw = bias_scatter(grid_raw, cap_sim, v_sim, cap_exp, v_exp)

    t_mean = temp_exp.mean()
    t_rise = temp_exp.max() - temp_exp[0]
    print(f"{label:>5} {cap_err:>+6.1f} {startv_err:>+7.0f} {bias_dod:>+9.0f} {scat_dod:>9.1f} "
          f"{bias_raw:>+9.0f} {scat_raw:>9.1f} {t_mean:>6.1f} {t_rise:>6.1f}")

    ax.plot(cap_exp, v_exp, color="#1f77b4", linewidth=2.2, label="experiment")
    ax.plot(cap_sim, v_sim, color="#ff5a69", linewidth=1.8, linestyle="--", label="DFN (sim)")
    ax.set_title(f"{label}: cap {cap_err:+.1f}%, raw scatter {scat_raw:.0f} mV, cell +{t_rise:.0f}C")
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
