// Viridis approximation for the energy heatmap.
const stops: Array<[number, [number, number, number]]> = [
  [0.0, [68, 1, 84]],
  [0.25, [59, 82, 139]],
  [0.5, [33, 145, 140]],
  [0.75, [94, 201, 98]],
  [1.0, [253, 231, 37]],
];

export function viridis(t: number): [number, number, number] {
  const x = Math.max(0, Math.min(1, t));
  for (let i = 0; i < stops.length - 1; i++) {
    const [a, ca] = stops[i];
    const [b, cb] = stops[i + 1];
    if (x >= a && x <= b) {
      const f = (x - a) / (b - a || 1);
      return [
        Math.round(ca[0] + (cb[0] - ca[0]) * f),
        Math.round(ca[1] + (cb[1] - ca[1]) * f),
        Math.round(ca[2] + (cb[2] - ca[2]) * f),
      ];
    }
  }
  return [253, 231, 37];
}

export function rgb([r, g, b]: [number, number, number], alpha = 1): string {
  return `rgba(${r},${g},${b},${alpha})`;
}
