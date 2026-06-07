import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { Eyebrow } from "../components/Eyebrow";
import { Panel } from "../components/Panel";
import { colors, fonts, tokens } from "../theme";
import { Heatmap, Dot, Winner, Plot } from "../components/Heatmap";
import data from "../demo_data.json";

const PLOT: Plot = { x: 160, y: 372, w: 660, h: 500 };
const DOT_START = 120;
const PER_DOT = 14;
const N = data.trajectory.length;
const SEARCH_END = DOT_START + N * PER_DOT;
const STAR = SEARCH_END + 6;

const stages = [
  { name: "Intake", start: 10, end: 60, detail: "Parsed the requirement into a structured spec." },
  { name: "Strategy", start: 60, end: 110, detail: "Search plan: energy-first, inside the manufacturing envelope." },
  { name: "Search", start: 110, end: SEARCH_END, detail: "" },
  { name: "Analyze", start: SEARCH_END, end: SEARCH_END + 60, detail: "Improvement flattened. Stopping the search." },
  { name: "Report", start: SEARCH_END + 60, end: SEARCH_END + 110, detail: "Ranked the buildable designs." },
];
const REPORT_DONE = SEARCH_END + 110;

type Status = "pending" | "active" | "done";

const StepDot: React.FC<{ status: Status }> = ({ status }) => {
  const frame = useCurrentFrame();
  if (status === "done") return <div style={{ width: 14, height: 14, borderRadius: "50%", background: colors.coral }} />;
  if (status === "active") {
    const pulse = 0.45 + 0.55 * Math.abs(Math.sin(frame / 9));
    return <div style={{ width: 14, height: 14, borderRadius: "50%", border: `2px solid ${colors.coral}`, boxShadow: `0 0 ${10 * pulse}px ${colors.coral}` }} />;
  }
  return <div style={{ width: 10, height: 10, borderRadius: "50%", background: "rgba(255,255,255,0.20)" }} />;
};

const Stepper: React.FC<{ statusOf: (s: typeof stages[number]) => Status }> = ({ statusOf }) => (
  <div style={{ position: "absolute", left: tokens.safeX, right: tokens.safeX, top: 224, height: 70 }}>
    <div style={{ position: "absolute", left: "10%", right: "10%", top: 6, height: 1, background: colors.hairline }} />
    <div style={{ display: "flex" }}>
      {stages.map((s) => {
        const st = statusOf(s);
        return (
          <div key={s.name} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center" }}>
            <StepDot status={st} />
            <div style={{ marginTop: 16, fontFamily: fonts.mono, fontSize: 16, letterSpacing: "0.18em", textTransform: "uppercase", color: st === "pending" ? colors.faint : colors.text }}>
              {s.name}
            </div>
          </div>
        );
      })}
    </div>
  </div>
);

export const Run: React.FC = () => {
  const frame = useCurrentFrame();
  const visible = Math.max(0, Math.min(N, Math.floor((frame - DOT_START) / PER_DOT) + 1));
  let best = 0;
  for (let k = 0; k < visible; k++) {
    const d = data.trajectory[k];
    if (d.feasible && d.specific_energy && d.specific_energy > best) best = d.specific_energy;
  }
  const statusOf = (s: typeof stages[number]): Status => (frame >= s.end ? "done" : frame >= s.start ? "active" : "pending");
  const active = stages.find((s) => statusOf(s) === "active");
  const isSearch = active?.name === "Search";

  return (
    <Background>
      <FadeUp delay={2} style={{ position: "absolute", left: tokens.safeX, top: 100, display: "flex", alignItems: "center", gap: 22 }}>
        <div style={{ fontFamily: fonts.serif, fontSize: 60, fontWeight: 600, letterSpacing: "-0.01em" }}>Step 2 &middot; the engine runs</div>
        <div style={{ fontFamily: fonts.mono, fontSize: 16, letterSpacing: "0.18em", color: colors.coralLabel, border: `1px solid ${colors.coralBorder}`, borderRadius: 999, padding: "6px 14px" }}>SPED UP</div>
      </FadeUp>

      <Stepper statusOf={statusOf} />

      <AbsoluteFill>
        <Heatmap plot={PLOT} fadeStart={80} fadeEnd={120} />
        {data.trajectory.slice(0, visible).map((d, k) => (
          <Dot key={k} d={d} appear={DOT_START + k * PER_DOT} plot={PLOT} />
        ))}
        <Winner starFrame={STAR} plot={PLOT} />
        <div style={{ position: "absolute", left: PLOT.x, top: PLOT.y + PLOT.h + 18, width: PLOT.w, textAlign: "center", color: colors.dim, fontSize: 20 }}>thicker electrode &rarr;</div>
      </AbsoluteFill>

      <div style={{ position: "absolute", left: 930, top: 392, width: 830 }}>
        <Eyebrow>{active ? active.name : "Complete"}</Eyebrow>

        {isSearch ? (
          <div style={{ marginTop: 18 }}>
            <div style={{ fontFamily: fonts.mono, fontSize: 70, fontWeight: 500, color: colors.amber }}>
              {best ? best.toFixed(0) : "..."} <span style={{ fontSize: 34, color: colors.body }}>Wh/kg</span>
            </div>
            <div style={{ fontFamily: fonts.mono, fontSize: 28, color: colors.dim, marginTop: 10 }}>best so far &middot; trial {String(visible).padStart(2, "0")} / {N}</div>
          </div>
        ) : (
          <div style={{ fontSize: 34, color: colors.text, marginTop: 16, lineHeight: 1.45, minHeight: 100 }}>{active ? active.detail : "Done."}</div>
        )}

        {frame >= REPORT_DONE && (
          <FadeUp delay={REPORT_DONE + 4} style={{ marginTop: 44 }}>
            <Panel accent style={{ padding: "30px 34px" }}>
              <Eyebrow>Recommended design</Eyebrow>
              <div style={{ fontFamily: fonts.mono, fontSize: 56, fontWeight: 500, color: colors.amber, marginTop: 14 }}>
                {data.best.specific_energy?.toFixed(0)} <span style={{ color: colors.text }}>Wh/kg</span> <span style={{ color: colors.body, fontSize: 38 }}>&middot; {data.best.capacity?.toFixed(1)} Ah</span>
              </div>
              <div style={{ fontSize: 26, color: colors.dim, marginTop: 12 }}>
                {data.best.thickness.toFixed(0)} &micro;m cathode, {(data.best.porosity * 100).toFixed(0)}% porosity &middot; {data.ranked.length} designs ranked
              </div>
            </Panel>
          </FadeUp>
        )}

        <div style={{ position: "absolute", top: 470, fontFamily: fonts.mono, fontSize: 20, color: colors.faint }}>
          <span style={{ color: colors.coralLabel }}>$ </span>python run_demo.py {frame >= REPORT_DONE ? "· done" : "· running..."}
        </div>
      </div>
    </Background>
  );
};
