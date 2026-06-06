export type Bounds = { thk: [number, number]; por: [number, number] };

// Heatmap plot area in 1920x1080 space.
export const PLOT = { x: 180, y: 230, w: 820, h: 620 };

export function scales(b: Bounds, plot = PLOT) {
  const sx = (thk: number) =>
    plot.x + ((thk - b.thk[0]) / (b.thk[1] - b.thk[0])) * plot.w;
  const sy = (por: number) =>
    plot.y + plot.h - ((por - b.por[0]) / (b.por[1] - b.por[0])) * plot.h;
  return { sx, sy };
}
