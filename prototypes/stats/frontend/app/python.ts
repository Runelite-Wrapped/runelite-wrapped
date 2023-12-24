"use client";

let pyodide: any;

const runScript = async (code: string) => {
  if (!pyodide) {
    console.log("loading pyodide")
    pyodide = await window.loadPyodide({
      indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
    });
    console.log("loading pyodide complete");
  }

  try {
    return await pyodide.runPythonAsync(code);
  } catch (error) {
    console.error(error);
    return error.message;
  }
}


export { runScript }
