import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { Eyebrow } from "../components/Eyebrow";
import { Panel } from "../components/Panel";
import { colors, fonts, tokens } from "../theme";

const Node: React.FC<{ delay: number; title: string; sub: string; card?: boolean }> = ({ delay, title, sub, card }) => {
  const inner = (
    <>
      <div style={{ fontFamily: fonts.serif, fontSize: 34, fontWeight: 600, color: card ? colors.text : colors.dim }}>{title}</div>
      <div style={{ fontSize: 22, color: colors.body, marginTop: 12, lineHeight: 1.4 }}>{sub}</div>
    </>
  );
  return (
    <FadeUp delay={delay} style={{ flex: 1 }}>
      {card ? (
        <Panel accent style={{ padding: "28px 26px", height: 210, display: "flex", flexDirection: "column", justifyContent: "center" }}>{inner}</Panel>
      ) : (
        <div style={{ padding: "28px 10px", height: 210, display: "flex", flexDirection: "column", justifyContent: "center" }}>{inner}</div>
      )}
    </FadeUp>
  );
};

const Chevron: React.FC<{ delay: number }> = ({ delay }) => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [delay, delay + 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ opacity: op, padding: "0 14px", flexShrink: 0 }}>
      <div style={{ width: 14, height: 14, borderTop: `2px solid ${colors.coral}`, borderRight: `2px solid ${colors.coral}`, transform: "rotate(45deg)" }} />
    </div>
  );
};

export const Architecture: React.FC = () => {
  const frame = useCurrentFrame();
  const loopOp = interpolate(frame, [86, 116], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <Background>
      <AbsoluteFill style={{ paddingLeft: tokens.safeX, paddingRight: tokens.safeX, paddingTop: 140 }}>
        <FadeUp delay={2}>
          <Eyebrow>The workflow</Eyebrow>
        </FadeUp>
        <FadeUp delay={8}>
          <div style={{ fontFamily: fonts.serif, fontSize: 60, fontWeight: 600, letterSpacing: "-0.01em", marginTop: 16 }}>How it works</div>
        </FadeUp>

        <div style={{ display: "flex", alignItems: "center", marginTop: 90 }}>
          <Node delay={14} title="Requirement" sub="what the cell has to do" />
          <Chevron delay={24} />
          <Node delay={32} title="Optimizer" sub="picks which design to try next" card />
          <Chevron delay={44} />
          <Node delay={52} title="Physics" sub="calculator + DFN simulation score each design" card />
          <Chevron delay={64} />
          <Node delay={72} title="Ranked designs" sub="the best buildable options" />
        </div>

        <div style={{ position: "relative", height: 70, opacity: loopOp }}>
          <div style={{ position: "absolute", left: "37%", right: "23%", top: 14, height: 38, border: `1.5px solid ${colors.coralBorder}`, borderTop: "none", borderRadius: "0 0 14px 14px" }} />
          <div style={{ position: "absolute", left: 0, right: 0, top: 56, textAlign: "center", color: colors.coralLabel, fontStyle: "italic", fontSize: 24 }}>
            tries hundreds, learning from each result
          </div>
        </div>

        <FadeUp delay={120}>
          <div style={{ fontSize: 30, color: colors.body, marginTop: 56, lineHeight: 1.5 }}>
            It runs end to end on its own. No simulation expert sits in the loop.
          </div>
        </FadeUp>
      </AbsoluteFill>
    </Background>
  );
};
