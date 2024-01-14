"use client";

import Script from "next/script";
// import "./StatsApp.css";
import {
  writeFileToFS,
  getPyodide,
  runTileDataAnalysis,
  runEnergyDataAnalysis,
  calculateTileCount,
  CombinedData,
  EnergyData,
  TileData,
  TileCount,
  loadAnalysisModule,
} from "../pythonWrapper";
import EnergyPlot from "./EnergyPlot/EnergyPlot";
import TilePlot from "./TilePlot/TilePlot";
import TileSplatter from "./TileSplatter/TileSplatter";
import { useDropzone } from "react-dropzone";
import { useState } from "react";

const btnclass = "flex justify-center content-center bg-osrslb-300 text-osrslb-100 hover:bg-osrslb-700 rounded-md hover:rounded-none duration-700 ease-in-out font-extrathin py-2 px-4 mt-4 mb-4 m-auto"

export default function StatsApp() {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
  const [energyData, setEnergyData] = useState<EnergyData | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [tileData, setTileData] = useState<TileData | null>(null);
  const [tileCount, setTileCount] = useState<TileCount | null>(null);
  const [activePlot, setActivePlot] = useState<String | null>(null);

  const handlePlotChange = (plot: string) => {
    setActivePlot(plot);
  };

  async function processFile(fileBuffer: ArrayBuffer) {
    try {
        await writeFileToFS("/stats.db", fileBuffer);
        console.log("Setting energy data");
        const energyData = await runEnergyDataAnalysis('jerome-o');
        setEnergyData(energyData);
        console.log("Energy data has been set:", energyData);
        console.log("Setting tile data");
        const tileData = await runTileDataAnalysis('jerome-o');
        setTileData(tileData);
        console.log("Tile data has been set:", tileData);
        const tileCount = await calculateTileCount('jerome-o');
        setTileCount(tileCount);
        console.log("Tile count has been set:", tileCount);
    } catch (error) {
        console.error("Error processing database file to file system:", error);
    }
  }

  const allLoaded = energyData && tileData && tileCount

  async function onDrop(acceptedFiles: File[]) {
    try {
        if (acceptedFiles.length === 0) return;
        const fileBuffer = await acceptedFiles[0].arrayBuffer();
        await processFile(fileBuffer);
    } catch (error) {
        console.error("Error loading input file", error);
    }
  }

  async function useDefault() {
    try {
        const res = await fetch("/databases/rlw_1.db");
        if (!res.ok) throw new Error("Could not load default database file");
        const fileBuffer = await res.arrayBuffer();
        await processFile(fileBuffer);
    } catch (error) {
        console.error("Error loading default database:", error);
    }
  }

  async function onLoad() {
    await getPyodide();
    await loadAnalysisModule();
  }

  let selectedPlot;
  switch (activePlot) {
      case 'energy':
        selectedPlot = <EnergyPlot x={energyData.timestamps} y={energyData.runEnergy} />;
          break;
      case 'tiles':
        selectedPlot = <TilePlot x={tileData.timestamps} y={tileData.regionId} />;
          break;
      case 'tilesplatter':
        selectedPlot = <TileSplatter x={tileData.xcoord} y={tileData.ycoord} />;
          break;
      default:
        selectedPlot = <div>Select a plot</div>;
  }

  return (
    <div className={`flex flex-col content-center items-center justify-center h-[100vh] w-[100vw] bg-osrslb-100 ${energyData ? 'fade-in' : ''}`}>
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"
        onLoad={onLoad}
      />
      {allLoaded ? (
        <div>
          {!loaded ? 
          <button 
          className={btnclass}
          onClick={() => {setLoaded(true)}}
          >Show the goods!
          </button>
          : 
          <div className={`${loaded ? 'fade-in' : ''}`}>
            <div className="flex flex-row gap-3">
              <button 
                className={`${btnclass} w-5rem`}
                onClick={() => handlePlotChange('energy')}
              >
                Energy
              </button>
              <button
                className={`${btnclass} w-5rem`}
                onClick={() => handlePlotChange('tiles')}
              >
                Tiles
              </button>
              <button
                className={`${btnclass} w-5rem`}
                onClick={() => handlePlotChange('tilesplatter')}
              >
                Tiles (but more of them)
              </button>
            </div>
            {selectedPlot}
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
