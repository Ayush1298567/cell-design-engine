"""Orchestrator tests: seam-output validation, the approval gate, and a smoke run."""

import pytest

from celltool import agents, config, orchestrator


def test_auto_approve_spec_passes_complete_rejects_incomplete():
    spec = config.load_config("configs/rfq.yaml")
    assert orchestrator.auto_approve_spec(spec)["approved"] is True
    assert orchestrator.auto_approve_spec({"targets": {}})["approved"] is False


def test_run_blocks_on_rejected_spec():
    # The human-in-the-loop gate: a rejecting reviewer stops the run before any
    # compute (no DFN runs), so this is fast.
    with pytest.raises(orchestrator.SpecNotApproved):
        orchestrator.run(approve=lambda spec: {"approved": False, "reason": "needs changes"})


def test_validate_strategy_clamps_inverted_budget():
    out = orchestrator._validate_strategy({"n_calls": 5, "n_initial": 20})
    assert out["n_initial"] <= out["n_calls"] == 5


def test_validate_strategy_caps_oversized_and_defaults_malformed():
    assert orchestrator._validate_strategy({"n_calls": 99999, "n_initial": 8})["n_calls"] == orchestrator.N_CALLS_CAP
    assert orchestrator._validate_strategy({"n_calls": "lots"}) == {"n_calls": 30, "n_initial": 8}


def test_validate_verdict_rejects_bad_shape():
    v = orchestrator._validate_verdict({"unexpected": 1})
    assert v["converged"] is False and "rejected" in v["message"]


def test_run_smoke(monkeypatch):
    # tiny budget for speed; assert the whole pipeline populates a RunResult
    monkeypatch.setattr(agents, "strategy", lambda spec: {"n_calls": 6, "n_initial": 3, "rationale": "test"})
    run = orchestrator.run()
    assert run.spec["spec_c_rate"] == 3.0
    assert run.approval["approved"] is True
    assert run.opt.best_overrides and run.opt.best_result is not None
    assert {"converged", "best_score", "n_evaluated", "message"}.issubset(run.verdict)
