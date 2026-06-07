import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { Eyebrow } from "../components/Eyebrow";
import { Panel } from "../components/Panel";
import { colors, fonts, tokens } from "../theme";
import data from "../demo_data.json";

const Card: React.FC<{ delay: number; tag: string; rate: string; por: number; energy: number; note: string }> = ({ delay, tag, rate, por, energy, note }) => (
  <FadeUp delay={delay} style={{ flex: 1 }}>
    <Panel style={{ padding: "38px 42px", height: 470 }}>
      <Eyebrow>{tag}</Eyebrow>
      <div style={{ fontSize: 30, color: colors.dim, marginTop: 14 }}>peak discharge {rate}</div>
      <div style={{ fontFamily: fonts.mono, fontSize: 150, fontWeight: 500, color: colors.amber, marginTop: 26, lineHeight: 1 }}>{(por * 100).toFixed(0)}%</div>
      <div style={{ fontSize: 28, color: colors.dim, marginTop: 6 }}>cathode porosity</div>
      <div style={{ fontSize: 34, fontFamily: fonts.serif, marginTop: 34 }}>{energy.toFixed(0)} Wh/kg</div>
      <div style={{ fontSize: 24, color: colors.body, marginTop: 16, lineHeight: 1.5 }}>{note}</div>
    </Panel>
  </FadeUp>
);

export const Generalize: React.FC = () => (
  <Background>
    <AbsoluteFill style={{ paddingLeft: tokens.safeX, paddingRight: tokens.safeX, paddingTop: 140 }}>
      <FadeUp delay={2}>
        <Eyebrow>It generalizes</Eyebrow>
      </FadeUp>
      <FadeUp delay={8}>
        <div style={{ fontFamily: fonts.serif, fontSize: 60, fontWeight: 600, letterSpacing: "-0.01em", marginTop: 16 }}>Same engine, different application</div>
      </FadeUp>
      <FadeUp delay={16}>
        <div style={{ fontSize: 26, color: colors.body, marginTop: 16, marginBottom: 42 }}>No retuning. The optimizer responds to the spec with a physically different design.</div>
      </FadeUp>
      <div style={{ display: "flex", gap: 56 }}>
        <Card delay={24} tag="Drone" rate={`${data.spec.spec_c_rate}C`} por={data.best.porosity} energy={data.best.specific_energy!} note="Balanced: holds rate while keeping the cell energy-dense." />
        <Card delay={36} tag="Power tool" rate={`${data.power.spec_c_rate}C`} por={data.power.best.porosity} energy={data.power.best.specific_energy!} note="Opens the electrode to survive the harder rate, trading some energy." />
      </div>
    </AbsoluteFill>
  </Background>
);
