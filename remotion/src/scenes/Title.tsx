import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

export const Title: React.FC = () => (
  <Background>
    <AbsoluteFill style={{ justifyContent: "center", paddingLeft: 170 }}>
      <FadeUp delay={4}>
        <div style={{ fontFamily: fonts.mono, letterSpacing: 9, color: colors.coral, fontSize: 24, textTransform: "uppercase" }}>
          International Battery Company
        </div>
      </FadeUp>
      <FadeUp delay={12}>
        <div style={{ fontFamily: fonts.serif, fontSize: 118, fontWeight: 700, lineHeight: 1.02, marginTop: 20 }}>
          Custom Cell
          <br />
          Design Engine
        </div>
      </FadeUp>
      <FadeUp delay={26}>
        <div style={{ width: 340, height: 4, background: colors.coral, marginTop: 36, marginBottom: 32 }} />
      </FadeUp>
      <FadeUp delay={32}>
        <div style={{ fontSize: 36, color: colors.dim }}>Requirements in. Ranked, buildable cell designs out.</div>
      </FadeUp>
    </AbsoluteFill>
  </Background>
);
