"use client";

// TODO: convert this into something like "usePyodide"
let _pyodide: any;

interface StatData {
  timestamps: number[];
  runEnergy: number[];
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
    _pyodide.loadPackage(["micropip", "packaging"]);

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

async function loadAllPythonScripts() {
  const pyodide = await getPyodide();
  const response = await fetch("/python/analysis-0.0.1-py3-none-any.whl");
  const buffer = await response.arrayBuffer();
  await pyodide.unpackArchive(buffer, "whl");
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

async function runAnalysis(): Promise<StatData> {
  const script = await (await fetch("/python/main.py")).text();
  const data = await runScript(script);
  return JSON.parse(data);
}

export {
  runScript,
  writeFileToFS,
  getPyodide,
  runAnalysis,
  loadAllPythonScripts,
  type StatData,
};
