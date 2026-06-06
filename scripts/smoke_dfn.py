"""Environment smoke test: one stock DFN discharge on the Chen2020 cell.

Proves PyBaMM, the DFN model, and the solver run end to end and produce a
physically sensible discharge curve. Not validation (rule 6) -- just proof the
machinery works. Saves the voltage curve to results/smoke_dfn_1C.png.
"""

import os
import sys
import time

import matplotlib

matplotlib.use("Agg")  # render to file, no display needed
import matplotlib.pyplot as plt

import pybamm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from celltool import constants  # noqa: E402

model = pybamm.lithium_ion.DFN()
params = pybamm.ParameterValues("Chen2020")

experiment = pybamm.Experiment([f"Discharge at 1C until {constants.DISCHARGE_CUTOFF_V} V"])
# Same converged mesh the engine ships with, so the proof artifact matches production.
sim = pybamm.Simulation(model, parameter_values=params, experiment=experiment, var_pts=constants.CONVERGED_MESH)

t0 = time.perf_counter()
solution = sim.solve()
solve_seconds = time.perf_counter() - t0

discharge_capacity = solution["Discharge capacity [A.h]"].entries
voltage = solution["Terminal voltage [V]"].entries
nominal_capacity = params["Nominal cell capacity [A.h]"]

print(f"model:               {model.name}")
print(f"parameter set:       Chen2020")
print(f"nominal capacity:    {nominal_capacity:.3f} Ah")
print(f"delivered capacity:  {discharge_capacity[-1]:.3f} Ah")
print(f"start voltage:       {voltage[0]:.3f} V")
print(f"end voltage:         {voltage[-1]:.3f} V")
print(f"solve time:          {solve_seconds:.3f} s")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(discharge_capacity, voltage, color="#ff5a69", linewidth=2)
ax.set_xlabel("Discharge capacity [Ah]")
ax.set_ylabel("Terminal voltage [V]")
ax.set_title("DFN 1C discharge, Chen2020 (environment smoke test)")
ax.grid(True, alpha=0.3)
fig.tight_layout()

out = "results/smoke_dfn_1C.png"
import os

os.makedirs("results", exist_ok=True)
fig.savefig(out, dpi=130)
print(f"saved:               {out}")
