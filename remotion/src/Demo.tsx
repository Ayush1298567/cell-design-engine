import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { Intro } from "./scenes/Intro";
import { Architecture } from "./scenes/Architecture";
import { RunInput } from "./scenes/RunInput";
import { Run } from "./scenes/Run";
import { Generalize } from "./scenes/Generalize";
import { Close } from "./scenes/Close";

const timing = linearTiming({ durationInFrames: 18 });

export const Demo: React.FC = () => (
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
);
