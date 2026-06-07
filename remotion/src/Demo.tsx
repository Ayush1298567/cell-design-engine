import React from "react";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { Intro } from "./scenes/Intro";
import { Architecture } from "./scenes/Architecture";
import { Terminal } from "./scenes/Terminal";
import { Search } from "./scenes/Search";
import { Generalize } from "./scenes/Generalize";
import { Close } from "./scenes/Close";

const timing = linearTiming({ durationInFrames: 18 });

export const Demo: React.FC = () => (
  <TransitionSeries>
    <TransitionSeries.Sequence durationInFrames={150}>
      <Intro />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={330}>
      <Architecture />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={450}>
      <Terminal />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={420}>
      <Search />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={240}>
      <Generalize />
    </TransitionSeries.Sequence>
    <TransitionSeries.Transition timing={timing} presentation={fade()} />
    <TransitionSeries.Sequence durationInFrames={150}>
      <Close />
    </TransitionSeries.Sequence>
  </TransitionSeries>
);
