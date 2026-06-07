import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

export const Intro: React.FC = () => (
  <Background>
    <AbsoluteFill style={{ justifyContent: "center", paddingLeft: 170, paddingRight: 170 }}>
      <FadeUp delay={4}>
        <div style={{ fontFamily: fonts.mono, letterSpacing: 9, color: colors.coral, fontSize: 24, textTransform: "uppercase" }}>
          What we built
        </div>
      </FadeUp>
      <FadeUp delay={12}>
        <div style={{ fontFamily: fonts.serif, fontSize: 100, fontWeight: 700, lineHeight: 1.05, marginTop: 20 }}>
          An engine that designs
          <br />
          battery cells
        </div>
      </FadeUp>
      <FadeUp delay={28}>
        <div style={{ fontSize: 36, color: colors.dim, marginTop: 36, maxWidth: 1300, lineHeight: 1.5 }}>
          You give it a requirement. It searches the possible cell designs with a physics
          simulation and hands back the best ones to build.
        </div>
      </FadeUp>
    </AbsoluteFill>
  </Background>
);
