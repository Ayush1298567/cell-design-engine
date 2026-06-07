import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";
import { PLOT, scales, Bounds } from "../lib/plot";
import { rgb, viridis } from "../lib/colormap";
import data from "../demo_data.json";

const bounds = data.bounds as Bounds;
const { sx, sy } = scales(bounds);
const thks = data.grid.thks;
const pors = data.grid.pors;
const nThk = thks.length;
const nPor = pors.length;
const cellW = PLOT.w / (nThk - 1);
const cellH = PLOT.h / (nPor - 1);
const flatE = data.grid.energy.flat().filter((v): v is number => v != null);
const minE = Math.min(...flatE);
const maxE = Math.max(...flatE);

const DOT_START = 60;
const PER_DOT = Math.max(5, Math.floor(250 / data.trajectory.length));
const STAR = DOT_START + data.trajectory.length * PER_DOT + 14;

const Heatmap: React.FC = () => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [20, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
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

const Dot: React.FC<{ d: any; appear: number }> = ({ d, appear }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < appear) return null;
  const s = spring({ frame: frame - appear, fps, config: { damping: 14, stiffness: 200 } });
  const r = interpolate(s, [0, 1], [0, d.feasible ? 9 : 6]);
  return (
    <div style={{ position: "absolute", left: sx(d.thickness) - r, top: sy(d.porosity) - r, width: r * 2, height: r * 2, borderRadius: "50%", background: d.feasible ? colors.cyan : "transparent", border: d.feasible ? "2px solid #ffffff" : `2px solid ${colors.dim}`, boxShadow: d.feasible ? `0 0 12px ${colors.cyan}` : "none", opacity: d.feasible ? 0.95 : 0.5 }} />
  );
};

const Winner: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < STAR) return null;
  const s = spring({ frame: frame - STAR, fps, config: { damping: 12 } });
  return (
    <div style={{ position: "absolute", left: sx(data.best.thickness) - 26, top: sy(data.best.porosity) - 26, width: 52, height: 52, transform: `scale(${interpolate(s, [0, 1], [0, 1])})`, color: "#ffffff", fontSize: 52, lineHeight: "52px", textAlign: "center", textShadow: `0 0 16px ${colors.coral}` }}>
      {"★"}
    </div>
  );
};

const Readout: React.FC = () => {
  const frame = useCurrentFrame();
  const n = data.trajectory.length;
  const visible = Math.max(0, Math.min(n, Math.floor((frame - DOT_START) / PER_DOT) + 1));
  let best = 0;
  for (let k = 0; k < visible; k++) {
    const d = data.trajectory[k];
    if (d.feasible && d.specific_energy && d.specific_energy > best) best = d.specific_energy;
  }
  return (
    <div style={{ position: "absolute", left: 1130, top: 230, width: 640 }}>
      <FadeUp delay={8}>
        <div style={{ fontFamily: fonts.mono, letterSpacing: 5, color: colors.coral, fontSize: 20, textTransform: "uppercase" }}>Requirement</div>
        <div style={{ fontSize: 38, fontFamily: fonts.serif, marginTop: 8 }}>Drone battery, hard 3C discharge</div>
      </FadeUp>
      <FadeUp delay={40} style={{ marginTop: 50 }}>
        <div style={{ fontFamily: fonts.mono, fontSize: 32, color: colors.dim }}>
          trial <span style={{ color: colors.text }}>{String(visible).padStart(2, "0")}</span> / {n}
        </div>
        <div style={{ fontFamily: fonts.mono, fontSize: 32, color: colors.dim, marginTop: 14 }}>
          best so far <span style={{ color: colors.cyan }}>{best ? best.toFixed(0) : "..."}</span> Wh/kg
        </div>
        <div style={{ fontSize: 25, color: colors.dim, marginTop: 26, lineHeight: 1.5 }}>
          The optimizer tries a design, the physics scores it, and each trial guides the next.
        </div>
      </FadeUp>
      {frame >= STAR && (
        <FadeUp delay={STAR + 6} style={{ marginTop: 40 }}>
          <div style={{ background: colors.panel, border: `1px solid ${colors.coral}`, borderRadius: 14, padding: "24px 28px" }}>
            <div style={{ fontFamily: fonts.mono, letterSpacing: 5, color: colors.coral, fontSize: 18, textTransform: "uppercase" }}>Best design found</div>
            <div style={{ fontSize: 44, fontFamily: fonts.serif, color: colors.amber, marginTop: 10 }}>
              {data.best.specific_energy?.toFixed(0)} Wh/kg &middot; {data.best.capacity?.toFixed(1)} Ah
            </div>
            <div style={{ fontSize: 26, color: colors.dim, marginTop: 8 }}>{data.best.thickness.toFixed(0)} &micro;m cathode, {(data.best.porosity * 100).toFixed(0)}% porosity</div>
          </div>
        </FadeUp>
      )}
    </div>
  );
};

export const Search: React.FC = () => {
  const frame = useCurrentFrame();
  const n = data.trajectory.length;
  const visible = Math.max(0, Math.min(n, Math.floor((frame - DOT_START) / PER_DOT) + 1));
  return (
    <Background>
      <FadeUp delay={2} style={{ position: "absolute", left: 180, top: 90 }}>
        <div style={{ fontFamily: fonts.serif, fontSize: 52, fontWeight: 700 }}>It searches the design space</div>
      </FadeUp>
      <AbsoluteFill>
        <Heatmap />
        <div style={{ position: "absolute", left: PLOT.x, top: PLOT.y + PLOT.h + 18, width: PLOT.w, textAlign: "center", color: colors.dim, fontSize: 22 }}>
          thicker electrode &rarr;
        </div>
        <div style={{ position: "absolute", left: PLOT.x - 150, top: PLOT.y + PLOT.h / 2, width: 300, textAlign: "center", color: colors.dim, fontSize: 22, transform: "rotate(-90deg)", transformOrigin: "center" }}>
          more porous &uarr;
        </div>
        {data.trajectory.slice(0, visible).map((d, k) => (
          <Dot key={k} d={d} appear={DOT_START + k * PER_DOT} />
        ))}
        <Winner />
      </AbsoluteFill>
      <Readout />
    </Background>
  );
};
