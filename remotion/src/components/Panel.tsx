import React from "react";
import { colors, tokens } from "../theme";

export const Panel: React.FC<{ accent?: boolean; children: React.ReactNode; style?: React.CSSProperties }> = ({ accent, children, style }) => (
  <div
    style={{
      background: colors.panel,
      border: `1px solid ${accent ? colors.coralBorder : colors.hairline}`,
      borderTop: `1px solid ${colors.panelTop}`,
      borderRadius: tokens.radius,
      boxShadow: accent ? `${tokens.shadow}, ${tokens.glow}` : tokens.shadow,
      ...style,
    }}
  >
    {children}
  </div>
);
