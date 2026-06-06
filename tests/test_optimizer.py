"""Optimizer tests with an injected analytic objective (fast, no DFN).

A synthetic score peaks at a known design; the optimizer must get close, proving
the Bayesian search drives toward the optimum and the bookkeeping is correct.
"""

from celltool import config, objective, optimizer

PLATFORM = config.load_config("configs/platform.yaml")
RFQ = config.load_config("configs/rfq.yaml")
CELL = config.load_config("configs/cell.yaml")

# Analytic optimum at thickness 70 um, porosity 0.30.
TARGET_THK, TARGET_POR = 70.0, 0.30


def _fake_eval(cell, rfq):
    thk = cell["cathode"]["thickness_um"]
    por = cell["cathode"]["porosity"]
    score = -((thk - TARGET_THK) / 30) ** 2 - ((por - TARGET_POR) / 0.2) ** 2
    return objective.ObjResult(score=score, feasible=score > -0.05, metrics={}, violations={})


def test_optimizer_converges_to_known_optimum():
    res = optimizer.optimize(CELL, PLATFORM, RFQ, n_calls=30, n_initial=10, seed=0, eval_fn=_fake_eval)
    assert abs(res.best_overrides["cathode.thickness_um"] - TARGET_THK) < 6
    assert abs(res.best_overrides["cathode.porosity"] - TARGET_POR) < 0.05


def test_history_and_ranking_recorded():
    res = optimizer.optimize(CELL, PLATFORM, RFQ, n_calls=15, n_initial=6, seed=1, eval_fn=_fake_eval)
    assert len(res.evaluations) == 15
    assert len(res.evaluations_by_trial) == 15
    # evaluations sorted feasibility-first, then by score
    keys = [(r.feasible, r.score) for _, r in res.evaluations]
    assert keys == sorted(keys, reverse=True)


def test_budget_clamped_not_raised():
    # inverted budget must be clamped, not crash skopt
    res = optimizer.optimize(CELL, PLATFORM, RFQ, n_calls=5, n_initial=20, seed=0, eval_fn=_fake_eval)
    assert len(res.evaluations) == 5


def test_optimizer_returns_feasible_on_real_objective():
    # Slow (~12 DFN-backed evals): the RFQ feasible region is non-empty, so the
    # winner must be feasible, and its energy must beat the min target.
    res = optimizer.optimize(CELL, PLATFORM, RFQ, n_calls=12, n_initial=6, seed=0)
    assert res.best_result.feasible
    assert res.best_result.metrics["specific_energy_Wh_kg"] >= RFQ["targets"]["min_specific_energy_Wh_kg"]
