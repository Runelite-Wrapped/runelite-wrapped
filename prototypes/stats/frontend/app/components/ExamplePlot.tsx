"use client";

import React from "react";
import Plot from "react-plotly.js";

export default function LineChart({ x, y }: { x: number[]; y: number[] }) {
  const data = {
    x,
    y,
    mode: "lines",
  };
  const layout = { title: "NICE" };

  return <Plot data={[data]} layout={layout} />;
}
