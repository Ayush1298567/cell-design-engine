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


def _evals(scores):
    return [({"x": i}, objective.ObjResult(score=float(s), feasible=True)) for i, s in enumerate(scores)]


def test_analysis_verdict_contract_and_improving_not_converged():
    v = agents.analysis(_evals(range(12)))  # strictly rising
    assert set(["converged", "best_score", "n_evaluated", "message"]).issubset(v)
    assert v["best_score"] == 11.0
    assert v["n_evaluated"] == 12
    assert v["converged"] is False


def test_analysis_detects_plateau():
    # best (5) is reached before the last plateau_window trials, then flat
    v = agents.analysis(_evals(list(range(6)) + [5.0] * 8), plateau_window=8)
    assert v["converged"] is True


def test_analysis_short_history_not_converged():
    v = agents.analysis(_evals([0, 1, 2]))
    assert v["converged"] is False


def test_report_summary_is_string_with_numbers():
    class _Opt:
        best_result = objective.ObjResult(score=1.0, feasible=True, metrics={
            "specific_energy_Wh_kg": 265, "capacity_Ah": 26.8, "rate_capability": 0.7, "temp_rise_C": 30})
        evaluations = [1, 2, 3]
        n_feasible = 2
    text = agents.report_summary(_Opt(), RFQ)
    assert "265" in text and "Wh/kg" in text
