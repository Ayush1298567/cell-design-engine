"""Generate the matplotlib diagrams for the docs: the review-convergence chart and
the system architecture block diagram (docs/diagrams/system_architecture.png).
The pipeline/flywheel flowcharts are Mermaid (docs/diagrams/*.mmd via mmdc).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

os.makedirs("results", exist_ok=True)
os.makedirs("docs/diagrams", exist_ok=True)

NAVY = "#1a2a4f"
BUILT = "#2e6fb7"

# ---- review convergence chart ----
fig, ax = plt.subplots(figsize=(7, 3.6))
rounds = ["Round 1\n(foundation)", "Round 2\n(complete engine)", "Round 3\n(verify fixes)"]
counts = [36, 21, 8]
bars = ax.bar(rounds, counts, color=[BUILT, "#3d8bd4", "#7fb3e0"], width=0.6)
for b, c in zip(bars, counts):
    ax.text(b.get_x() + b.get_width() / 2, c + 0.6, str(c), ha="center", fontsize=12, weight="bold", color=NAVY)
ax.set_ylabel("confirmed findings", color=NAVY)
ax.set_title("Adversarial review convergence (0 refuted across all rounds)", color=NAVY, fontsize=11, weight="bold")
ax.spines[["top", "right"]].set_visible(False)
ax.set_ylim(0, 40)
fig.tight_layout()
fig.savefig("results/review_convergence.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---- system architecture block diagram ----
BG, TXT, DIM, CORAL = "#0a0608", "#f4efed", "#9a8a85", "#ff5a69"
CORALLBL = "#ff8088"


def _box(ax, x0, x1, yc, h, title, sub, fill, edge, lw=1.0):
    ax.add_patch(FancyBboxPatch((x0, yc - h / 2), x1 - x0, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                facecolor=fill, edgecolor=edge, linewidth=lw))
    ax.text((x0 + x1) / 2, yc + 0.16, title, ha="center", va="center", color=TXT, fontsize=12.5, weight="bold")
    ax.text((x0 + x1) / 2, yc - 0.22, sub, ha="center", va="center", color=DIM, fontsize=9.5)


def _lane(ax, items, yc, fill, edge, x0=2.3, x1=15.6, gap=0.22, h=1.05, lw=1.0):
    n = len(items)
    w = (x1 - x0 - gap * (n - 1)) / n
    for i, (title, sub, *acc) in enumerate(items):
        bx0 = x0 + i * (w + gap)
        e = CORAL if acc and acc[0] else edge
        _box(ax, bx0, bx0 + w, yc, h, title, sub, fill, e, lw=2.0 if (acc and acc[0]) else lw)


fig, ax = plt.subplots(figsize=(16, 9.5))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.text(0.3, 9.55, "CUSTOM CELL DESIGN ENGINE", color=CORALLBL, fontsize=11, family="monospace", weight="bold")
ax.text(0.3, 9.0, "System architecture", color=TXT, fontsize=24, weight="bold")

lanes = [
    (8.0, "PEOPLE", [("Customer RFQ", "application + targets"), ("Engineers build & test", "top designs (unchanged)")], "#1c1a1d", "#6b6168"),
    (6.4, "LLM AGENTS  ·  bounded judgment (orchestrates, not the science)",
     [("Intake", "req → spec"), ("Strategy", "search plan"), ("Analysis", "progress / stop"), ("Evaluation", "cost, safety, mfg"), ("Report", "ranked write-up")], "#241813", "#c2724a"),
    (4.9, "ORCHESTRATOR", [("Orchestrator", "deterministic state machine — validates every agent answer")], "#141821", "#3a4654"),
    (3.4, "TOOLS  ·  the math and physics",
     [("Validation gate", "screen candidates"), ("Bayesian optimizer", "picks next design"), ("Cell calculator", "tier-1 quote-grade"), ("DFN simulation", "tier-3 directional"), ("Objective + scoring", "feasible? rank")], "#141821", "#3a4654"),
    (1.9, "KNOWLEDGE & CALIBRATION",
     [("Knowledge base", "retrieval grounds agents"), ("Calibration loop", "refit DFN to IBC cells (the moat)", True)], "#15121b", "#6f6470"),
]
for yc, label, items, fill, edge in lanes:
    ax.text(0.3, yc + 0.62, label, color=CORALLBL, fontsize=9.5, family="monospace")
    # special-case the wide single orchestrator box
    if len(items) == 1 and label == "ORCHESTRATOR":
        _box(ax, 2.3, 15.6, yc, 0.95, items[0][0], items[0][1], fill, edge)
    else:
        _lane(ax, items, yc, fill, edge)

ax.text(0.3, 0.55, "↓  requirement flows down into ranked designs        ↺  test data flows back up and recalibrates",
        color=DIM, fontsize=10, family="monospace")

fig.savefig("docs/diagrams/system_architecture.png", dpi=150, facecolor=BG, bbox_inches="tight")
plt.close(fig)

print("saved results/review_convergence.png and docs/diagrams/system_architecture.png")
