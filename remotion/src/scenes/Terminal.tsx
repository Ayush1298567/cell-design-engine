import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

type Line = { k: "cmd" | "out" | "ok" | "gap"; t?: string };

const lines: Line[] = [
  { k: "cmd", t: "pytest" },
  { k: "ok", t: "47 passed in 90s" },
  { k: "gap" },
  { k: "cmd", t: "python run_demo.py" },
  { k: "out", t: "Running optimization pipeline..." },
  { k: "out", t: "  searching designs:   trial 30 / 30" },
  { k: "out", t: "  evaluating design-space landscape..." },
  { k: "gap" },
  { k: "ok", t: "Recommended design:  270 Wh/kg,  24.5 Ah  at 3C" },
  { k: "out", t: "  27 of 30 designs met every target" },
  { k: "out", t: "  saved:  design_space.png   run_report.md" },
];

const PER_LINE = 26;
const START = 30;

const Row: React.FC<{ line: Line; idx: number }> = ({ line, idx }) => {
  const frame = useCurrentFrame();
  const appear = START + idx * PER_LINE;
  const op = interpolate(frame, [appear, appear + 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  if (line.k === "gap") return <div style={{ height: 24 }} />;
  const color = line.k === "cmd" ? colors.text : line.k === "ok" ? colors.green : colors.dim;
  return (
    <div style={{ opacity: op, fontFamily: fonts.mono, fontSize: 30, color, lineHeight: 1.7, whiteSpace: "pre" }}>
      {line.k === "cmd" ? <span style={{ color: colors.coral }}>$ </span> : "  "}
      {line.t}
    </div>
  );
};

export const Terminal: React.FC = () => {
  const frame = useCurrentFrame();
  const cursorOn = Math.floor(frame / 15) % 2 === 0;
  const visible = Math.min(lines.length, Math.max(0, Math.floor((frame - START) / PER_LINE) + 1));
  return (
    <Background>
      <AbsoluteFill style={{ padding: "90px 170px" }}>
        <FadeUp delay={2}>
          <div style={{ fontFamily: fonts.serif, fontSize: 56, fontWeight: 700 }}>It runs today</div>
        </FadeUp>
        <FadeUp delay={10}>
          <div style={{ fontSize: 26, color: colors.dim, marginTop: 14 }}>The full pipeline, tested and running on an ordinary laptop.</div>
        </FadeUp>

        <FadeUp delay={8} style={{ marginTop: 40 }}>
          <div style={{ background: "#0c0708", border: `1px solid ${colors.panelLine}`, borderRadius: 14, overflow: "hidden" }}>
            <div style={{ display: "flex", gap: 10, padding: "16px 22px", borderBottom: `1px solid ${colors.panelLine}` }}>
              <span style={{ width: 14, height: 14, borderRadius: "50%", background: "#ff5f57" }} />
              <span style={{ width: 14, height: 14, borderRadius: "50%", background: "#febc2e" }} />
              <span style={{ width: 14, height: 14, borderRadius: "50%", background: "#28c840" }} />
              <span style={{ marginLeft: 16, fontFamily: fonts.mono, fontSize: 22, color: colors.dim }}>cell-design-engine</span>
            </div>
            <div style={{ padding: "30px 34px", minHeight: 520 }}>
              {lines.slice(0, visible).map((l, i) => (
                <Row key={i} line={l} idx={i} />
              ))}
              <span style={{ fontFamily: fonts.mono, fontSize: 30, color: colors.coral, opacity: cursorOn ? 1 : 0 }}>{"▋"}</span>
            </div>
          </div>
        </FadeUp>
      </AbsoluteFill>
    </Background>
  );
};
