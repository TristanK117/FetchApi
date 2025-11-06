import Header from "./components/Header.jsx";
import Home from "./pages/Home.jsx";
import Search from "./pages/Search.jsx";
import About from "./pages/About.jsx";
import { Routes, Route } from "react-router-dom";

export default function App() {
  return (
    <div className="app">
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/search" element={<Search />} />
        <Route path="/about" element={<About />} />
      </Routes>

      <footer className="app-footer">
        <small>&copy; {new Date().getFullYear()} FetchAPI</small>
      </footer>
    </div>
  );
}