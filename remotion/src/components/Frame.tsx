import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { colors, fonts, tokens } from "../theme";

export const Frame: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const progress = Math.min(1, frame / durationInFrames);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: "radial-gradient(125% 95% at 50% 38%, transparent 56%, rgba(0,0,0,0.6) 100%)" }} />

      <div style={{ position: "absolute", top: 56, left: tokens.safeX, display: "flex", alignItems: "center", gap: 14 }}>
        <div style={{ width: 16, height: 16, background: colors.coral, borderRadius: 4 }} />
        <div style={{ fontFamily: fonts.mono, fontSize: 17, letterSpacing: 4, color: colors.dim, textTransform: "uppercase" }}>
          International Battery Company
        </div>
      </div>

      <div style={{ position: "absolute", bottom: 56, left: tokens.safeX, width: 360, height: 3, background: "rgba(255,255,255,0.10)", borderRadius: 2 }}>
        <div style={{ width: `${progress * 100}%`, height: "100%", background: colors.coral, borderRadius: 2 }} />
      </div>
      <div style={{ position: "absolute", bottom: 50, right: tokens.safeX, fontFamily: fonts.mono, fontSize: 17, letterSpacing: 3, color: colors.faint, textTransform: "uppercase" }}>
        Custom Cell Design Engine
      </div>
    </AbsoluteFill>
  );
};
