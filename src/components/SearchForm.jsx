// src/components/SearchForm.jsx
import React, { useState } from "react";
import "./SearchForm.css";

// Simple search bar component
// No backend yet, just logs queries.

export default function SearchForm({ onSearch }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    console.log("Searching for:", query);

    if (onSearch) {
      onSearch(query);
    }
  };

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="search-input"
        placeholder="Search for an API (e.g. weather with pollution data)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
}