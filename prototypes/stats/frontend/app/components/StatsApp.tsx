"use client";

import "./StatsApp.css";
import { runScript } from "../python";
import { useDropzone } from "react-dropzone";

export default function StatsApp() {
  function run() {
    runScript("print('hello world')");
  }

  function onDrop(acceptedFiles: File[]) {
    console.log(acceptedFiles);
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="stats-app">
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
