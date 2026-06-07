import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { Eyebrow } from "../components/Eyebrow";
import { colors, fonts, tokens } from "../theme";

export const Close: React.FC = () => (
  <Background>
    <div style={{ position: "absolute", right: tokens.safeX, bottom: 150, fontFamily: fonts.serif, fontSize: 240, fontWeight: 600, color: "rgba(255,255,255,0.035)", lineHeight: 1 }}>06</div>
    <AbsoluteFill style={{ justifyContent: "center", paddingLeft: tokens.safeX, paddingRight: tokens.safeX }}>
      <FadeUp delay={4}>
        <Eyebrow>Where it stands</Eyebrow>
      </FadeUp>
      <FadeUp delay={12}>
        <div style={{ fontFamily: fonts.serif, fontSize: 78, fontWeight: 600, lineHeight: 1.05, letterSpacing: "-0.01em", marginTop: 22, maxWidth: 1180 }}>
          Built and running on published cell data
        </div>
      </FadeUp>
      <FadeUp delay={26}>
        <div style={{ fontSize: 34, color: colors.body, marginTop: 28, maxWidth: 1040, lineHeight: 1.55 }}>
          The next step is plugging in IBC&rsquo;s own cells and calibrating it, so the numbers move from the published cell to IBC&rsquo;s.
        </div>
      </FadeUp>
    </AbsoluteFill>
  </Background>
);
