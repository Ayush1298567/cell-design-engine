import { loadFont as loadSans } from "@remotion/google-fonts/Inter";
import { loadFont as loadSerif } from "@remotion/google-fonts/Fraunces";
import { loadFont as loadMono } from "@remotion/google-fonts/IBMPlexMono";

const sans = loadSans("normal", { weights: ["400", "500", "600", "700"] }).fontFamily;
const serif = loadSerif("normal", { weights: ["500", "600", "700"] }).fontFamily;
const mono = loadMono("normal", { weights: ["400", "500"] }).fontFamily;

export const fonts = { sans, serif, mono };

export const colors = {
  bg0: "#08070a",
  bg1: "#110d11",
  panel: "#15121b",
  panelTop: "rgba(255,255,255,0.10)",
  hairline: "rgba(255,255,255,0.09)",
  text: "#f4efed",
  body: "#cfc7c4",
  dim: "#8e837e",
  faint: "#5a534f",
  coral: "#ff5a69",
  coralLabel: "#ff8088",
  coralBorder: "rgba(255,90,105,0.35)",
  amber: "#ff9d6c",
};

export const tokens = {
  radius: 16,
  shadow: "0 16px 50px rgba(0,0,0,0.55)",
  glow: "0 0 64px rgba(255,90,105,0.16)",
  safeX: 160,
  safeRight: 1760,
  safeTop: 156,
  safeBottom: 128,
};
