import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { scales, Bounds } from "../lib/plot";
import { rgb, viridis } from "../lib/colormap";
import { colors } from "../theme";
import data from "../demo_data.json";

const bounds = data.bounds as Bounds;
const thks = data.grid.thks;
const pors = data.grid.pors;
const nThk = thks.length;
const nPor = pors.length;
const flatE = data.grid.energy.flat().filter((v): v is number => v != null);
const minE = Math.min(...flatE);
const maxE = Math.max(...flatE);

export type Plot = { x: number; y: number; w: number; h: number };

export const Heatmap: React.FC<{ plot: Plot; fadeStart?: number; fadeEnd?: number }> = ({ plot, fadeStart = 0, fadeEnd = 20 }) => {
  const frame = useCurrentFrame();
  const { sx, sy } = scales(bounds, plot);
  const cellW = plot.w / (nThk - 1);
  const cellH = plot.h / (nPor - 1);
  const op = interpolate(frame, [fadeStart, fadeEnd], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cells: React.ReactNode[] = [];
  for (let i = 0; i < nPor; i++) {
    for (let j = 0; j < nThk; j++) {
      const e = data.grid.energy[i][j];
      if (e == null) continue;
      const feas = data.grid.feasible[i][j] === 1;
      const t = (e - minE) / (maxE - minE || 1);
      const b = viridis(t);
      const fill = feas ? rgb(b, 1) : rgb([b[0] * 0.35, b[1] * 0.35, b[2] * 0.35], 1);
      cells.push(
        <div key={`${i}-${j}`} style={{ position: "absolute", left: sx(thks[j]) - cellW / 2, top: sy(pors[i]) - cellH / 2, width: cellW + 1, height: cellH + 1, background: fill }} />
      );
    }
  }
  return <div style={{ opacity: op }}>{cells}</div>;
};

export const Dot: React.FC<{ d: any; appear: number; plot: Plot }> = ({ d, appear, plot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { sx, sy } = scales(bounds, plot);
  if (frame < appear) return null;
  const s = spring({ frame: frame - appear, fps, config: { damping: 14, stiffness: 220 } });
  const r = interpolate(s, [0, 1], [0, d.feasible ? 8 : 5]);
  return (
    <div style={{ position: "absolute", left: sx(d.thickness) - r, top: sy(d.porosity) - r, width: r * 2, height: r * 2, borderRadius: "50%", background: d.feasible ? colors.cyan : "transparent", border: d.feasible ? "2px solid #ffffff" : `2px solid ${colors.dim}`, boxShadow: d.feasible ? `0 0 10px ${colors.cyan}` : "none", opacity: d.feasible ? 0.95 : 0.5 }} />
  );
};

export const Winner: React.FC<{ starFrame: number; plot: Plot }> = ({ starFrame, plot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { sx, sy } = scales(bounds, plot);
  if (frame < starFrame) return null;
  const s = spring({ frame: frame - starFrame, fps, config: { damping: 12 } });
  return (
    <div style={{ position: "absolute", left: sx(data.best.thickness) - 24, top: sy(data.best.porosity) - 24, width: 48, height: 48, transform: `scale(${interpolate(s, [0, 1], [0, 1])})`, color: "#ffffff", fontSize: 48, lineHeight: "48px", textAlign: "center", textShadow: `0 0 16px ${colors.coral}` }}>
      {"★"}
    </div>
  );
};
