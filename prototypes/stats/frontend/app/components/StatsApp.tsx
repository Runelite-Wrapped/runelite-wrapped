"use client";

import Script from "next/script";
import "./StatsApp.css";
import {
  writeFileToFS,
  getPyodide,
  runAnalysis,
  StatData,
  loadAllPythonScripts,
} from "../pythonWrapper";
import ExamplePlot from "./ExamplePlot";
import { useDropzone } from "react-dropzone";
import { useState } from "react";

export default function StatsApp() {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
  const [data, setData] = useState<StatData | null>(null);

  async function onDrop(acceptedFiles: File[]) {
    await writeFileToFS("/stats.db", await acceptedFiles[0].arrayBuffer());
    const newData = await runAnalysis();
    setData(newData);
    console.log(data);
  }

  async function onLoad() {
    await getPyodide();
    await loadAllPythonScripts();
  }

  return (
    <div className="stats-app">
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js"
        onLoad={onLoad}
      />
      {data ? (
        <ExamplePlot x={data.timestamps} y={data.runEnergy} />
      ) : (
        <div
          className={isDragActive ? "drop-zone drop-zone-active" : "drop-zone"}
          {...getRootProps()}
        >
          <input {...getInputProps()} />
          {isDragActive ? <p>you got this</p> : <p>drop some files</p>}
        </div>
      )}
    </div>
  );
}
