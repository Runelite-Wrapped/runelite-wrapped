"use client";

let _pyodide: any;


const getPyodide = async () => {
  if (!_pyodide) {
    console.log("loading pyodide")
    // check for window.pyodide
    if (!window.loadPyodide) {
      // sleep for 1 second
    }

    _pyodide = await window.loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
    });
    console.log("loading pyodide complete");
  }
  return _pyodide;
}

const writeFileToFS = async (filename: string, content: ArrayBuffer) => {
  const pyodide = await getPyodide();

  // const db = await resp.arrayBuffer()
  const arr = new Uint8Array(content)
  await pyodide.FS.writeFile(filename, arr)
  runScript('import os; print(os.listdir("/"))')
}

const runScript = async (code: string) => {
  const pyodide = await getPyodide();

  try {
    return await pyodide.runPythonAsync(code);
  } catch (error) {
    console.error(error);
    return error.message;
  }
}


export { runScript, writeFileToFS, getPyodide }
