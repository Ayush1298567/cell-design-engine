"""LLM agent seams.

Each function is a decision point where the full tool would consult an LLM. Today
each has a deterministic stub body, but a FIXED input/output contract. Swapping in
a real LLM later means replacing only the function body with an API call that
returns the same shape and a schema-validated response -- the orchestrator that
calls these never changes. No API key is needed to run the engine.

Contract per seam is documented above each function. See THE_IDEA.md steps 2, 6,
10, 14 for the intended LLM roles.
"""


def intake(rfq_raw):
    """SEAM (intake agent). Contract: raw application -> structured spec dict.

    LLM version: parse a plain-language conversation into this structured spec and
    surface implied requirements (desert -> thermal margin, fast charge -> plating
    risk). Stub: the rfq config is already structured, so pass it through.
    """
    assert "spec_c_rate" in rfq_raw and "targets" in rfq_raw, "rfq missing required fields"
    return rfq_raw


def strategy(spec):
    """SEAM (strategy agent). Contract: spec -> optimizer search config.

    LLM version: read the spec + retrieved knowledge and choose search regions,
    weights, and budget. Stub: scale the evaluation budget with how demanding the
    rate requirement is (tighter rate -> harder search -> more evaluations).
    """
    demanding = spec["targets"]["min_rate_capability"] >= 0.5 or spec["spec_c_rate"] >= 3.0
    return {
        "n_calls": 30 if demanding else 20,
        "n_initial": 8,
        "rationale": "rate-demanding spec, wider search" if demanding else "relaxed spec, shorter search",
    }


def analysis(evaluations, plateau_window=8):
    """SEAM (analysis agent). Contract: ranked evaluations -> stop/continue verdict.

    LLM version: read the round's metrics and judge whether designs are still
    meaningfully improving, returning a bounded decision. Stub: declare converged
    when the best score has not improved within the last `plateau_window` trials.
    """
    scores_in_order = [r.score for _, r in evaluations]  # NOTE: evaluations are score-sorted
    best = max(scores_in_order) if scores_in_order else float("-inf")
    converged = len(evaluations) >= plateau_window
    return {
        "converged": converged,
        "best_score": best,
        "n_evaluated": len(evaluations),
        "message": "search budget spent; reporting best designs" if converged else "still improving",
    }


def report_summary(opt_result, spec):
    """SEAM (report agent). Contract: optimization result -> plain-language summary.

    LLM version: write the engineer-facing narrative (tradeoffs, why the winner
    wins). Stub: a templated one-paragraph summary from the numbers.
    """
    b = opt_result.best_result.metrics
    feas = "feasible" if opt_result.best_result.feasible else "INFEASIBLE (closest)"
    return (
        f"Best design is {feas}: {b.get('specific_energy_Wh_kg', 0):.0f} Wh/kg, "
        f"{b.get('capacity_Ah', 0):.1f} Ah, rate capability {b.get('rate_capability', 0):.2f} at "
        f"{spec['spec_c_rate']}C, temp rise {b.get('temp_rise_C', 0):.0f} C (directional). "
        f"{opt_result.n_feasible} of {len(opt_result.evaluations)} evaluated designs met all targets."
    )
