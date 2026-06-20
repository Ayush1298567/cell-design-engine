# Custom Cell Design Engine

IBC sells custom cells, and every custom cell starts with an expensive guess. This tool makes the first guess better and cheaper.

It does not compete with the lab. It competes with the engineer's first guess: it makes the starting design better than an expert's first pass, and makes each physical build teach more, so the lab converges in fewer build-test loops.

Built by Ayush Garg and Rohan Prasad for International Battery Company (IBC).

## What it does

A customer shows up with an application in plain language (drone, 45 min flights, 80 A at takeoff, desert heat, 500 cycles, fixed volume and weight). The engine turns that into a ranked set of buildable cell designs plus a DoE build plan, searching inside IBC's three Prabal platforms and inside IBC's manufacturing envelope.

Built — the deterministic engine runs end to end (`python scripts/run_demo.py`): spec in → ranked buildable designs + design-space maps out.

- **Quote-grade calculator** — capacity, energy, mass, volume, N/P from algebra over known material properties. Lands within a percent or two of the built cell.
- **DFN physics simulation** (PyBaMM) — rate capability and a relative thermal proxy, validated against real Chen2020/LG M50 data. Directional on literature parameters; design-guidance grade once calibrated to IBC's own test data.
- **Objective + Bayesian optimization** — maximizes the tier-1 specific energy subject to rate/thermal constraints; a Gaussian-process search finds the feasible optimum in tens of simulations.
- **Orchestrator + report** — runs the pipeline and emits ranked distinct designs plus design-space heatmaps with the feasible region marked.
- **Agent seams** — intake/strategy/analysis/report are named functions with fixed contracts, currently deterministic stubs (no API key, runs free). The orchestrator validates every seam output.

Planned (post-meeting):

- **Real LLM agents** — swap each stub body for a Claude API call returning the same validated shape (needs IBC to fund the API). One file per agent; the orchestrator never changes.
- **Calibration flywheel** — real test data flows back, the model refits to IBC's cells, and design N starts from everything learned in designs 1 through N-1. This is the moat, and it only works inside IBC's walls.
- **DoE build plan** — propose the few prototypes that jointly teach the most when physically built (beyond the current distinct-design de-duplication).

## Trust tiers

Every output is labeled with the confidence of the layer that produced it:

1. **Quote-grade** — calculator algebra (±1-2%, customer-facing)
2. **Design-guidance** — calibrated DFN, reported with error bars
3. **Directional** — uncalibrated DFN and all degradation predictions (rankings and trends, never promised numbers; cycle life is always a ranking with reasoning)
4. **Ground truth** — the pilot line. Built and tested cells are the only truth.

## Status

DFN validated against real LG M50 data (`docs/validation_chen2020.md`), and the full deterministic engine is built and demoable on literature data. Numbers above the calculator tier are directional until calibrated on IBC's own cells. The demo cell, bounds, and targets are strawman/literature placeholders (config-driven) pending IBC values. `cell.yaml` density/packaging choices are flagged for review.

## Run

```
python data/download_data.py          # fetch validation data (Zenodo, MD5-checked)
python -m pytest tests/ -q            # 47 tests
python scripts/run_demo.py            # end-to-end: ranked designs + design-space maps in results/
```

## Docs

- [`docs/THE_IDEA.md`](docs/THE_IDEA.md) — the complete concept: problem, business logic, every component, technical foundations, honest limitations, open questions.
- [`docs/PROJECT_HISTORY.md`](docs/PROJECT_HISTORY.md) — internship timeline, decision log, research findings, current open items.
- [`docs/validation_chen2020.md`](docs/validation_chen2020.md) — the DFN-vs-experiment validation, with honest error decomposition.

## Stack

Python. PyBaMM (DFN simulation), scikit-optimize (Gaussian-process Bayesian optimization), NumPy/SciPy, pytest. The agent layer is currently a deterministic, contract-first scaffold — the seams are in place, but there is no LLM in the loop yet. PyBOP parameter fitting and a ChromaDB knowledge base are planned, not built (see [`docs/THE_IDEA.md`](docs/THE_IDEA.md)).

---

Confidential. IBC internship work.
