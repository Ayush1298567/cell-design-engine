import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";
import data from "../demo_data.json";

const cols = "60px 1.1fr 1.1fr 1.2fr 1fr 1fr 1fr";

const Cell: React.FC<{ children: React.ReactNode; color?: string; mono?: boolean; align?: string }> = ({ children, color, mono, align }) => (
  <div style={{ fontSize: 30, color: color ?? colors.text, fontFamily: mono ? fonts.mono : fonts.sans, textAlign: (align as any) ?? "right", padding: "16px 18px" }}>
    {children}
  </div>
);

export const Results: React.FC = () => {
  const rows = data.ranked.slice(0, 5);
  return (
    <Background>
      <AbsoluteFill style={{ padding: "90px 170px" }}>
        <FadeUp delay={2}>
          <div style={{ fontFamily: fonts.serif, fontSize: 56, fontWeight: 700 }}>Ranked, buildable designs</div>
        </FadeUp>
        <FadeUp delay={10}>
          <div style={{ fontSize: 26, color: colors.dim, marginTop: 14, marginBottom: 30 }}>
            One recommendation plus distinct alternatives that trade energy for rate and thermal margin.
          </div>
        </FadeUp>

        <FadeUp delay={16}>
          <div style={{ display: "grid", gridTemplateColumns: cols, borderBottom: `1px solid ${colors.panelLine}`, paddingBottom: 6 }}>
            <Cell color={colors.dim} align="center">#</Cell>
            <Cell color={colors.dim}>cathode µm</Cell>
            <Cell color={colors.dim}>porosity</Cell>
            <Cell color={colors.amber}>Wh/kg ¹</Cell>
            <Cell color={colors.amber}>Ah ¹</Cell>
            <Cell color={colors.cyan}>rate ³</Cell>
            <Cell color={colors.cyan}>ΔT °C ³</Cell>
          </div>
        </FadeUp>

        {rows.map((r, k) => (
          <FadeUp key={k} delay={28 + k * 12}>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: cols,
                background: k === 0 ? "rgba(255,90,105,0.10)" : "transparent",
                border: k === 0 ? `1px solid ${colors.coral}` : "1px solid transparent",
                borderRadius: 10,
                marginTop: 6,
              }}
            >
              <Cell mono color={k === 0 ? colors.coral : colors.dim} align="center">{k + 1}</Cell>
              <Cell mono>{r.thickness?.toFixed(0)}</Cell>
              <Cell mono>{(r.porosity! * 100).toFixed(0)}%</Cell>
              <Cell mono color={colors.amber}>{r.specific_energy?.toFixed(0)}</Cell>
              <Cell mono color={colors.amber}>{r.capacity?.toFixed(1)}</Cell>
              <Cell mono color={colors.cyan}>{r.rate?.toFixed(2)}</Cell>
              <Cell mono color={colors.cyan}>{r.temp != null ? r.temp.toFixed(0) : ">lim"}</Cell>
            </div>
          </FadeUp>
        ))}

        <FadeUp delay={28 + rows.length * 12 + 10}>
          <div style={{ fontSize: 24, color: colors.dim, marginTop: 40, lineHeight: 1.5 }}>
            <span style={{ color: colors.amber }}>¹ tier-1, quote-grade</span> (calculator algebra) ·{" "}
            <span style={{ color: colors.cyan }}>³ tier-3, directional</span> (uncalibrated DFN). Calibration on IBC cells makes the directional numbers design-guidance grade.
          </div>
        </FadeUp>
      </AbsoluteFill>
    </Background>
  );
};
