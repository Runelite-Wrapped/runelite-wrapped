import StatsApp from "./components/StatsApp";
import Navbar from "./components/Navbar";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-[100vh] w-[100vw]">
      <Navbar />
      <StatsApp />
    </div>
  );
}