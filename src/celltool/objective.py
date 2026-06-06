"""Objective function: the contract between the metrics and the optimizer.

Turns a design into a single scalar score (higher is better) plus a feasibility
flag and the trust-tiered metrics. The optimizer MAXIMIZES the application's
objective metric (the tier-1 quote-grade specific energy, for a drone) subject to
the rate and temperature targets as constraints. Constraints are handled as a soft
penalty, so the optimizer can climb toward feasibility from an infeasible start,
and among feasible designs the score is just the objective metric.

This keeps trust tiers clean (CLAUDE.md rule 5): the RANKING is driven by the
tier-1 number; the tier-3 directional numbers (rate, temp) only gate feasibility,
they never inflate the score. There is no reward for exceeding a constraint, which
would otherwise trade away the primary goal.
"""

from dataclasses import dataclass, field

from . import calculator, simulator

PENALTY = 1000.0         # per-unit-violation penalty, large vs the Wh/kg objective
NON_VIABLE_SCORE = -1e9  # designs the solver cannot evaluate


@dataclass
class ObjResult:
    score: float
    feasible: bool
    metrics: dict = field(default_factory=dict)
    violations: dict = field(default_factory=dict)


def score_from_metrics(specific_energy_Wh_kg, rate_capability, temp_rise_C, ok, rfq):
    """Pure scoring step (no DFN run), so it is fast and unit-testable."""
    t = rfq["targets"]
    metrics = {
        "specific_energy_Wh_kg": specific_energy_Wh_kg,  # tier-1
        "rate_capability": rate_capability,              # tier-3
        "temp_rise_C": temp_rise_C,                      # tier-3
        "sim_ok": ok,
    }
    if not ok:
        return ObjResult(NON_VIABLE_SCORE, False, metrics, {"sim": 1.0})

    violations = {}
    if specific_energy_Wh_kg < t["min_specific_energy_Wh_kg"]:
        violations["specific_energy"] = (t["min_specific_energy_Wh_kg"] - specific_energy_Wh_kg) / t["min_specific_energy_Wh_kg"]
    if rate_capability < t["min_rate_capability"]:
        violations["rate_capability"] = (t["min_rate_capability"] - rate_capability) / t["min_rate_capability"]
    if temp_rise_C > t["max_temp_rise_C"]:
        violations["temp_rise"] = (temp_rise_C - t["max_temp_rise_C"]) / t["max_temp_rise_C"]

    # Maximize the objective metric; subtract a penalty for any constraint miss so
    # the optimizer is pulled toward feasibility. No reward for exceeding a target.
    score = specific_energy_Wh_kg - PENALTY * sum(violations.values())
    return ObjResult(score, len(violations) == 0, metrics, violations)


def evaluate(cell, rfq):
    """Run calculator + simulator on a realized cell and score it."""
    m = calculator.compute(cell)
    s = simulator.evaluate_design(cell, rfq["spec_c_rate"])
    result = score_from_metrics(m.specific_energy_Wh_kg, s.rate_capability, s.temp_rise_C, s.ok, rfq)
    # carry the full quote-grade metrics for the report
    result.metrics.update(
        capacity_Ah=m.capacity_Ah,
        energy_Wh=m.energy_Wh,
        energy_density_Wh_L=m.energy_density_Wh_L,
        mass_g=m.mass_g,
        np_ratio=m.np_ratio,
    )
    return result
