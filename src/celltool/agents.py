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
    assert "targets" in spec and "spec_c_rate" in spec, "spec missing required fields"
    demanding = spec["targets"]["min_rate_capability"] >= 0.5 or spec["spec_c_rate"] >= 3.0
    return {
        "n_calls": 30 if demanding else 20,
        "n_initial": 8,
        "rationale": "rate-demanding spec, wider search" if demanding else "relaxed spec, shorter search",
    }


def analysis(evaluations_by_trial, plateau_window=8, min_rel_gain=0.01):
    """SEAM (analysis agent). Contract: TRIAL-ORDERED evaluations -> stop/continue verdict.

    LLM version: read the round's metrics and judge whether designs are still
    meaningfully improving. Stub: declare converged when the running-best score has
    not improved by more than min_rel_gain (relative) across the last plateau_window
    trials. Requires trial order (not score-sorted) to see the improvement curve.
    """
    assert isinstance(evaluations_by_trial, list), "analysis expects a list of (overrides, result)"
    scores = [r.score for _, r in evaluations_by_trial]
    best = max(scores) if scores else float("-inf")
    converged = False
    if len(scores) >= plateau_window + 1:
        prior_best = max(scores[:-plateau_window])
        recent_best = max(scores)
        denom = abs(prior_best) if prior_best else 1.0
        converged = (recent_best - prior_best) / denom <= min_rel_gain
    return {
        "converged": converged,
        "best_score": best,
        "n_evaluated": len(scores),
        "message": "improvement flattened; reporting best designs" if converged
                   else "still improving; budget allows more search",
    }


def report_summary(opt_result, spec):
    """SEAM (report agent). Contract: optimization result -> plain-language summary.

    LLM version: write the engineer-facing narrative (tradeoffs, why the winner
    wins). Stub: a templated one-paragraph summary from the numbers.
    """
    b = opt_result.best_result.metrics
    lead = ("Recommended (a representative energy-max design on the feasible frontier)"
            if opt_result.best_result.feasible
            else "NO FEASIBLE DESIGN FOUND; closest is")
    return (
        f"{lead}: {b.get('specific_energy_Wh_kg', 0):.0f} Wh/kg, "
        f"{b.get('capacity_Ah', 0):.1f} Ah, rate capability {b.get('rate_capability', 0):.2f} at "
        f"{spec['spec_c_rate']}C, temp rise {b.get('temp_rise_C', 0):.0f} C (directional). "
        f"{opt_result.n_feasible} of {len(opt_result.evaluations)} evaluated designs met all targets."
    )
