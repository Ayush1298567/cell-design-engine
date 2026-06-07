import React from "react";
import { AbsoluteFill } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { Grain } from "./components/Grain";
import { Frame } from "./components/Frame";
import { colors } from "./theme";
import { Intro } from "./scenes/Intro";
import { Architecture } from "./scenes/Architecture";
import { RunInput } from "./scenes/RunInput";
import { Run } from "./scenes/Run";
import { Generalize } from "./scenes/Generalize";
import { Close } from "./scenes/Close";

const timing = linearTiming({ durationInFrames: 18 });

export const Demo: React.FC = () => (
  <AbsoluteFill style={{ background: `radial-gradient(145% 120% at 50% -12%, ${colors.bg1} 0%, ${colors.bg0} 58%)` }}>
    <Grain />
    <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={180}>
      <Intro />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={300}>
      <Architecture />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={180}>
      <RunInput />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={780}>
      <Run />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={210}>
      <Generalize />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={150}>
      <Close />
    </TransitionSeries.Sequence>
    </TransitionSeries>
    <Frame />
  </AbsoluteFill>
);
