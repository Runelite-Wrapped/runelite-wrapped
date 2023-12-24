"use client";

import "./StatsApp.css";
import { runScript } from "../python";

export default function StatsApp() {
  function run() {
    runScript("print('hello world')");
  }

  return (
    <div className="stats-app">
      <h1>hey</h1>
      <button onClick={run}>run script</button>
    </div>
  );
}
