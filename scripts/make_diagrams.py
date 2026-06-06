"""Generate the matplotlib diagrams for the status PDF (the review-convergence
chart). The pipeline and flywheel flowcharts are Mermaid (docs/diagrams/*.mmd,
rendered with mmdc); see scripts/build_status_pdf.py for the full build sequence.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("results", exist_ok=True)
NAVY = "#1a2a4f"
BUILT = "#2e6fb7"

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
print("saved results/review_convergence.png")
