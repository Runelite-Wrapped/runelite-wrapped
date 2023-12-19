let pyodide = null;

async function main() {
  pyodide = await loadPyodide();
  await pyodide.loadPackage("sqlite3");
  // Pyodide is now ready to use...
  console.log(pyodide.runPython(`
      import sys
      sys.version
    `));
};

async function runScript(scriptName) {
  const resp = await fetch(`/python/${scriptName}`)
  const script = await resp.text()
  return pyodide.runPython(script)
}

async function loadDb(dbPath) {
  const resp = await fetch(dbPath)
  const db = await resp.arrayBuffer()
  console.log(db.byteLength)
  const arr = new Uint8Array(db)
  await pyodide.FS.writeFile("/stat.db", arr)
  pyodide.runPython(`
    import os
    print(os.path.exists("/stat.db"))
    print(os.stat("/stat.db").st_size)
  `)
}

let $ = document.querySelector.bind(document);

window.addEventListener("load", async function () {
  // get output element
  let output = $("#output");
  output.innerHTML = "Hello World!";
  await main();
  await loadDb("/test.db");
  await runScript("read_db.py")
});
