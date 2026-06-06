import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";

const tiers = [
  { name: "Quote-grade", note: "calculator algebra", w: 1.0, c: colors.amber },
  { name: "Design-guidance", note: "calibrated DFN", w: 0.78, c: colors.green },
  { name: "Directional", note: "uncalibrated DFN (today)", w: 0.56, c: colors.cyan },
  { name: "Ground truth", note: "the pilot line", w: 0.34, c: colors.coral },
];

export const Close: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <Background>
      <AbsoluteFill style={{ padding: "90px 170px" }}>
        <FadeUp delay={2}>
          <div style={{ fontFamily: fonts.serif, fontSize: 56, fontWeight: 700 }}>Every number, labeled by trust</div>
        </FadeUp>

        <div style={{ marginTop: 50 }}>
          {tiers.map((t, k) => {
            const grow = interpolate(frame, [20 + k * 8, 50 + k * 8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return (
              <div key={k} style={{ display: "flex", alignItems: "center", marginTop: 22 }}>
                <div style={{ width: 360, fontSize: 32 }}>
                  <span style={{ color: colors.text }}>{t.name}</span>
                </div>
                <div style={{ flex: 1, height: 46, background: colors.panel, borderRadius: 8, overflow: "hidden" }}>
                  <div style={{ width: `${t.w * grow * 100}%`, height: "100%", background: t.c, borderRadius: 8 }} />
                </div>
                <div style={{ width: 360, fontSize: 26, color: colors.dim, paddingLeft: 24 }}>{t.note}</div>
              </div>
            );
          })}
        </div>

        <FadeUp delay={90} style={{ marginTop: 60 }}>
          <div style={{ fontSize: 34, color: colors.text, lineHeight: 1.5 }}>
            Directional today, on literature data. <span style={{ color: colors.amber }}>Design-guidance once calibrated on IBC&rsquo;s own cells</span> &mdash; the part that runs on data which never leaves IBC.
          </div>
        </FadeUp>

        <FadeUp delay={150}>
          <div style={{ fontFamily: fonts.serif, fontSize: 60, fontWeight: 700, marginTop: 70 }}>
            Validated. Demoable. <span style={{ color: colors.coral }}>Ready to calibrate.</span>
          </div>
        </FadeUp>
      </AbsoluteFill>
    </Background>
  );
};
