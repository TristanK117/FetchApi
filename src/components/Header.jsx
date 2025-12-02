import React from "react";
import { Link } from "react-router-dom";
import "./Header.css";

export default function Header() {
  return (
    <header className="header">
      <div className="header-logo">FetchAPI</div>

      <nav className="header-nav">
        <Link to="/" className="header-link">Home</Link>
        <Link to="/search" className="header-link">Search</Link>
        <Link to="/about" className="header-link">About</Link>
      </nav>
    </header>
  );
}