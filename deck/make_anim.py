"""Render the optimizer-search animation (deck/assets/search.mp4) and a clean
static design-space map (deck/assets/designspace.png) from results/demo_data.json.
Light, professional palette to match the deck."""
import json

import matplotlib

matplotlib.use("Agg")
import imageio_ffmpeg
import matplotlib.animation as manim
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["animation.ffmpeg_path"] = imageio_ffmpeg.get_ffmpeg_exe()
plt.rcParams["font.family"] = "Helvetica Neue"

NAVY, ACCENT, GRID = "#16203a", "#c2603a", "#e4e7ee"
d = json.load(open("results/demo_data.json"))
thks = np.array(d["grid"]["thks"], float)
pors = np.array(d["grid"]["pors"], float)
E = np.array([[np.nan if v is None else v for v in r] for r in d["grid"]["energy"]], float)
F = np.array(d["grid"]["feasible"], float)
if E.shape == (len(thks), len(pors)):
    E, F = E.T, F.T  # want (por, thk)
traj = d["trajectory"]
best = d["best"]
N = len(traj)


def setup(ax):
    Z = np.ma.masked_invalid(E)
    pm = ax.pcolormesh(thks, pors, Z, cmap="Blues", shading="gouraud", vmin=np.nanmin(E), vmax=np.nanmax(E))
    # shade infeasible region softly, draw the feasible boundary
    ax.contourf(thks, pors, F, levels=[-0.5, 0.5], colors=["white"], alpha=0.45)
    ax.contour(thks, pors, F, levels=[0.5], colors=[NAVY], linewidths=1.3, linestyles="--")
    ax.set_xlabel("cathode thickness  (µm)", fontsize=13, color=NAVY)
    ax.set_ylabel("cathode porosity", fontsize=13, color=NAVY)
    ax.tick_params(colors="#6a7488", labelsize=11)
    for s in ax.spines.values():
        s.set_color(GRID)
    return pm


# --- static design-space map ---
fig, ax = plt.subplots(figsize=(7.6, 6.2), dpi=150)
setup(ax)
for t in traj:
    ax.scatter(t["thickness"], t["porosity"], s=42, facecolor=ACCENT if t["feasible"] else "none",
               edgecolor=ACCENT, linewidths=1.4, alpha=0.85, zorder=3)
ax.scatter(best["thickness"], best["porosity"], marker="*", s=620, facecolor="#fff", edgecolor=NAVY, linewidths=1.8, zorder=5)
ax.set_title("Design space: specific energy, with the recommended design", fontsize=13, color=NAVY, pad=12)
fig.tight_layout()
fig.savefig("deck/assets/designspace.png", facecolor="white")
plt.close(fig)

# --- animation ---
PER = 2
HOLD = 18
frames = N * PER + HOLD
fig, ax = plt.subplots(figsize=(8.4, 6.0), dpi=140)
setup(ax)
cnt = ax.text(0.02, 1.04, "", transform=ax.transAxes, fontsize=14, color=NAVY, fontweight="bold", va="bottom")
scat = ax.scatter([], [], s=46, zorder=3)
star = ax.scatter([], [], marker="*", s=640, facecolor="#fff", edgecolor=NAVY, linewidths=1.8, zorder=5)


def update(f):
    k = min(N, f // PER + 1) if f < N * PER else N
    pts = traj[:k]
    xy = np.array([[t["thickness"], t["porosity"]] for t in pts]) if pts else np.empty((0, 2))
    fc = [ACCENT if t["feasible"] else (1, 1, 1, 0) for t in pts]
    scat.set_offsets(xy)
    scat.set_facecolor(fc)
    scat.set_edgecolor(ACCENT)
    bsf = max([t["specific_energy"] for t in pts if t["feasible"] and t["specific_energy"]] + [0])
    cnt.set_text(f"trial {k:>2} / {N}     best feasible: {bsf:.0f} Wh/kg" if k < N else
                 f"done · {N} trials     recommended: {best['specific_energy']:.0f} Wh/kg")
    star.set_offsets(np.array([[best["thickness"], best["porosity"]]]) if f >= N * PER else np.empty((0, 2)))
    return scat, star, cnt


fig.tight_layout()
anim = manim.FuncAnimation(fig, update, frames=frames, interval=90, blit=False)
anim.save("deck/assets/search.mp4", writer=manim.FFMpegWriter(fps=11, codec="libx264", extra_args=["-pix_fmt", "yuv420p"]))
plt.close(fig)
print(f"wrote deck/assets/search.mp4 ({frames} frames) and designspace.png")
