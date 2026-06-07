import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { scales, Bounds } from "../lib/plot";
import { rgb, heat } from "../lib/colormap";
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
      const b = heat(t);
      const fill = feas ? rgb(b, 0.92) : rgb([b[0] * 0.4, b[1] * 0.4, b[2] * 0.4], 0.85);
      cells.push(
        <div key={`${i}-${j}`} style={{ position: "absolute", left: sx(thks[j]) - cellW / 2 + 1.5, top: sy(pors[i]) - cellH / 2 + 1.5, width: cellW - 3, height: cellH - 3, background: fill, borderRadius: 3 }} />
      );
    }
  }
  return (
    <div style={{ opacity: op }}>
      {cells}
      <div style={{ position: "absolute", left: plot.x - cellW / 2, top: plot.y - cellH / 2, width: plot.w + cellW, height: plot.h + cellH, border: `1px solid ${colors.hairline}`, borderRadius: 8 }} />
    </div>
  );
};

export const Dot: React.FC<{ d: any; appear: number; plot: Plot }> = ({ d, appear, plot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { sx, sy } = scales(bounds, plot);
  if (frame < appear) return null;
  const s = spring({ frame: frame - appear, fps, config: { damping: 16, stiffness: 220 } });
  const r = interpolate(s, [0, 1], [0, d.feasible ? 7 : 5]);
  return (
    <div style={{ position: "absolute", left: sx(d.thickness) - r, top: sy(d.porosity) - r, width: r * 2, height: r * 2, borderRadius: "50%", background: d.feasible ? "#ffffff" : "transparent", border: `1.5px solid ${colors.coral}`, opacity: d.feasible ? 1 : 0.45 }} />
  );
};

export const Winner: React.FC<{ starFrame: number; plot: Plot }> = ({ starFrame, plot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { sx, sy } = scales(bounds, plot);
  if (frame < starFrame) return null;
  const s = spring({ frame: frame - starFrame, fps, config: { damping: 12 } });
  return (
    <div style={{ position: "absolute", left: sx(data.best.thickness) - 22, top: sy(data.best.porosity) - 22, width: 44, height: 44, transform: `scale(${interpolate(s, [0, 1], [0, 1])})`, color: "#ffffff", fontSize: 44, lineHeight: "44px", textAlign: "center", textShadow: `0 0 18px ${colors.coral}` }}>
      {"★"}
    </div>
  );
};
