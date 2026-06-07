import React from "react";
import { AbsoluteFill } from "remotion";
import { Grain } from "./components/Grain";
import { colors, fonts, tokens } from "./theme";

const Chip: React.FC<{ label: string; sub?: string; tone: "agent" | "core" | "human" | "data"; accent?: boolean }> = ({ label, sub, tone, accent }) => {
  const fill = tone === "agent" ? "rgba(255,157,108,0.14)" : tone === "core" ? "rgba(255,255,255,0.04)" : tone === "human" ? "rgba(255,255,255,0.06)" : "rgba(255,255,255,0.03)";
  const border = accent ? colors.coral : tone === "agent" ? "rgba(255,157,108,0.5)" : colors.hairline;
  return (
    <div style={{ flex: 1, background: fill, border: `1px solid ${border}`, borderRadius: 12, padding: "16px 18px", boxShadow: accent ? tokens.glow : "none" }}>
      <div style={{ fontSize: 25, fontWeight: 600, color: colors.text }}>{label}</div>
      {sub ? <div style={{ fontSize: 17, color: colors.dim, marginTop: 6, lineHeight: 1.3 }}>{sub}</div> : null}
    </div>
  );
};

const Lane: React.FC<{ y: number; label: string; children: React.ReactNode }> = ({ y, label, children }) => (
  <div style={{ position: "absolute", left: 80, right: 120, top: y }}>
    <div style={{ fontFamily: fonts.mono, fontSize: 16, letterSpacing: "0.2em", color: colors.coralLabel, textTransform: "uppercase", marginBottom: 12 }}>{label}</div>
    <div style={{ display: "flex", gap: 18 }}>{children}</div>
  </div>
);

export const ArchDiagram: React.FC = () => (
  <AbsoluteFill style={{ background: `radial-gradient(145% 120% at 50% -12%, ${colors.bg1} 0%, ${colors.bg0} 58%)`, fontFamily: fonts.sans, color: colors.text }}>
    <Grain />

    <div style={{ position: "absolute", top: 64, left: 80 }}>
      <div style={{ fontFamily: fonts.mono, fontSize: 17, letterSpacing: "0.22em", color: colors.coralLabel, textTransform: "uppercase" }}>Custom Cell Design Engine</div>
      <div style={{ fontFamily: fonts.serif, fontSize: 60, fontWeight: 600, letterSpacing: "-0.01em", marginTop: 12 }}>System architecture</div>
    </div>

    <Lane y={230} label="People">
      <Chip tone="human" label="Customer RFQ" sub="application + targets, in plain language" />
      <Chip tone="human" label="Engineer reviews the spec" sub="human-in-the-loop: approve before the run" accent />
      <Chip tone="human" label="Engineers build & test" sub="the top designs (unchanged core work)" />
    </Lane>

    <Lane y={420} label="LLM agents · bounded judgment, validated JSON (orchestrates, does not do the science)">
      <Chip tone="agent" label="Intake" sub="requirement → spec" />
      <Chip tone="agent" label="Strategy" sub="search plan" />
      <Chip tone="agent" label="Analysis" sub="progress / stop" />
      <Chip tone="agent" label="Evaluation" sub="cost, safety, mfg" />
      <Chip tone="agent" label="Report" sub="ranked write-up" />
    </Lane>

    <Lane y={610} label="Orchestrator">
      <Chip tone="core" label="Deterministic state machine" sub="runs the pipeline, validates every agent answer, rejects out-of-bounds ones" />
    </Lane>

    <Lane y={760} label="Tools · the math and physics">
      <Chip tone="core" label="Validation gate" sub="screen candidates" />
      <Chip tone="core" label="Bayesian optimizer" sub="picks next design" />
      <Chip tone="core" label="Cell calculator" sub="tier-1 quote-grade" />
      <Chip tone="core" label="DFN simulation" sub="tier-3 directional" />
      <Chip tone="core" label="Objective + scoring" sub="feasible? rank" />
    </Lane>

    <Lane y={950} label="Knowledge & calibration">
      <Chip tone="data" label="Knowledge base" sub="retrieval grounds the agents in real data" />
      <Chip tone="data" label="Calibration loop" sub="test data refits the DFN to IBC's own cells (the moat)" accent />
    </Lane>

    <div style={{ position: "absolute", left: 80, bottom: 60, display: "flex", gap: 34, fontFamily: fonts.mono, fontSize: 17, color: colors.dim }}>
      <span><span style={{ color: colors.coral }}>↓</span> requirement flows down into ranked designs</span>
      <span><span style={{ color: colors.coral }}>↺</span> test data flows back up and recalibrates</span>
    </div>
  </AbsoluteFill>
);
