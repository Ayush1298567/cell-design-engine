"""Objective tests. Scoring logic is tested with synthetic metrics (fast); one
integration test runs the real engine."""

from celltool import calculator, config, objective

RFQ = config.load_config("configs/rfq.yaml")
CELL = config.load_config("configs/cell.yaml")


def test_feasible_design_scores_positive_no_penalty():
    # beats every target -> feasible, score == pure desirability (no penalty)
    r = objective.score_from_metrics(270, 0.90, 25, True, RFQ)
    assert r.feasible
    assert not r.violations
    assert r.score > 0


def test_low_energy_is_infeasible_with_violation():
    r = objective.score_from_metrics(210, 0.90, 25, True, RFQ)  # below 240 target
    assert not r.feasible
    assert "specific_energy" in r.violations


def test_non_viable_sim_scored_floor():
    r = objective.score_from_metrics(0.0, 0.0, float("inf"), False, RFQ)
    assert r.score == objective.NON_VIABLE_SCORE
    assert not r.feasible


def test_more_energy_scores_higher_all_else_equal():
    lo = objective.score_from_metrics(250, 0.90, 25, True, RFQ)
    hi = objective.score_from_metrics(290, 0.90, 25, True, RFQ)
    assert hi.score > lo.score


def test_infeasible_scores_below_feasible():
    feasible = objective.score_from_metrics(270, 0.90, 25, True, RFQ)
    infeasible = objective.score_from_metrics(200, 0.30, 60, True, RFQ)  # misses all 3
    assert infeasible.score < feasible.score


def test_near_boundary_infeasible_still_below_feasible():
    # The realistic inversion: high energy but misses a constraint by a hair.
    feasible = objective.score_from_metrics(260, 0.60, 40, True, RFQ)
    infeasible = objective.score_from_metrics(290, 0.60, 45.5, True, RFQ)  # +30 Wh/kg, temp over by 0.5
    assert not infeasible.feasible
    assert infeasible.score < feasible.score


def test_feasibility_gate_property():
    # No infeasible design may ever outrank a feasible one, anywhere in the space.
    feas, infeas = [], []
    for se in (240, 260, 290, 320):
        for rate in (0.50, 0.70, 0.95):
            for temp in (10, 30, 45):
                r = objective.score_from_metrics(se, rate, temp, True, RFQ)
                (feas if r.feasible else infeas).append(r.score)
    for se in (200, 239, 320):           # guaranteed infeasible cases
        for rate in (0.30, 0.49):
            for temp in (50, 70):
                r = objective.score_from_metrics(se, rate, temp, True, RFQ)
                (feas if r.feasible else infeas).append(r.score)
    assert feas and infeas
    assert min(feas) > max(infeas)


def test_evaluate_runs_end_to_end():
    cell = calculator.realize_design(CELL, {"cathode.thickness_um": 65, "cathode.porosity": 0.35})
    r = objective.evaluate(cell, RFQ)
    assert r.metrics["sim_ok"]
    assert "capacity_Ah" in r.metrics and "energy_density_Wh_L" in r.metrics
