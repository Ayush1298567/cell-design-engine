"""Export real engine data for the slide-deck animation: the optimizer's
trial-by-trial search path, the design-space grid, the recommended design, and a
second application (power tool). Writes results/demo_data.json.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from celltool import config, orchestrator, report  # noqa: E402

CELL = config.load_config("configs/cell.yaml")
PLATFORM = config.load_config("configs/platform.yaml")


def _f(x):
    return None if x is None or (isinstance(x, float) and not math.isfinite(x)) else float(x)


def row(ov, r):
    m = r.metrics
    return {"thickness": _f(ov["cathode.thickness_um"]), "porosity": _f(ov["cathode.porosity"]),
            "feasible": bool(r.feasible), "specific_energy": _f(m.get("specific_energy_Wh_kg")),
            "capacity": _f(m.get("capacity_Ah")), "energy_density": _f(m.get("energy_density_Wh_L")),
            "rate": _f(m.get("rate_capability")), "temp": _f(m.get("temp_rise_C"))}


print("drone run...")
drone = orchestrator.run(rfq_path="configs/rfq.yaml", seed=0)
print("grid...")
grid = report.evaluate_grid(CELL, PLATFORM, drone.spec, n_thk=13, n_por=11, progress=True)
print("power run...")
power = orchestrator.run(rfq_path="configs/rfq_power.yaml", seed=0)

data = {
    "spec": {"spec_c_rate": drone.spec["spec_c_rate"], "targets": drone.spec["targets"]},
    "grid": {"thks": [float(x) for x in grid["thks"]], "pors": [float(x) for x in grid["pors"]],
             "energy": [[_f(v) for v in r] for r in grid["specific_energy"].tolist()],
             "feasible": [[int(bool(v)) for v in r] for r in grid["feasible"].tolist()]},
    "trajectory": [row(ov, r) for ov, r in drone.opt.evaluations_by_trial],
    "best": row(drone.opt.best_overrides, drone.opt.best_result),
    "ranked": [row(ov, r) for ov, r in report.distinct_designs(drone.opt.evaluations, k=5)],
    "n_feasible": drone.opt.n_feasible, "n_total": len(drone.opt.evaluations),
    "power": {"spec_c_rate": power.spec["spec_c_rate"], "best": row(power.opt.best_overrides, power.opt.best_result)},
    "bounds": {"thk": [PLATFORM["design_variables"]["cathode.thickness_um"]["min"], PLATFORM["design_variables"]["cathode.thickness_um"]["max"]],
               "por": [PLATFORM["design_variables"]["cathode.porosity"]["min"], PLATFORM["design_variables"]["cathode.porosity"]["max"]]},
}
os.makedirs("results", exist_ok=True)
with open("results/demo_data.json", "w") as f:
    json.dump(data, f, indent=2)
print(f"wrote results/demo_data.json: {len(data['trajectory'])} trials")
