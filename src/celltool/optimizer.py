"""Bayesian optimization over the design space.

Maintains a Gaussian-process surrogate of "how good is each design" and uses an
acquisition function to choose the next design to evaluate, balancing exploit
(near the best so far) and explore (where the model is uncertain). Finds good
designs in tens of evaluations instead of a blind grid of thousands, and works
from the first run. Pure math, no LLM.

The objective evaluator is injected (eval_fn) so the optimization loop can be
tested fast without running the DFN.
"""

from dataclasses import dataclass, field

from skopt import gp_minimize
from skopt.space import Real

from . import calculator, objective


@dataclass
class OptResult:
    best_overrides: dict
    best_result: object                       # ObjResult for the winner
    evaluations: list = field(default_factory=list)  # (overrides, ObjResult), score-sorted
    n_feasible: int = 0


def optimize(base_cell, platform, rfq, n_calls=30, n_initial=8, seed=0, eval_fn=objective.evaluate):
    """Search platform.design_variables to maximize the objective score."""
    dv = platform["design_variables"]
    names = list(dv.keys())
    space = [Real(dv[n]["min"], dv[n]["max"], name=n) for n in names]

    history = []

    def negative_score(point):
        overrides = dict(zip(names, point))
        cell = calculator.realize_design(base_cell, overrides)
        result = eval_fn(cell, rfq)
        history.append((overrides, result))
        return -result.score  # gp_minimize minimizes

    gp_minimize(
        negative_score,
        space,
        n_calls=n_calls,
        n_initial_points=n_initial,
        random_state=seed,
    )

    evaluations = sorted(history, key=lambda hr: hr[1].score, reverse=True)
    best_overrides, best_result = evaluations[0]
    n_feasible = sum(1 for _, r in evaluations if r.feasible)
    return OptResult(best_overrides, best_result, evaluations, n_feasible)
