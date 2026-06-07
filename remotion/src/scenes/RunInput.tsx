import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

const TEXT =
  "We build agricultural drones. Flights are about 45 minutes, the motors pull hard at takeoff, it has to fit the existing battery bay, and it should be as light as possible.";

const START = 24;
const CPS = 2.4; // characters per frame

export const RunInput: React.FC = () => {
  const frame = useCurrentFrame();
  const shown = Math.max(0, Math.min(TEXT.length, Math.floor((frame - START) * CPS)));
  const typed = TEXT.slice(0, shown);
  const done = shown >= TEXT.length;
  const cursorOn = Math.floor(frame / 14) % 2 === 0;
  const runOp = interpolate(frame, [START + TEXT.length / CPS + 12, START + TEXT.length / CPS + 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <Background>
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 200px" }}>
        <FadeUp delay={2}>
          <div style={{ fontFamily: fonts.mono, letterSpacing: 6, color: colors.coral, fontSize: 22, textTransform: "uppercase" }}>
            Step 1 &middot; the requirement, in plain language
          </div>
        </FadeUp>
        <FadeUp delay={10} style={{ marginTop: 26 }}>
          <div style={{ background: colors.panel, border: `1px solid ${colors.panelLine}`, borderRadius: 16, padding: "44px 50px", minHeight: 280 }}>
            <div style={{ fontSize: 44, lineHeight: 1.5, color: colors.text, fontFamily: fonts.sans }}>
              {typed}
              <span style={{ opacity: cursorOn && !done ? 1 : 0, color: colors.coral }}>{"▋"}</span>
            </div>
          </div>
        </FadeUp>
        <div style={{ marginTop: 34, opacity: runOp, display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ background: colors.coral, borderRadius: 10, padding: "16px 30px", fontSize: 28, fontFamily: fonts.sans, color: "#1a0a0a", fontWeight: 700 }}>
            Run the engine
          </div>
          <div style={{ fontFamily: fonts.mono, fontSize: 24, color: colors.dim }}>no battery jargon required</div>
        </div>
      </AbsoluteFill>
    </Background>
  );
};
