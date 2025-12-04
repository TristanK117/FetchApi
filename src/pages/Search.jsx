import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";

import "./Search.css";

export default function Search() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const query = searchParams.get("query") || "";

  const [searchText, setSearchText] = useState(query);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [authFilter, setAuthFilter] = useState("All");
  const [sortOption, setSortOption] = useState("Relevance");


  function fetchResults(q) {
    setLoading(true);
    setError("");

    fetch(`http://127.0.0.1:5000/api/hybrid?query=${encodeURIComponent(q)}`)
      .then((res) => {
        if (!res.ok) {
          setError("Something went wrong while fetching results.");
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (data && data.results) {
          setResults(data.results);
        } else {
          setResults([]);
        }
      })
      .catch(() => {
        setError("Something went wrong while fetching results.");
      })
      .finally(() => {
        setLoading(false);
      });
  }
  

  useEffect(() => {
    if (query) fetchResults(query);
  }, [query]);

  const filteredResults = results
  .filter((api) => {
    // Category filter
    if (categoryFilter !== "All" && api.category !== categoryFilter)
      return false;

    // Auth filter
    if (authFilter !== "All") {
      const apiAuth = (api.auth_type || "").toLowerCase();

      if (authFilter === "No Auth" && apiAuth !== "no") return false;
      if (authFilter === "API Key" && apiAuth !== "apikey") return false;
      if (authFilter === "OAuth" && apiAuth !== "oauth") return false;
    }

    return true;
  });

  // Sorting
  if (sortOption === "Relevance") {
    filteredResults.sort((a, b) => b.hybrid_score - a.hybrid_score);
  }
  // Optional sorting placeholders:
  else if (sortOption === "Popularity") {
    filteredResults.sort((a, b) => (b.popularity || 0) - (a.popularity || 0));
  } else if (sortOption === "Ease of Use") {
    filteredResults.sort((a, b) => (b.ease || 0) - (a.ease || 0));
  }
  return (
    <div className="search-page">

      {/*Left Sidebar*/}
      <aside className="sidebar">
        <h3 className="sidebar-title">Filters</h3>

        <div className="filter-group">
          <label className="filter-label">Category</label>
          <select
              className="filter-select"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option>All</option>
              <option>Weather</option>
              <option>Finance</option>
              <option>AI</option>
              <option>Maps</option>
            </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">Authentication</label>
          <select
              className="filter-select"
              value={authFilter}
              onChange={(e) => setAuthFilter(e.target.value)}
            >
              <option>All</option>
              <option>No Auth</option>
              <option>API Key</option>
              <option>OAuth</option>
            </select>
        </div>
      </aside>

      {/*Main Content*/}
      <main className="search-results">

        {/*Search bar*/}
        <div className="search-header">
          <input
            className="search-input"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          <button className="search-button" onClick={() => fetchResults(searchText)}>
            Search
          </button>
        </div>

        {/*Result list*/}
        {loading && <p>Searching...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {!loading && results.length === 0 && (
          <p>No results found.</p>
        )}

        <div className="result-list">
          {filteredResults.map((api, index) => {
            const similarity = api.hybrid_score ?? 0;
            
            return (
              <div
                className="result-card"
                key={api.id || index}
                onClick={() => navigate(`/api/${api.id}`)}
                style={{ 
                  cursor: "pointer",
                }}
                
              >
                <div className="result-top">
                  <h3 className="api-name">{api.name}</h3>
                  <span className="similarity">
                    Similarity {similarity.toFixed(0)}%
                  </span>
                </div>

                <div className="similarity-bar">
                  <div className="bar-fill" style={{ width: `${similarity}%` }}></div>
                </div>

                <p className="api-description">{api.description}</p>
                <p className="api-category">{api.category}</p>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
}