import React from "react";
import { AbsoluteFill } from "remotion";
import { colors, fonts } from "../theme";

export const Background: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(130% 130% at 50% -10%, ${colors.bg2} 0%, ${colors.bg} 62%)`,
      fontFamily: fonts.sans,
      color: colors.text,
    }}
  >
    {children}
  </AbsoluteFill>
);
