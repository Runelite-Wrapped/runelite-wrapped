import Script from "next/script";
import StatsApp from "./components/StatsApp";

export default function Home() {
  return (
    <div className="main-container">
      <Script src="https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js" />
      <StatsApp />
    </div>
  );
}
