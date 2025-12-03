import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ApiDetail.css";

export default function ApiDetail() {
    const [recommended, setRecommended] = useState([]);
    const { id } = useParams();
    const navigate = useNavigate();

    const [apiData, setApiData] = useState(null);
    const [loading, setLoading] = useState(true);

    // Fetch main API info + recommended APIs
    useEffect(() => {
        async function loadData() {
            try {
            const bm25Res = await fetch(
                `http://127.0.0.1:5000/api/bm25?query=${encodeURIComponent(id)}`
            );
            const bm25Data = await bm25Res.json();
            const mainAPI = bm25Data.results?.find((item) => String(item.id) === id);
            setApiData(mainAPI || null);

            const recRes = await fetch(`http://127.0.0.1:5000/api/recommend/${id}`);
            const recData = await recRes.json();
            setRecommended(recData.recommendations || []);

            } catch (err) {
            console.error(err);
            } finally {
            setLoading(false);
            }
        }

        loadData();
    }, [id]);

    if (loading) return <p className="loading">Loading API details…</p>;
    if (!apiData) return <p>API not found.</p>;

    return (
        <div className="detail-page">
            {/* Back Button */}
            <button className="back-button" onClick={() => navigate(-1)}>
                ← Back
            </button>

            {/*Detail Layout Section */}
            <div className="detail-layout">

                {/* Left Column api information*/}
                <div className="detail-left">
                <h1 className="api-title">{apiData.name}</h1>
                <p className="api-category">{apiData.category}</p>

                <p className="api-description">{apiData.description}</p>

                <div className="meta-box">
                    <p><strong>Auth:</strong> {apiData.auth || "Unknown"}</p>
                    <p><strong>Category:</strong> {apiData.category}</p>
                    <p><strong>API ID:</strong> {apiData.id}</p>
                </div>
                </div>

                {/*Right Column code snippet */}
                <div className="detail-right">
                <h2>Example Request</h2>

                <pre className="code-block">
                        {`fetch("https://api.example.com/${apiData.id}", {
                                method: "GET",
                                headers: {
                                    "Content-Type": "application/json"
                                }
                            })
                            .then(res => res.json())
                            .then(data => console.log(data));`
                        }
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