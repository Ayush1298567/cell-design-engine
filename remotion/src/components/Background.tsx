import React from "react";
import { AbsoluteFill } from "remotion";
import { colors, fonts } from "../theme";

// Transparent wrapper. The base gradient, grain, and brand frame live at the
// composition level (Demo) so they stay constant while scenes cross-fade.
export const Background: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ fontFamily: fonts.sans, color: colors.text }}>{children}</AbsoluteFill>
);
