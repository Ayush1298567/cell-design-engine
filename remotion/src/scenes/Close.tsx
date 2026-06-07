import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

export const Close: React.FC = () => (
  <Background>
    <AbsoluteFill style={{ justifyContent: "center", paddingLeft: 170, paddingRight: 170 }}>
      <FadeUp delay={4}>
        <div style={{ fontFamily: fonts.mono, letterSpacing: 9, color: colors.coral, fontSize: 24, textTransform: "uppercase" }}>
          Where it stands
        </div>
      </FadeUp>
      <FadeUp delay={14}>
        <div style={{ fontFamily: fonts.serif, fontSize: 72, fontWeight: 700, lineHeight: 1.1, marginTop: 22 }}>
          Built and running on
          <br />
          published cell data
        </div>
      </FadeUp>
      <FadeUp delay={30}>
        <div style={{ fontSize: 36, color: colors.dim, marginTop: 38, maxWidth: 1300, lineHeight: 1.5 }}>
          The next step is plugging in IBC&rsquo;s own cells and calibrating it, so the
          numbers move from the published cell to IBC&rsquo;s.
        </div>
      </FadeUp>
    </AbsoluteFill>
  </Background>
);
