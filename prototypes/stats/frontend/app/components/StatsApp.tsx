"use client";

import Script from "next/script";
// import "./StatsApp.css";
import {
  writeFileToFS,
  getPyodide,
  runTileDataAnalysis,
  runGameTickAnalysis,
  CombinedData,
  StatData,
  TileData,
  loadAnalysisModule,
} from "../pythonWrapper";
import ExamplePlot from "./ExamplePlot";
import { useDropzone } from "react-dropzone";
import { useState } from "react";

export default function StatsApp() {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
  const [data, setData] = useState<StatData | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [tileData, setTileData] = useState<TileData | null>(null);

  async function onDrop(acceptedFiles: File[]) {
    await writeFileToFS("/stats.db", await acceptedFiles[0].arrayBuffer());
    const newData = await runGameTickAnalysis('jerome-o');
    setData(newData);
    console.log(data); // 'data' isn't updated until the scope of onDrop is finished
  }

  async function useDefault() {
    await writeFileToFS(
      "/stats.db",
      await fetch("/databases/rlw_1.db").then((res) => res.arrayBuffer())
    );
    const newData = await runGameTickAnalysis('jerome-o');
    console.log("Setting energy data")
    setData(newData);
    console.log("Energy data has been set:")
    console.log(newData);
    const tileData = await runTileDataAnalysis('jerome-o');
    console.log("Setting tile data")
    setTileData(tileData);
    console.log("Tile data has been set:")
    console.log(tileData);

  }

  async function onLoad() {
    await getPyodide();
    await loadAnalysisModule();
  }

  return (
    <div className={`flex flex-col content-center items-center justify-center h-[100vh] w-[100vw] bg-osrslb-100 ${data ? 'fade-in' : ''}`}>
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"
        onLoad={onLoad}
      />
      {data ? (
        <div>
          {!loaded ? 
          <button 
          className="flex justify-center content-center bg-osrslb-300 text-osrslb-100 hover:bg-osrslb-700 rounded-md hover:rounded-none duration-700 ease-in-out font-extrathin py-2 px-4 mt-4 mb-4 m-auto" 
          onClick={() => {setLoaded(true), console.log(data)}}
          >Show the goods!
          </button>
          : 
          <div className={`${loaded ? 'fade-in' : ''}`}>
            <ExamplePlot x={data.timestamps} y={data.runEnergy}/>
          </div>}
        </div>
      ) : (
        <div className="relative flex-col justify-center align-middle content-center bg-osrslb-100 w-[100vw] h-full">
          <button 
          className="flex justify-center content-center bg-osrslb-300 text-osrslb-100 hover:bg-osrslb-700 rounded-md hover:rounded-none duration-700 ease-in-out font-extrathin py-2 px-4 mt-4 mb-4 m-auto" onClick={useDefault}
          >Use Default
          </button>
          <div
            className={
              isDragActive ? 
              "bg-osrslb-100 hover:bg-osrslb-150 w-1/5 h-1/2 flex justify-center items-center  align-middle border-2 rounded-[100px] hover:rounded-[50px] duration-500 ease-in-out border-dashed m-auto" : 
              "bg-osrslb-100 hover:bg-osrslb-150 w-1/5 h-1/2 flex justify-center items-center  align-middle border-2 rounded-[150px] hover:rounded-[120px] duration-500 ease-in-out border-dashed m-auto"
            }
            {...getRootProps()}
          >
            <input {...getInputProps()} />
            {isDragActive ? <p className="align-middle">you got this</p> : <p>Drop your files here</p>}
          </div>
        </div>
      )}
    </div>
  );
}

// .drop-zone {
//   width: 50%;
//   height: 50%;
//   display: flex;
//   justify-content: center;
//   align-items: center;
//   border-radius: 15px;
//   border: 2px dashed #444;
// }