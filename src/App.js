import Header from "./components/Header.jsx";
import Home from "./pages/Home.jsx";
import Search from "./pages/Search.jsx";
import About from "./pages/About.jsx";
import { Routes, Route } from "react-router-dom";
import ApiDetail from "./pages/ApiDetail.jsx";

export default function App() {
  return (
    <div className="app">
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<Search />} />
        <Route path="/about" element={<About />} />
        <Route path="/api/:id" element={<ApiDetail />} />
      </Routes>

    </div>
  );
}