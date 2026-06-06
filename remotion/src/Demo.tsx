import React from "react";
import { Series } from "remotion";
import { Title } from "./scenes/Title";
import { Search } from "./scenes/Search";
import { Results } from "./scenes/Results";
import { Generalize } from "./scenes/Generalize";
import { Close } from "./scenes/Close";

export const Demo: React.FC = () => (
  <Series>
    <Series.Sequence durationInFrames={90}>
      <Title />
    </Series.Sequence>
    <Series.Sequence durationInFrames={600}>
      <Search />
    </Series.Sequence>
    <Series.Sequence durationInFrames={300}>
      <Results />
    </Series.Sequence>
    <Series.Sequence durationInFrames={300}>
      <Generalize />
    </Series.Sequence>
    <Series.Sequence durationInFrames={330}>
      <Close />
    </Series.Sequence>
  </Series>
);
