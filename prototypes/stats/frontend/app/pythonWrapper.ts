"use client";

// TODO: convert this into something like "usePyodide"
let _pyodide: any;

interface EnergyData {
  timestamps: number[];
  runEnergy: number[];
}
interface TileData {
  timestamps: number[];
  xcoord: number[];
  ycoord: number[];
  regionId: number[];
}

interface TileCount {
  tilecount: number[]
  username: string[],
  favourite_tile: any[],
}
interface CombinedData {
  energyData: EnergyData;
  tileData: TileData;
}

const getPyodide = async () => {
  if (!_pyodide) {
    // todo: handle race condition
    console.log("loading pyodide");

    _pyodide = await window.loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.24.1/full/",
      env: {
        PYTHONPATH: "/",
      },
    });
    await _pyodide.loadPackage(["micropip", "packaging", "sqlite3", "pandas"]);
    

    // for debugging
    window.pyodide = _pyodide;
    console.log("loading pyodide complete");
  }
  return _pyodide;
};

const writeFileToFS = async (filename: string, content: ArrayBuffer) => {
  const pyodide = await getPyodide();

  // const db = await resp.arrayBuffer()
  const arr = new Uint8Array(content);
  await pyodide.FS.writeFile(filename, arr);
};

async function loadAnalysisModule() {
  const pyodide = await getPyodide();
  const response = await fetch("/python/analysis-0.0.1-py3-none-any.whl");
  const buffer = await response.arrayBuffer();
  await pyodide.unpackArchive(buffer, "whl");
  console.log("loaded analysis module");
}

const runScript = async (code: string) => {
  const pyodide = await getPyodide();

  try {
    return await pyodide.runPythonAsync(code);
  } catch (error) {
    console.error(error);
    return error.message;
  }
};

// async function runAnalysis(): Promise<CombinedData> {
//   const data = await runScript("import analysis; analysis.run()");
//   return JSON.parse(data);
// }

const runPythonFunction = async (functionName: string, args: any[] = []) => {
  const pyodide = await getPyodide();
  const argStr = args.map(JSON.stringify).join(", ");
  const code = `import analysis; analysis.${functionName}(${argStr})`;
  
  try {
    const result = await pyodide.runPythonAsync(code);
    return result;
  } catch (error) {
    console.error(error);
    return error.message;
  }
};

async function runEnergyDataAnalysis(username: string): Promise<EnergyData> {
  const data = await runPythonFunction('get_energy_data', [username]);
  return JSON.parse(data);
}

async function runTileDataAnalysis(username: string): Promise<TileData> {
  const data = await runPythonFunction('get_tile_data', [username]);
  return JSON.parse(data);
}

async function calculateTileCount(username: string): Promise<TileCount> {
  const data = await runPythonFunction('calculate_tile_count', [username]);
  return JSON.parse(data);
}

export {
  runScript,
  writeFileToFS,
  getPyodide,
  loadAnalysisModule,
  runEnergyDataAnalysis,
  runTileDataAnalysis,
  calculateTileCount,
  type CombinedData,
  type EnergyData,
  type TileData,
  type TileCount,
};
