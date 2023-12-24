"use client";

let _pyodide: any;


const getPyodide = async () => {
  if (!_pyodide) {
    console.log("loading pyodide")
    _pyodide = await window.loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
    });
    console.log("loading pyodide complete");
  }
  return _pyodide;
}

const writeFileToFS = async (filename: string, content: ArrayBufferView) => {
  const pyodide = await getPyodide();
  pyodide.FS.writeFile(filename, content);
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


export { runScript, writeFileToFS }
