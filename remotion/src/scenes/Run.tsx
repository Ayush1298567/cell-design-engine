import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";
import { Heatmap, Dot, Winner, Plot } from "../components/Heatmap";
import data from "../demo_data.json";

const PLOT: Plot = { x: 150, y: 330, w: 690, h: 540 };
const DOT_START = 120;
const PER_DOT = 14;
const N = data.trajectory.length;
const SEARCH_END = DOT_START + N * PER_DOT; // ~540
const STAR = SEARCH_END + 6;

const stages = [
  { name: "Intake", start: 10, end: 60, detail: "Parsed the requirement into a structured spec." },
  { name: "Strategy", start: 60, end: 110, detail: "Search plan: energy-first, inside the manufacturing envelope." },
  { name: "Search", start: 110, end: SEARCH_END, detail: "" },
  { name: "Analyze", start: SEARCH_END, end: SEARCH_END + 60, detail: "Improvement flattened. Stopping the search." },
  { name: "Report", start: SEARCH_END + 60, end: SEARCH_END + 110, detail: "Ranked the buildable designs." },
];
const REPORT_DONE = SEARCH_END + 110;

const StagePill: React.FC<{ name: string; status: "pending" | "active" | "done" }> = ({ name, status }) => {
  const frame = useCurrentFrame();
  const pulse = status === "active" ? 0.5 + 0.5 * Math.abs(Math.sin(frame / 8)) : 1;
  const border = status === "done" ? colors.green : status === "active" ? colors.coral : colors.panelLine;
  const text = status === "pending" ? colors.dim : colors.text;
  return (
    <div style={{ flex: 1, textAlign: "center" }}>
      <div style={{ display: "inline-block", background: colors.panel, border: `2px solid ${border}`, borderRadius: 10, padding: "14px 20px", minWidth: 200, opacity: status === "active" ? pulse : 1, boxShadow: status === "active" ? `0 0 18px ${colors.coral}55` : "none" }}>
        <span style={{ fontSize: 28, color: text, fontFamily: fonts.sans }}>
          {status === "done" ? "✓ " : ""}
          {name}
        </span>
      </div>
    </div>
  );
};

export const Run: React.FC = () => {
  const frame = useCurrentFrame();
  const visible = Math.max(0, Math.min(N, Math.floor((frame - DOT_START) / PER_DOT) + 1));
  let best = 0;
  for (let k = 0; k < visible; k++) {
    const d = data.trajectory[k];
    if (d.feasible && d.specific_energy && d.specific_energy > best) best = d.specific_energy;
  }

  const statusOf = (s: typeof stages[number]): "pending" | "active" | "done" =>
    frame >= s.end ? "done" : frame >= s.start ? "active" : "pending";
  const active = stages.find((s) => statusOf(s) === "active");
  const detail = active ? (active.name === "Search" ? `trial ${String(visible).padStart(2, "0")} / ${N}   ·   best so far ${best ? best.toFixed(0) : "..."} Wh/kg` : active.detail) : "Done.";

  return (
    <Background>
      <FadeUp delay={2} style={{ position: "absolute", left: 150, top: 64 }}>
        <div style={{ fontFamily: fonts.serif, fontSize: 48, fontWeight: 700 }}>
          Step 2 &middot; the engine runs <span style={{ fontFamily: fonts.mono, fontSize: 24, color: colors.coral }}>(sped up)</span>
        </div>
      </FadeUp>

      {/* stage tracker */}
      <div style={{ position: "absolute", left: 150, right: 100, top: 150, display: "flex", alignItems: "center" }}>
        {stages.map((s) => (
          <StagePill key={s.name} name={s.name} status={statusOf(s)} />
        ))}
      </div>

      {/* heatmap (the search) */}
      <AbsoluteFill>
        <Heatmap plot={PLOT} fadeStart={70} fadeEnd={110} />
        {data.trajectory.slice(0, visible).map((d, k) => (
          <Dot key={k} d={d} appear={DOT_START + k * PER_DOT} plot={PLOT} />
        ))}
        <Winner starFrame={STAR} plot={PLOT} />
        <div style={{ position: "absolute", left: PLOT.x, top: PLOT.y + PLOT.h + 16, width: PLOT.w, textAlign: "center", color: colors.dim, fontSize: 20 }}>thicker electrode &rarr;</div>
      </AbsoluteFill>

      {/* status panel */}
      <div style={{ position: "absolute", left: 930, top: 340, width: 840 }}>
        <div style={{ fontFamily: fonts.mono, letterSpacing: 5, color: colors.coral, fontSize: 20, textTransform: "uppercase" }}>
          {active ? active.name : "Complete"}
        </div>
        <div style={{ fontSize: 34, color: colors.text, marginTop: 14, lineHeight: 1.4, fontFamily: active && active.name === "Search" ? fonts.mono : fonts.sans, minHeight: 100 }}>
          {detail}
        </div>

        {frame >= REPORT_DONE && (
          <FadeUp delay={REPORT_DONE + 4} style={{ marginTop: 40 }}>
            <div style={{ background: colors.panel, border: `1px solid ${colors.coral}`, borderRadius: 14, padding: "26px 30px" }}>
              <div style={{ fontFamily: fonts.mono, letterSpacing: 5, color: colors.coral, fontSize: 18, textTransform: "uppercase" }}>Recommended design</div>
              <div style={{ fontSize: 46, fontFamily: fonts.serif, color: colors.amber, marginTop: 10 }}>
                {data.best.specific_energy?.toFixed(0)} Wh/kg &middot; {data.best.capacity?.toFixed(1)} Ah
              </div>
              <div style={{ fontSize: 26, color: colors.dim, marginTop: 8 }}>
                {data.best.thickness.toFixed(0)} &micro;m cathode, {(data.best.porosity * 100).toFixed(0)}% porosity &middot; {data.ranked.length} designs ranked
              </div>
            </div>
          </FadeUp>
        )}
      </div>

      {/* real-run grounding */}
      <div style={{ position: "absolute", left: 150, bottom: 50, fontFamily: fonts.mono, fontSize: 22, color: colors.dim }}>
        <span style={{ color: colors.coral }}>$ </span>python run_demo.py {frame >= REPORT_DONE ? "  ·  done" : "  ·  running pipeline..."}
      </div>
    </Background>
  );
};
