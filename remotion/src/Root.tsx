import React from "react";
import { Composition } from "remotion";
import { Demo } from "./Demo";
import { ArchDiagram } from "./ArchDiagram";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Demo"
        component={Demo}
        durationInFrames={1710}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition id="Arch" component={ArchDiagram} durationInFrames={1} fps={30} width={1920} height={1200} />
    </>
  );
};
