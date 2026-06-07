import React from "react";
import { colors, fonts } from "../theme";

export const Eyebrow: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <div style={{ fontFamily: fonts.mono, fontSize: 19, letterSpacing: "0.22em", color: colors.coralLabel, textTransform: "uppercase", ...style }}>
    {children}
  </div>
);
