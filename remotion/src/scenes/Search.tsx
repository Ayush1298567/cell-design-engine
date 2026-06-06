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

const DOT_START = 120;
const PER_DOT = Math.max(7, Math.floor(330 / data.trajectory.length));
const STAR = DOT_START + data.trajectory.length * PER_DOT + 18;

const Heatmap: React.FC = () => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [40, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cells: React.ReactNode[] = [];
  for (let i = 0; i < nPor; i++) {
    for (let j = 0; j < nThk; j++) {
      const e = data.grid.energy[i][j];
      const feas = data.grid.feasible[i][j] === 1;
      if (e == null) continue;
      const t = (e - minE) / (maxE - minE || 1);
      const base = viridis(t);
      const fill = feas ? rgb(base, 1) : rgb([base[0] * 0.35, base[1] * 0.35, base[2] * 0.35], 1);
      cells.push(
        <div
          key={`${i}-${j}`}
          style={{
            position: "absolute",
            left: sx(thks[j]) - cellW / 2,
            top: sy(pors[i]) - cellH / 2,
            width: cellW + 1,
            height: cellH + 1,
            background: fill,
          }}
        />
      );
    }
  }
  return <div style={{ opacity: op }}>{cells}</div>;
};

const Dot: React.FC<{ d: any; appear: number }> = ({ d, appear }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - appear, fps, config: { damping: 14, stiffness: 200 } });
  if (frame < appear) return null;
  const r = interpolate(s, [0, 1], [0, d.feasible ? 9 : 6]);
  return (
    <div
      style={{
        position: "absolute",
        left: sx(d.thickness) - r,
        top: sy(d.porosity) - r,
        width: r * 2,
        height: r * 2,
        borderRadius: "50%",
        background: d.feasible ? colors.cyan : "transparent",
        border: d.feasible ? `2px solid #ffffff` : `2px solid ${colors.dim}`,
        boxShadow: d.feasible ? `0 0 12px ${colors.cyan}` : "none",
        opacity: d.feasible ? 0.95 : 0.5,
      }}
    />
  );
};

const Axis: React.FC = () => (
  <>
    <div style={{ position: "absolute", left: PLOT.x, top: PLOT.y + PLOT.h + 18, width: PLOT.w, textAlign: "center", color: colors.dim, fontSize: 22 }}>
      Cathode thickness  ({bounds.thk[0]}&ndash;{bounds.thk[1]} &micro;m)
    </div>
    <div style={{ position: "absolute", left: PLOT.x - 150, top: PLOT.y + PLOT.h / 2, width: 300, textAlign: "center", color: colors.dim, fontSize: 22, transform: "rotate(-90deg)", transformOrigin: "center" }}>
      Cathode porosity
    </div>
  </>
);

const SpecCard: React.FC = () => {
  const t = data.spec.targets;
  const row = (label: string, val: string) => (
    <div style={{ display: "flex", justifyContent: "space-between", fontSize: 28, marginTop: 14 }}>
      <span style={{ color: colors.dim }}>{label}</span>
      <span style={{ fontFamily: fonts.mono, color: colors.text }}>{val}</span>
    </div>
  );
  return (
    <FadeUp delay={10} style={{ position: "absolute", left: 1130, top: 230, width: 620 }}>
      <div style={{ background: colors.panel, border: `1px solid ${colors.panelLine}`, borderRadius: 14, padding: "26px 30px" }}>
        <div style={{ fontFamily: fonts.mono, letterSpacing: 6, color: colors.coral, fontSize: 20, textTransform: "uppercase" }}>Requirement &middot; agricultural drone</div>
        <div style={{ fontSize: 34, fontFamily: fonts.serif, marginTop: 8, marginBottom: 8 }}>Peak discharge {data.spec.spec_c_rate}C</div>
        {row("specific energy", `≥ ${t.min_specific_energy_Wh_kg} Wh/kg`)}
        {row("rate capability", `≥ ${t.min_rate_capability}`)}
        {row("temperature rise", `≤ ${t.max_temp_rise_C} °C`)}
      </div>
    </FadeUp>
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
    <FadeUp delay={60} style={{ position: "absolute", left: 1130, top: 560, width: 620 }}>
      <div style={{ fontFamily: fonts.mono, fontSize: 30, color: colors.dim }}>
        trial <span style={{ color: colors.text }}>{String(visible).padStart(2, "0")}</span> / {n}
      </div>
      <div style={{ fontFamily: fonts.mono, fontSize: 30, color: colors.dim, marginTop: 14 }}>
        best feasible <span style={{ color: colors.cyan }}>{best ? best.toFixed(0) : "—"}</span> Wh/kg
      </div>
      <div style={{ fontSize: 24, color: colors.dim, marginTop: 28, lineHeight: 1.5 }}>
        Bayesian optimization over a validated DFN model. Every trial is informed by all prior trials.
      </div>
    </FadeUp>
  );
};

const Winner: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < STAR) return null;
  const s = spring({ frame: frame - STAR, fps, config: { damping: 12 } });
  const scale = interpolate(s, [0, 1], [0, 1]);
  const x = sx(data.best.thickness);
  const y = sy(data.best.porosity);
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: x - 26,
          top: y - 26,
          width: 52,
          height: 52,
          transform: `scale(${scale})`,
          color: "#ffffff",
          fontSize: 52,
          lineHeight: "52px",
          textAlign: "center",
          textShadow: `0 0 16px ${colors.coral}`,
        }}
      >
        {"★"}
      </div>
      <FadeUp delay={STAR + 10} style={{ position: "absolute", left: 1130, top: 760, width: 620 }}>
        <div style={{ background: colors.panel, border: `1px solid ${colors.coral}`, borderRadius: 14, padding: "22px 28px" }}>
          <div style={{ fontFamily: fonts.mono, letterSpacing: 5, color: colors.coral, fontSize: 18, textTransform: "uppercase" }}>Recommended design</div>
          <div style={{ fontSize: 30, marginTop: 10 }}>
            <span style={{ fontFamily: fonts.mono }}>{data.best.thickness.toFixed(0)} &micro;m</span> cathode,{" "}
            <span style={{ fontFamily: fonts.mono }}>{(data.best.porosity * 100).toFixed(0)}%</span> porosity
          </div>
          <div style={{ fontSize: 40, fontFamily: fonts.serif, color: colors.amber, marginTop: 8 }}>
            {data.best.specific_energy?.toFixed(0)} Wh/kg &middot; {data.best.capacity?.toFixed(1)} Ah
          </div>
        </div>
      </FadeUp>
    </>
  );
};

export const Search: React.FC = () => {
  const frame = useCurrentFrame();
  const n = data.trajectory.length;
  const visible = Math.max(0, Math.min(n, Math.floor((frame - DOT_START) / PER_DOT) + 1));
  return (
    <Background>
      <FadeUp delay={2} style={{ position: "absolute", left: 180, top: 90 }}>
        <div style={{ fontFamily: fonts.serif, fontSize: 52, fontWeight: 700 }}>Searching the design space</div>
      </FadeUp>
      <AbsoluteFill>
        <Heatmap />
        <Axis />
        {data.trajectory.slice(0, visible).map((d, k) => (
          <Dot key={k} d={d} appear={DOT_START + k * PER_DOT} />
        ))}
        <Winner />
      </AbsoluteFill>
      <SpecCard />
      <Readout />
    </Background>
  );
};
