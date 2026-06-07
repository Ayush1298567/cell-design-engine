import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

const Box: React.FC<{ delay: number; title: string; sub: string; accent?: boolean }> = ({ delay, title, sub, accent }) => (
  <FadeUp delay={delay} style={{ flex: 1 }}>
    <div
      style={{
        background: colors.panel,
        border: `1px solid ${accent ? colors.coral : colors.panelLine}`,
        borderRadius: 14,
        padding: "30px 26px",
        height: 230,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <div style={{ fontFamily: fonts.serif, fontSize: 38, fontWeight: 700, color: accent ? colors.amber : colors.text }}>{title}</div>
      <div style={{ fontSize: 24, color: colors.dim, marginTop: 14, lineHeight: 1.4 }}>{sub}</div>
    </div>
  </FadeUp>
);

const Arrow: React.FC<{ delay: number }> = ({ delay }) => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [delay, delay + 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return <div style={{ color: colors.dim, fontSize: 44, opacity: op, padding: "0 6px" }}>{"→"}</div>;
};

export const Architecture: React.FC = () => {
  const frame = useCurrentFrame();
  const loopOp = interpolate(frame, [80, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Background>
      <AbsoluteFill style={{ padding: "90px 120px" }}>
        <FadeUp delay={2}>
          <div style={{ fontFamily: fonts.serif, fontSize: 56, fontWeight: 700 }}>How it works</div>
        </FadeUp>

        <div style={{ display: "flex", alignItems: "center", marginTop: 110 }}>
          <Box delay={10} title="Requirement" sub="what the cell has to do" />
          <Arrow delay={22} />
          <Box delay={30} title="Optimizer" sub="picks which design to try next" accent />
          <Arrow delay={42} />
          <Box delay={50} title="Physics" sub="calculator + DFN simulation score each design" accent />
          <Arrow delay={62} />
          <Box delay={70} title="Ranked designs" sub="the best buildable options" />
        </div>

        <div style={{ position: "relative", height: 90, marginTop: 10, opacity: loopOp }}>
          <div style={{ position: "absolute", left: "37%", right: "23%", top: 30, height: 50, border: `2px solid ${colors.coral}`, borderTop: "none", borderRadius: "0 0 16px 16px" }} />
          <div style={{ position: "absolute", left: "59%", top: 72, color: colors.coral, fontSize: 26, fontFamily: fonts.mono }}>
            tries hundreds, learning from each result
          </div>
        </div>

        <FadeUp delay={120}>
          <div style={{ fontSize: 30, color: colors.dim, marginTop: 40, lineHeight: 1.5 }}>
            It runs end to end on its own. No simulation expert sits in the loop.
          </div>
        </FadeUp>
      </AbsoluteFill>
    </Background>
  );
};
