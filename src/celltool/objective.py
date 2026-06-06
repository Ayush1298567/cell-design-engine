"""Objective function: the contract between the metrics and the optimizer.

Turns a design into a single scalar score (higher is better) plus a feasibility
flag and the trust-tiered metrics. Ranking is lexicographic:

  feasible designs   -> score = tier-1 specific energy (ranked purely by energy)
  infeasible designs -> score = energy - INFEASIBLE_OFFSET - PENALTY*violations
  non-viable sims    -> NON_VIABLE_SCORE

The fixed INFEASIBLE_OFFSET guarantees no infeasible design can ever outrank a
feasible one (a tiny constraint miss still drops below every feasible design); the
relative PENALTY only provides a gradient WITHIN the infeasible region so the GP
can still climb toward the feasible boundary from an infeasible start.

This keeps trust tiers clean (CLAUDE.md rule 5): the ranking among feasible designs
is driven by the tier-1 number; the tier-3 directional numbers (rate, temp) only
gate feasibility, they never inflate the score.
"""

import math
from dataclasses import dataclass, field

from . import calculator, simulator

PENALTY = 1000.0           # gradient within the infeasible region only
INFEASIBLE_OFFSET = 1e6    # fixed drop so any infeasible design < every feasible one
NON_VIABLE_SCORE = -1e9    # designs the solver cannot evaluate (below infeasible band)


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
    if not math.isfinite(temp_rise_C):
        # design died before the thermal checkpoint (already fails rate): a full,
        # FINITE temp miss, so the score stays finite for the GP optimizer.
        violations["temp_rise"] = 1.0
    elif temp_rise_C > t["max_temp_rise_C"]:
        violations["temp_rise"] = (temp_rise_C - t["max_temp_rise_C"]) / t["max_temp_rise_C"]

    # Lexicographic: feasible designs ranked by energy; infeasible designs sit a
    # fixed offset below the entire feasible band, ranked ONLY by total violation so
    # the gradient always points toward feasibility (energy is excluded here so a
    # high-energy deeply-infeasible design cannot outrank a near-feasible one). The
    # fixed offset dominates any realistic energy (cells are < ~400 Wh/kg, offset 1e6),
    # so no infeasible design can reach the feasible band.
    if violations:
        score = -INFEASIBLE_OFFSET - PENALTY * sum(violations.values())
    else:
        score = specific_energy_Wh_kg
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
