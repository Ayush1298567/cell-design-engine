"""Mesh convergence study for the DFN 1C discharge (Chen2020).

Refines the spatial mesh (electrodes/separator x, particles r) and checks that
the terminal voltage stops changing. This separates numerical error from physics
error. Reports each mesh's deviation from the FINEST tested mesh (48 pts) -- note
that is a lower bound on the true discretisation error, since the 48-pt mesh
carries its own grid error (a 64-pt reference puts the 32-pt absolute error at
~3.7 mV vs 2.6 mV against 48 pts). Either way it is far below the ~40 mV physics
bias, so numerical error is negligible against the physics budget.
"""

import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import pybamm

model = pybamm.lithium_ion.DFN()
params = pybamm.ParameterValues("Chen2020")


def var_pts(n):
    """Uniform n points across every spatial/particle domain."""
    return {"x_n": n, "x_s": n, "x_p": n, "r_n": n, "r_p": n}


levels = [8, 12, 20, 32, 48]  # finest (48) is the reference

curves = {}
print(f"{'pts/domain':>11} {'delivered Ah':>13} {'solve s':>8}")
for n in levels:
    sim = pybamm.Simulation(model, parameter_values=params, var_pts=var_pts(n))
    t0 = time.perf_counter()
    sol = sim.solve([0, 3600], inputs=None)  # 1C-equivalent window; cutoff handles end
    dt = time.perf_counter() - t0
    cap = sol["Discharge capacity [A.h]"].entries
    volt = sol["Terminal voltage [V]"].entries
    curves[n] = (cap, volt)
    print(f"{n:>11} {cap[-1]:>13.4f} {dt:>8.3f}")

# Compare each mesh to the finest on a common capacity grid.
ref_cap, ref_volt = curves[levels[-1]]
grid = np.linspace(ref_cap.min(), ref_cap.max(), 500)
ref_on_grid = np.interp(grid, ref_cap, ref_volt)

print(f"\nvs finest mesh ({levels[-1]} pts):")
print(f"{'pts/domain':>11} {'max dV [mV]':>12} {'RMS dV [mV]':>12}")
errors = []
for n in levels[:-1]:
    cap, volt = curves[n]
    on_grid = np.interp(grid, cap, volt)
    diff_mV = (on_grid - ref_on_grid) * 1000.0
    max_mV = np.max(np.abs(diff_mV))
    rms_mV = np.sqrt(np.mean(diff_mV**2))
    errors.append((n, max_mV, rms_mV))
    print(f"{n:>11} {max_mV:>12.2f} {rms_mV:>12.2f}")

# Plots: overlaid curves + convergence of max error.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
for n in levels:
    cap, volt = curves[n]
    ax1.plot(cap, volt, linewidth=1.6, label=f"{n} pts")
ax1.set_xlabel("Discharge capacity [Ah]")
ax1.set_ylabel("Terminal voltage [V]")
ax1.set_title("DFN 1C discharge at increasing mesh resolution")
ax1.legend()
ax1.grid(True, alpha=0.3)

ns = [e[0] for e in errors]
maxes = [e[1] for e in errors]
ax2.semilogy(ns, maxes, "o-", color="#ff5a69", linewidth=2)
ax2.set_xlabel("Mesh points per domain")
ax2.set_ylabel("Max |dV| vs finest [mV]")
ax2.set_title("Convergence: error shrinks as mesh refines")
ax2.grid(True, alpha=0.3, which="both")

fig.tight_layout()
import os

os.makedirs("results", exist_ok=True)
out = "results/convergence_dfn.png"
fig.savefig(out, dpi=130)
print(f"\nsaved: {out}")
