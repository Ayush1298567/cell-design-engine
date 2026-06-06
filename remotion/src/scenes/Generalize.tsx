import React from "react";
import { AbsoluteFill } from "remotion";
import { Background } from "../components/Background";
import { FadeUp } from "../components/FadeUp";
import { colors, fonts } from "../theme";
import data from "../demo_data.json";

const Card: React.FC<{ delay: number; tag: string; rate: string; por: number; energy: number; note: string }> = ({ delay, tag, rate, por, energy, note }) => (
  <FadeUp delay={delay} style={{ width: 680 }}>
    <div style={{ background: colors.panel, border: `1px solid ${colors.panelLine}`, borderRadius: 16, padding: "36px 40px", height: 520 }}>
      <div style={{ fontFamily: fonts.mono, letterSpacing: 6, color: colors.coral, fontSize: 22, textTransform: "uppercase" }}>{tag}</div>
      <div style={{ fontSize: 34, color: colors.dim, marginTop: 10 }}>peak discharge {rate}</div>
      <div style={{ fontFamily: fonts.mono, fontSize: 150, fontWeight: 700, color: colors.amber, marginTop: 30, lineHeight: 1 }}>
        {(por * 100).toFixed(0)}%
      </div>
      <div style={{ fontSize: 30, color: colors.dim, marginTop: 4 }}>cathode porosity</div>
      <div style={{ fontSize: 38, fontFamily: fonts.serif, marginTop: 40 }}>{energy.toFixed(0)} Wh/kg</div>
      <div style={{ fontSize: 26, color: colors.dim, marginTop: 18, lineHeight: 1.5 }}>{note}</div>
    </div>
  </FadeUp>
);

export const Generalize: React.FC = () => (
  <Background>
    <AbsoluteFill style={{ padding: "90px 170px" }}>
      <FadeUp delay={2}>
        <div style={{ fontFamily: fonts.serif, fontSize: 56, fontWeight: 700 }}>Same engine, different application</div>
      </FadeUp>
      <FadeUp delay={10}>
        <div style={{ fontSize: 26, color: colors.dim, marginTop: 14, marginBottom: 44 }}>
          No retuning. The optimizer responds to the spec with a physically different design.
        </div>
      </FadeUp>
      <div style={{ display: "flex", gap: 60, justifyContent: "center" }}>
        <Card
          delay={20}
          tag="Drone"
          rate={`${data.spec.spec_c_rate}C`}
          por={data.best.porosity}
          energy={data.best.specific_energy!}
          note="Balanced: holds rate while keeping the cell energy-dense."
        />
        <Card
          delay={34}
          tag="Power tool"
          rate={`${data.power.spec_c_rate}C`}
          por={data.power.best.porosity}
          energy={data.power.best.specific_energy!}
          note="Opens the electrode (more porous) to survive the harder rate, trading some energy."
        />
      </div>
    </AbsoluteFill>
  </Background>
);
