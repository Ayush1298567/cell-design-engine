"""End-to-end demo: spec in -> ranked buildable designs + design-space maps out.

Runs the full deterministic pipeline (intake -> strategy -> Bayesian optimization
over calculator + validated DFN -> analysis -> report). The LLM agent roles are
deterministic stubs here (no API key needed). Heavy: runs the DFN many times.
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from celltool import agents, config, orchestrator, report  # noqa: E402

t0 = time.perf_counter()

print("Running optimization pipeline...")
run = orchestrator.run()
summary = agents.report_summary(run.opt, run.spec)
print("\n" + summary + "\n")

print("Evaluating design-space grid for the landscape map...")
grid = report.evaluate_grid(
    config.load_config("configs/cell.yaml"),
    config.load_config("configs/platform.yaml"),
    run.spec,
    progress=True,
)

heatmap = report.render_heatmap(grid, run.opt, "results/design_space.png")
md = report.write_report(run, summary, heatmap, "results/run_report.md")

print(f"best design: {run.opt.best_overrides}")
print(f"verdict: {run.verdict['message']} (best score {run.verdict['best_score']:.3f})")
print(f"saved: {heatmap}")
print(f"saved: {md}")
print(f"total wall time: {time.perf_counter() - t0:.0f} s")
