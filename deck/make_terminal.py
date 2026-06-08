"""Render a clean terminal clip (deck/assets/term.mp4) of the real run output,
revealed line by line. Dark panel, monospace. Numbers come from the real run."""
import json

import matplotlib

matplotlib.use("Agg")
import imageio_ffmpeg
import matplotlib.animation as manim
import matplotlib.pyplot as plt

plt.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
plt.rcParams["font.family"] = "monospace"

d = json.load(open("results/demo_data.json"))
b = d["best"]
thk, por = round(b["thickness"]), round(b["porosity"] * 100)
we, ah = round(b["specific_energy"]), b["capacity"]
nf, nt = d["n_feasible"], d["n_total"]

BG, PANEL, DIM, OK, ACC, HEAD, NUM = "#0a0d12", "#0f141b", "#aeb6c2", "#69d08a", "#5fa8e6", "#ffffff", "#ffb27a"
lines = [
    ("$ pytest -q", ACC), ("47 passed in 77s", OK), ("", DIM),
    ("$ python scripts/run_demo.py", ACC),
    ("intake     parsed requirement into spec  (3C, 45 min)", DIM),
    ("strategy   plan: energy-first, 30 trials in envelope", DIM),
    (f"search     trial 30/30    best feasible {we} Wh/kg", DIM),
    ("analyze    improvement flattened, stopping", DIM),
    ("report     ranked 5 buildable designs", DIM),
    ("", DIM),
    (f"recommended   {thk} um cathode, {por}% porosity", HEAD),
    (f"              {we} Wh/kg   {ah:.1f} Ah   {nf}/{nt} designs feasible", NUM),
    ("saved         design_space.png    run_report.md", DIM),
]

fig = plt.figure(figsize=(11.2, 4.4), dpi=120)
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0.03, 0.05, 0.94, 0.9])
ax.set_facecolor(PANEL)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
# title bar dots
for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
    ax.scatter(0.018 + i * 0.018, 0.95, s=70, color=c, zorder=5, clip_on=False)

y0, dy, x0 = 0.86, 0.066, 0.03
texts = []
for i, (txt, col) in enumerate(lines):
    t = ax.text(x0, y0 - i * dy, txt, color=col, fontsize=13.5, family="monospace",
                fontweight="bold" if col in (HEAD, ACC) else "normal", va="top", visible=False)
    texts.append(t)
cursor = ax.text(x0, y0, "█", color=ACC, fontsize=13.5, va="top")

PER = 7
frames = len(lines) * PER + 22


def update(f):
    shown = min(len(lines), f // PER + 1)
    for i, t in enumerate(texts):
        t.set_visible(i < shown)
    j = min(len(lines) - 1, shown - 1)
    cursor.set_position((x0 + 0.0095 * (len(lines[j][0]) + 1), y0 - j * dy))
    cursor.set_visible((f // 4) % 2 == 0)
    return texts + [cursor]


anim = manim.FuncAnimation(fig, update, frames=frames, interval=90, blit=False)
anim.save("deck/assets/term.mp4", writer=manim.FFMpegWriter(fps=11, codec="libx264", extra_args=["-pix_fmt", "yuv420p"]))
plt.close(fig)
print(f"wrote deck/assets/term.mp4 ({frames} frames)")
