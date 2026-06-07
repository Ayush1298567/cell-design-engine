import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { Eyebrow } from "../components/Eyebrow";
import { Panel } from "../components/Panel";
import { colors, fonts, tokens } from "../theme";

const TEXT =
  "We build agricultural drones. Flights are about 45 minutes, the motors pull hard at takeoff, it has to fit the existing battery bay, and it should be as light as possible.";

const START = 24;
const CPS = 2.4;

export const RunInput: React.FC = () => {
  const frame = useCurrentFrame();
  const shown = Math.max(0, Math.min(TEXT.length, Math.floor((frame - START) * CPS)));
  const typed = TEXT.slice(0, shown);
  const done = shown >= TEXT.length;
  const cursorOn = Math.floor(frame / 14) % 2 === 0;
  const doneFrame = START + TEXT.length / CPS;
  const runOp = interpolate(frame, [doneFrame + 12, doneFrame + 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <Background>
      <AbsoluteFill style={{ justifyContent: "center", paddingLeft: tokens.safeX, paddingRight: tokens.safeX }}>
        <FadeUp delay={2}>
          <Eyebrow>Step 1 &middot; the requirement, in plain language</Eyebrow>
        </FadeUp>
        <FadeUp delay={10} style={{ marginTop: 28 }}>
          <Panel style={{ padding: "48px 54px", minHeight: 300 }}>
            <div style={{ fontSize: 46, lineHeight: 1.5, color: colors.text }}>
              {typed}
              <span style={{ opacity: cursorOn && !done ? 1 : 0, color: colors.coral }}>{"▋"}</span>
            </div>
          </Panel>
        </FadeUp>
        <div style={{ marginTop: 38, opacity: runOp, display: "flex", alignItems: "center", gap: 20 }}>
          <div style={{ background: colors.coral, borderRadius: 12, padding: "18px 34px", fontSize: 28, fontWeight: 600, color: "#1a0a0a" }}>Run the engine</div>
          <div style={{ fontFamily: fonts.mono, fontSize: 22, color: colors.dim }}>no battery jargon required</div>
        </div>
      </AbsoluteFill>
    </Background>
  );
};
