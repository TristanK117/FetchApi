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

  async function fetchResults(q) {
    try {
      setLoading(true);
      setError("");

      const res = await fetch(
        `http://127.0.0.1:5000/api/bm25?query=${encodeURIComponent(q)}`
      );

      if (!res.ok) throw new Error("Server error");

      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setError("Something went wrong while fetching results.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (query) fetchResults(query);
  }, [query]);

  return (
    <div className="search-page">

      {/*Left Sidebar*/}
      <aside className="sidebar">
        <h3 className="sidebar-title">Filters</h3>

        <div className="filter-group">
          <label className="filter-label">Category</label>
          <select className="filter-select">
            <option>All</option>
            <option>Weather</option>
            <option>Finance</option>
            <option>AI</option>
            <option>Maps</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">Authentication</label>
          <select className="filter-select">
            <option>All</option>
            <option>No Auth</option>
            <option>API Key</option>
            <option>OAuth</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">Sort by</label>
          <select className="filter-select">
            <option>Relevance</option>
            <option>Popularity</option>
            <option>Ease of Use</option>
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

        {/*Tabs*/}
        <div className="sort-tabs">
          <span className="tab active">Category</span>
          <span className="tab">Popularity</span>
          <span className="tab">Ease of Use</span>
        </div>

        {/*Result list*/}
        {loading && <p>Searching...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {!loading && results.length === 0 && (
          <p>No results found.</p>
        )}

        <div className="result-list">
          {results.map((api, index) => {
            const similarity = Math.min(api.score * 10, 99);

            return (
              <div
                className="result-card"
                key={api.id || index}
                onClick={() => navigate(`/api/${api.id}`)}
                style={{ cursor: "pointer" }}
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