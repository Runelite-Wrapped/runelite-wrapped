"use client";

import React from "react";
import Plot from "react-plotly.js";

export default function DensityPlot({ x, y }: { x: number[]; y :number[] }) {
  const data = {
    x,
    y,
    type: 'histogram2dcontour',
    colorscale: 'turbid',
    contours: {
        coloring: 'heatmap',
    },
  };
  const layout = {
    title: 'Tile density',
    paper_bgcolor: '#FFF7E8',
    plot_bgcolor: 'FFF7E8',
    xaxis: { title: 'Tile X Coordinate' },
    yaxis: { title: 'Tile Y Coordinate' },
  };

  return <Plot data={[data]} layout={layout} />;
}

