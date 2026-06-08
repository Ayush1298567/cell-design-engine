"""Orchestrator: the deterministic pipeline that runs the engine.

A plain state machine. It calls the agent seams for the bounded judgment calls
(intake, strategy, analysis) and the math tools (optimizer over calculator+DFN)
for everything quantitative. Deterministic Python is in charge; the agents only
choose from contracts they cannot break.

There is a human-in-the-loop gate after intake: an engineer approves the structured
spec before the autonomous run starts (see auto_approve_spec).
"""

from dataclasses import dataclass

from . import agents, config, optimizer


@dataclass
class RunResult:
    spec: dict
    approval: dict
    strategy: dict
    opt: object       # OptResult
    verdict: dict


class SpecNotApproved(Exception):
    """Raised when the spec fails the human-in-the-loop gate, so the run never starts."""


N_CALLS_CAP = 200


def auto_approve_spec(spec):
    """Default reviewer for the human-in-the-loop gate (THE_IDEA step 2).

    In a real engagement an IBC engineer reviews and approves the structured spec
    here, before the autonomous run spends any compute. This default stands in for
    that engineer: it checks the spec is complete and approves. Swap it for a real
    approval (a prompt, a UI confirmation, an LLM-assisted review) without changing
    the orchestrator.
    """
    required = {"spec_c_rate", "targets"}
    missing = required - set(spec)
    return {"approved": not missing, "reason": "spec complete" if not missing else f"missing fields: {sorted(missing)}"}


def _validate_strategy(strat):
    """Validate the strategy seam's output before obeying it (the 'rejected and
    retried, never obeyed' contract). A malformed budget falls back to a safe
    default; an inverted/oversized budget is clamped, never executed raw."""
    n_calls = strat.get("n_calls")
    n_initial = strat.get("n_initial")
    if not (isinstance(n_calls, int) and isinstance(n_initial, int)):
        return {"n_calls": 30, "n_initial": 8}
    n_calls = max(1, min(n_calls, N_CALLS_CAP))
    n_initial = max(1, min(n_initial, n_calls))
    return {"n_calls": n_calls, "n_initial": n_initial}


def _validate_verdict(verdict):
    """Ensure the analysis seam returned the expected shape; fall back if not."""
    required = {"converged", "best_score", "n_evaluated", "message"}
    if not isinstance(verdict, dict) or not required.issubset(verdict):
        return {"converged": False, "best_score": float("nan"), "n_evaluated": 0,
                "message": "analysis verdict rejected (bad shape); defaulting to continue"}
    return verdict


def run(cell_path="configs/cell.yaml", platform_path="configs/platform.yaml", rfq_path="configs/rfq.yaml",
        seed=0, approve=auto_approve_spec):
    base_cell = config.load_config(cell_path)
    platform = config.load_config(platform_path)
    rfq_raw = config.load_config(rfq_path)

    spec = agents.intake(rfq_raw)                          # seam (validated inside)

    # Human-in-the-loop gate: an engineer approves the spec before the autonomous
    # run starts. Nothing downstream runs until this passes.
    approval = approve(spec)
    if not approval.get("approved"):
        raise SpecNotApproved(approval.get("reason", "spec rejected"))

    strat = agents.strategy(spec)                          # seam
    budget = _validate_strategy(strat)                     # reject/clamp before obeying
    opt = optimizer.optimize(
        base_cell, platform, spec,
        n_calls=budget["n_calls"], n_initial=budget["n_initial"], seed=seed,
    )
    verdict = _validate_verdict(agents.analysis(opt.evaluations_by_trial))  # seam, validated
    return RunResult(spec=spec, approval=approval, strategy=strat, opt=opt, verdict=verdict)
