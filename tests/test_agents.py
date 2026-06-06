"""Agent-seam tests: each stub must honor its fixed input/output contract so an
LLM can be swapped in later without touching the orchestrator."""

import pytest

from celltool import agents, config, objective

RFQ = config.load_config("configs/rfq.yaml")


def test_intake_passes_structured_spec():
    spec = agents.intake(RFQ)
    assert spec["spec_c_rate"] == RFQ["spec_c_rate"]
    assert "targets" in spec


def test_intake_rejects_malformed_input():
    with pytest.raises(AssertionError):
        agents.intake({"nonsense": 1})


def test_strategy_returns_budget_contract():
    s = agents.strategy(RFQ)
    assert set(["n_calls", "n_initial", "rationale"]).issubset(s)
    assert s["n_calls"] >= s["n_initial"] > 0


def test_analysis_verdict_contract():
    evals = [({"x": i}, objective.ObjResult(score=float(i), feasible=True)) for i in range(10)]
    v = agents.analysis(evals)
    assert set(["converged", "best_score", "n_evaluated", "message"]).issubset(v)
    assert v["best_score"] == 9.0
    assert v["n_evaluated"] == 10


def test_report_summary_is_string_with_numbers():
    class _Opt:
        best_result = objective.ObjResult(score=1.0, feasible=True, metrics={
            "specific_energy_Wh_kg": 265, "capacity_Ah": 26.8, "rate_capability": 0.7, "temp_rise_C": 30})
        evaluations = [1, 2, 3]
        n_feasible = 2
    text = agents.report_summary(_Opt(), RFQ)
    assert "265" in text and "Wh/kg" in text
