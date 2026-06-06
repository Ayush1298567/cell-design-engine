"""Orchestrator: the deterministic pipeline that runs the engine.

A plain state machine. It calls the agent seams for the bounded judgment calls
(intake, strategy, analysis) and the math tools (optimizer over calculator+DFN)
for everything quantitative. Deterministic Python is in charge; the agents only
choose from contracts they cannot break.
"""

from dataclasses import dataclass

from . import agents, config, optimizer


@dataclass
class RunResult:
    spec: dict
    strategy: dict
    opt: object       # OptResult
    verdict: dict


def run(cell_path="configs/cell.yaml", platform_path="configs/platform.yaml", rfq_path="configs/rfq.yaml", seed=0):
    base_cell = config.load_config(cell_path)
    platform = config.load_config(platform_path)
    rfq_raw = config.load_config(rfq_path)

    spec = agents.intake(rfq_raw)                       # seam
    strat = agents.strategy(spec)                       # seam
    opt = optimizer.optimize(
        base_cell, platform, spec,
        n_calls=strat["n_calls"], n_initial=strat["n_initial"], seed=seed,
    )
    verdict = agents.analysis(opt.evaluations)          # seam
    return RunResult(spec=spec, strategy=strat, opt=opt, verdict=verdict)
