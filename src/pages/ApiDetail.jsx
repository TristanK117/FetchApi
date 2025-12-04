import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ApiDetail.css";

export default function ApiDetail() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [apiData, setApiData] = useState(null);
    const [recommended, setRecommended] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
    // Load main API + recommended APIs
    fetch(`http://127.0.0.1:5000/api/hybrid?query=${encodeURIComponent(id)}`)
      .then((res) => {
        if (!res.ok) return null;
        return res.json();
      })
      .then((data) => {
        if (data && data.results) {
          const mainAPI = data.results.find((item) => String(item.id) === id);
          setApiData(mainAPI || null);
        }
      })
      .catch(() => {
        setApiData(null);
      });

    fetch(`http://127.0.0.1:5000/api/recommend/${id}`)
      .then((res) => {
        if (!res.ok) return null;
        return res.json();
      })
      .then((data) => {
        if (data && data.recommendations) {
          setRecommended(data.recommendations);
        }
      })
      .catch(() => {
        setRecommended([]);
      })
      .finally(() => {
        setLoading(false);
      });
    }, [id]);

    if (loading) return <p className="loading">Loading API details…</p>;
    if (!apiData) return <p>API not found.</p>;

    return (
        <div className="detail-page">
            {/* Back Button */}
            <button className="back-button" onClick={() => navigate(-1)}>
                ← Back
            </button>

            <div className="detail-header">
                <h1 className="api-title">{apiData.name}</h1>

                <div className="tag-row">
                <span className="tag category-tag">{apiData.category}</span>
                <span className="tag auth-tag">{apiData.auth || "No Auth"}</span>
                </div>
            </div>

            {/*Detail Layout Section */}
            <div className="detail-layout">

                {/* Left Column api information*/}
                <div className="detail-left">
                    <p className="api-description">{apiData.description}</p>

                    <div className="meta-section">
                        <h3>API Details</h3>
                        <ul className="meta-list">
                        <li><strong>API ID:</strong> {apiData.id}</li>
                        <li><strong>Category:</strong> {apiData.category}</li>
                        <li><strong>Auth:</strong> {apiData.auth || "Unknown"}</li>
                        </ul>
                    </div>
                </div>

                {/*Right Column code snippet */}
                <div className="detail-right">
                    <div className="code-header">
                        <button className="code-tab active">JavaScript</button>
                        <button className="code-tab">Python</button>
                        <button className="copy-btn">Copy</button>
                    </div>

                    <pre className="code-box">
                {`fetch("https://api.example.com/${apiData.id}", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
                })
                .then(res => res.json())
                .then(data => console.log(data));`}
                    </pre>
                    </div>

        </div>
            
            {/* Recommended APIs Section */}
            <div className="recommended-section">
                <h2>Recommended APIs</h2>

                {recommended.length === 0 && (
                    <p>No similar APIs found.</p>
                )}

                <div className="recommended-list">
                    {recommended.map((api, i) => (
                        <div
                            key={api.id || i}
                            className="recommended-card"
                            onClick={() => navigate(`/api/${api.id}`)}
                        >
                            <h3>{api.name}</h3>
                            <p>{api.description?.slice(0, 120)}...</p>
                            <span className="rec-category">{api.category}</span>
                        </div>
                    ))}
                </div>
            </div>

        </div>
    );
}