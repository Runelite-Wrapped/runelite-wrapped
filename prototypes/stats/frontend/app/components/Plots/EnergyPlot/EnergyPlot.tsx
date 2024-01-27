"use client";

import React from "react";
import Plot from "react-plotly.js";

export default function LineChart({ x, y }: { x: number[]; y: number[] }) {
  const data = {
    x,
    y,
    mode: "lines",
    line: {
      color: '#282318'
    }
  };
  const layout = { 
    title: "Energy over time",
    paper_bgcolor: '#FFF7E8',
    plot_bgcolor: 'FFF7E8',
    colourway: '#282318'
   };

  return <Plot data={[data]} layout={layout} />;
}
