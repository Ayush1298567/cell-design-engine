# Custom Cell Design Engine

IBC sells custom cells, and every custom cell starts with an expensive guess. This tool makes the first guess better and cheaper.

It does not compete with the lab. It competes with the engineer's first guess: it makes the starting design better than an expert's first pass, and makes each physical build teach more, so the lab converges in fewer build-test loops.

Built by Ayush Garg and Rohan Prasad for International Battery Company (IBC).

## What it does

A customer shows up with an application in plain language (drone, 45 min flights, 80 A at takeoff, desert heat, 500 cycles, fixed volume and weight). The engine turns that into a ranked set of buildable cell designs plus a DoE build plan, searching inside IBC's three Prabal platforms and inside IBC's manufacturing envelope.

- **Quote-grade calculator** — capacity, energy, mass, volume, layer counts from algebra over known material properties. Lands within a percent or two of the built cell.
- **DFN physics simulation** (PyBaMM) — voltage curves, rate capability, thermal behavior. Directional on literature parameters, design-guidance grade once calibrated to IBC's own test data.
- **Bayesian optimization** (PyBOP) — picks which exact designs to simulate next; finds good designs in hundreds of sims instead of tens of thousands, works from run one.
- **Agent layer** — one LLM in narrow, bounded roles (intake, strategy, analysis, evaluation, report), consulted at checkpoints, picking from menus of legal actions. A deterministic Python orchestrator validates every answer; physics is the final filter.
- **Calibration flywheel** — real test data flows back, the model refits to IBC's cells, and design N starts from everything learned in designs 1 through N-1. This is the moat, and it only works inside IBC's walls.

## Trust tiers

Every output is labeled with the confidence of the layer that produced it:

1. **Quote-grade** — calculator algebra (±1-2%, customer-facing)
2. **Design-guidance** — calibrated DFN, reported with error bars
3. **Directional** — uncalibrated DFN and all degradation predictions (rankings and trends, never promised numbers; cycle life is always a ranking with reasoning)
4. **Ground truth** — the pilot line. Built and tested cells are the only truth.

## Status

Phase 1 (per IBC, May 2026): implement and validate PyBaMM's DFN model. The rest of the engine follows. No build started yet.

This repo currently holds the concept and project history. Code lands after the June 8 kickoff and the DFN validation scope is confirmed.

## Docs

- [`Context/THE_IDEA.md`](Context/THE_IDEA.md) — the complete concept: problem, business logic, every component, technical foundations, honest limitations, open questions.
- [`Context/PROJECT_HISTORY.md`](Context/PROJECT_HISTORY.md) — internship timeline, decision log, research findings, current open items.

## Stack

Python. PyBaMM (DFN simulation), PyBOP (Bayesian optimization and parameter fitting), ChromaDB (knowledge base / retrieval), an LLM agent layer over a deterministic orchestrator.

---

Confidential. IBC internship work.
