"""Generate diagrams for the status PDF: pipeline architecture + review convergence."""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

os.makedirs("results", exist_ok=True)

NAVY = "#1a2a4f"
BUILT = "#2e6fb7"     # deterministic, built
SEAM = "#e0a13c"      # LLM seam, stubbed
HUMAN = "#8a8f99"     # human / IO
TEXT = "#ffffff"


def box(ax, x, y, w, h, label, color, fontsize=10):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                linewidth=0, facecolor=color))
    ax.text(x, y, label, ha="center", va="center", color=TEXT, fontsize=fontsize, weight="bold")


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.6, color=NAVY))


# ---- Diagram 1: pipeline architecture ----
fig, ax = plt.subplots(figsize=(13, 4.2))
ax.set_xlim(0, 26)
ax.set_ylim(0, 8)
ax.axis("off")

y = 5.2
stages = [
    (2.0, 2.4, "Customer\nRFQ", HUMAN),
    (5.2, 2.0, "Intake *", SEAM),
    (8.0, 2.0, "Strategy *", SEAM),
    (12.6, 4.6, "Bayesian Optimizer\nover Calculator (T1) + DFN (T3)\n→ Objective", BUILT),
    (17.2, 2.0, "Analysis *", SEAM),
    (20.4, 2.6, "Report\n(ranked designs\n+ design maps)", BUILT),
    (23.8, 2.6, "Engineer\nreview & build", HUMAN),
]
centers = []
for x, w, label, color in stages:
    box(ax, x, y, w, 1.5 if "\n\n" not in label else 2.0, label, color, fontsize=9)
    centers.append((x, w))
for (x1, w1), (x2, w2) in zip(centers[:-1], centers[1:]):
    arrow(ax, x1 + w1 / 2, y, x2 - w2 / 2, y)

# loop arrow on the optimizer
ax.add_patch(FancyArrowPatch((11.8, 6.7), (13.4, 6.7), connectionstyle="arc3,rad=-0.9",
                             arrowstyle="-|>", mutation_scale=12, linewidth=1.4, color=BUILT))
ax.text(12.6, 7.4, "every trial informed by all prior trials", ha="center", fontsize=8, color=BUILT, style="italic")

# legend
leg = [(BUILT, "Built (deterministic)"), (SEAM, "LLM seam *  (stubbed today, swap-in later)"), (HUMAN, "Human / I-O")]
for i, (c, t) in enumerate(leg):
    ax.add_patch(FancyBboxPatch((2.0 + i * 8.0, 1.2), 0.5, 0.5, boxstyle="round,pad=0.02", linewidth=0, facecolor=c))
    ax.text(2.7 + i * 8.0, 1.45, t, va="center", fontsize=8.5, color=NAVY)
ax.text(13, 7.9, "Engine pipeline: requirements in, ranked buildable designs out",
        ha="center", fontsize=12, weight="bold", color=NAVY)
fig.tight_layout()
fig.savefig("results/architecture.png", dpi=150, bbox_inches="tight")

# ---- Diagram 2: review convergence ----
fig2, ax2 = plt.subplots(figsize=(7, 3.6))
rounds = ["Round 1\n(foundation)", "Round 2\n(complete engine)", "Round 3\n(verify fixes)"]
counts = [36, 21, 8]
bars = ax2.bar(rounds, counts, color=[BUILT, "#3d8bd4", "#7fb3e0"], width=0.6)
for b, c in zip(bars, counts):
    ax2.text(b.get_x() + b.get_width() / 2, c + 0.6, str(c), ha="center", fontsize=12, weight="bold", color=NAVY)
ax2.set_ylabel("confirmed findings", color=NAVY)
ax2.set_title("Adversarial review convergence (0 refuted across all rounds)", color=NAVY, fontsize=11, weight="bold")
ax2.spines[["top", "right"]].set_visible(False)
ax2.set_ylim(0, 40)
fig2.tight_layout()
fig2.savefig("results/review_convergence.png", dpi=150, bbox_inches="tight")

print("saved results/architecture.png and results/review_convergence.png")
