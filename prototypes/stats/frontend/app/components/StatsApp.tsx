"use client";

import Script from "next/script";
import "./StatsApp.css";
import {
  runScript,
  writeFileToFS,
  getPyodide,
  runAnalysis,
} from "../pythonWrapper";
import { useDropzone } from "react-dropzone";

export default function StatsApp() {
  function run() {
    runScript("print('hello world')");
  }

  async function onDrop(acceptedFiles: File[]) {
    await writeFileToFS("/stats.db", await acceptedFiles[0].arrayBuffer());
    const data = await runAnalysis();
    console.log(data);
  }

  async function onLoad() {
    await getPyodide();
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="stats-app">
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js"
        onLoad={onLoad}
      />
      <div
        className={isDragActive ? "drop-zone drop-zone-active" : "drop-zone"}
        {...getRootProps()}
      >
        <input {...getInputProps()} />
        {isDragActive ? <p>you got this</p> : <p>drop some files</p>}
      </div>
    </div>
  );
}
