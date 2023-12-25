"use client";
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
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/",
      env: {
        PYTHONPATH: "/",
      },
    });
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

async function loadScript(scriptName: string) {
  const resp = await fetch(`/python/${scriptName}`);
  writeFileToFS(`/${scriptName}`, await resp.arrayBuffer());
  console.log(`loaded ${scriptName}`);
}

async function loadAllPythonScripts() {
  // todo: figure out how to no need to list all files..
  const scripts = ["main.py", "testmodule.py"];
  for (const script of scripts) {
    await loadScript(script);
  }
  console.log("loaded all scripts");
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
