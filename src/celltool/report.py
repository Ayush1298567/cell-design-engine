"""Report layer: design-space maps + ranked, trust-tiered designs + markdown.

The heatmaps give engineers intuition about the landscape (where good designs
live, where constraints bind), not just a single answer.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from . import calculator, objective


def fmt_temp(tr):
    """Display a temp rise. Non-finite means the design died before the thermal
    checkpoint (a non-comparable, infeasible design), shown as '>limit' not 'inf'."""
    return ">limit" if not np.isfinite(tr) else f"{tr:.0f}"


def evaluate_grid(base_cell, platform, rfq, n_thk=15, n_por=13, progress=False):
    """Evaluate a dense grid of designs for the landscape map (heavy: runs the DFN)."""
    dv = platform["design_variables"]
    thks = np.linspace(dv["cathode.thickness_um"]["min"], dv["cathode.thickness_um"]["max"], n_thk)
    pors = np.linspace(dv["cathode.porosity"]["min"], dv["cathode.porosity"]["max"], n_por)
    shape = (n_por, n_thk)
    se = np.full(shape, np.nan)
    score = np.full(shape, np.nan)
    feasible = np.zeros(shape, dtype=bool)
    total = n_thk * n_por
    k = 0
    for i, por in enumerate(pors):
        for j, thk in enumerate(thks):
            cell = calculator.realize_design(base_cell, {"cathode.thickness_um": float(thk), "cathode.porosity": float(por)})
            r = objective.evaluate(cell, rfq)
            se[i, j] = r.metrics.get("specific_energy_Wh_kg", np.nan)
            score[i, j] = r.score if r.score > -1e8 else np.nan
            feasible[i, j] = r.feasible
            k += 1
            if progress:
                print(f"  grid {k}/{total}", end="\r")
    if progress:
        print()
    return {"thks": thks, "pors": pors, "specific_energy": se, "score": score, "feasible": feasible}


def render_heatmap(grid, opt_result, rfq, out_path):
    thks, pors = grid["thks"], grid["pors"]
    feas = grid["feasible"].astype(float)
    extent = [thks.min(), thks.max(), pors.min(), pors.max()]
    bx = opt_result.best_overrides["cathode.thickness_um"]
    by = opt_result.best_overrides["cathode.porosity"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    im1 = ax1.imshow(grid["specific_energy"], origin="lower", aspect="auto", extent=extent, cmap="viridis")
    ax1.set_title("Specific energy [Wh/kg] (tier-1)\nwhite = feasible boundary, star = recommended")
    fig.colorbar(im1, ax=ax1)

    # Score panel: mask infeasible cells so the deep penalty band does not read as
    # a smooth landscape; only the feasible region is colored.
    score_masked = np.where(grid["feasible"], grid["score"], np.nan)
    im2 = ax2.imshow(score_masked, origin="lower", aspect="auto", extent=extent, cmap="magma")
    xs = [o["cathode.thickness_um"] for o, _ in opt_result.evaluations]
    ys = [o["cathode.porosity"] for o, _ in opt_result.evaluations]
    ax2.scatter(xs, ys, s=16, c="cyan", alpha=0.7, label="optimizer samples")
    ax2.set_title("Objective score (feasible only) with optimizer path")

    for ax in (ax1, ax2):
        ax.contourf(thks, pors, feas, levels=[-0.5, 0.5], colors=["gray"], alpha=0.22)  # shade infeasible
        ax.contour(thks, pors, feas, levels=[0.5], colors="white", linewidths=2)
        ax.scatter([bx], [by], s=220, marker="*", c="white", edgecolors="black", label="recommended", zorder=5)
        ax.set_xlabel("Cathode thickness [um]")
        ax.set_ylabel("Cathode porosity")
    ax2.legend(loc="upper right")
    fig.colorbar(im2, ax=ax2)

    best = opt_result.best_result.metrics
    t = rfq["targets"]
    fig.text(0.5, 0.005,
             f"Recommended design is constraint-binding: rate {best.get('rate_capability', 0):.2f} "
             f"(floor {t['min_rate_capability']:.2f}), temp rise {fmt_temp(best.get('temp_rise_C', 0))} C "
             f"(limit {t['max_temp_rise_C']:.0f}, directional). The brightest energy cells lie OUTSIDE "
             f"the feasible boundary.", ha="center", fontsize=9)
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=130)
    return out_path


def distinct_designs(evaluations, k=5, min_thk=4.0, min_por=0.03, feasible_only=True):
    """Pick the top-k score-ranked designs that are meaningfully distinct, so the
    list shows real alternatives instead of near-clones of the winner. (A lighter
    stand-in for the information-maximizing DoE build plan, which is deferred.)"""
    chosen = []
    for ov, r in evaluations:  # already score-sorted
        if feasible_only and not r.feasible:
            continue
        if any(
            abs(ov["cathode.thickness_um"] - c["cathode.thickness_um"]) < min_thk
            and abs(ov["cathode.porosity"] - c["cathode.porosity"]) < min_por
            for c, _ in chosen
        ):
            continue
        chosen.append((ov, r))
        if len(chosen) >= k:
            break
    return chosen


def write_report(run_result, summary, heatmap_path, out_path, top_n=5):
    opt = run_result.opt
    lines = []
    lines.append("# Cell design run report\n")
    lines.append(f"Application: **{run_result.spec.get('application', 'n/a')}**, "
                 f"peak rate {run_result.spec['spec_c_rate']}C. "
                 f"Search: {run_result.strategy['n_calls']} evaluations "
                 f"({run_result.strategy['rationale']}).\n")
    lines.append(f"\n{summary}\n")
    ranked = distinct_designs(opt.evaluations, k=top_n)
    if ranked:
        lines.append("\n## Ranked designs (distinct feasible alternatives)\n")
    else:
        ranked = opt.evaluations[:top_n]
        lines.append("\n## Closest designs (NO FEASIBLE DESIGN FOUND)\n")
    lines.append("Tier-1 (quote-grade): specific energy, capacity, energy density. "
                 "Tier-3 (directional): rate capability, temp rise.\n")
    lines.append("\n| # | cath um | porosity | Wh/kg | Ah | Wh/L | rate | dT C | feasible |")
    lines.append("|--:|--:|--:|--:|--:|--:|--:|--:|:--:|")
    for idx, (ov, r) in enumerate(ranked, 1):
        m = r.metrics
        lines.append(
            f"| {idx} | {ov['cathode.thickness_um']:.0f} | {ov['cathode.porosity']:.3f} | "
            f"{m.get('specific_energy_Wh_kg', 0):.0f} | {m.get('capacity_Ah', 0):.1f} | "
            f"{m.get('energy_density_Wh_L', 0):.0f} | {m.get('rate_capability', 0):.2f} | "
            f"{fmt_temp(m.get('temp_rise_C', 0))} | {'yes' if r.feasible else 'no'} |"
        )
    lines.append(f"\n{opt.n_feasible} of {len(opt.evaluations)} evaluated designs were feasible. "
                 "The winner is one representative energy-max design on the feasible frontier; "
                 "the rows above are distinct alternatives trading energy for rate/thermal margin.\n")
    lines.append(f"\n![design space]({os.path.basename(heatmap_path)})\n")
    lines.append("\n_Tier-1 (specific energy, capacity, energy density) is quote-grade calculator "
                 "algebra. Tier-3 (rate capability, temp rise, and the feasibility gate on them) is a "
                 "directional ranking from an uncalibrated literature DFN (Chen2020 chemistry on this "
                 "geometry); the DFN's internal electrode balance is not the quoted N/P. Calibration on "
                 "IBC test data is what makes the tier-3 numbers design-guidance grade._\n")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    return out_path
