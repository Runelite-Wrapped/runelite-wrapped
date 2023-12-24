"use client";

import React from "react";
import Plot from "react-plotly.js";

export default function LineChart() {
  const data = {
    x: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    y: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    mode: "lines",
  };
  const layout = { title: "NICE" };

  return <Plot data={[data]} layout={layout} />;
}
