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
        placeholder="e.g. weather and pollution data by city"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button type="submit" className="search-button">
        Search
      </button>
    </form>
  );
}