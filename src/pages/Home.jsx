import React from "react";
import "./Home.css";
import SearchForm from "../components/SearchForm.jsx";

export default function Home() {
  return (
    <div className="home-page">

      {/* Header Section */}
      <section className="section">
        <h1 className="title">FetchAPI</h1>
        <p className="subtitle">
          Centralized search tool for APIs 
        </p>
      </section>

      <section className="section">
        <SearchForm />
      </section>

      {/* Project Sections */}
      <section className="section">
        <h2 className="section-title">Motivation & Problem</h2>
        <p className="text">
          Developers often waste time searching for APIs that match their project 
          needs. Platforms like RapidAPI rely mainly on keyword matching, which 
          ignores developer intent. For example, searching for 
          <em> “weather + pollution by city” </em> may return general weather APIs 
          but miss APIs with air quality data.
        </p>
        <p className="text">
          FetchAPI addresses this by using semantic search to understand meaning 
          behind user queries and API documentation. This improves accuracy and 
          supports more efficient developer workflows.
        </p>
      </section>

      <section className="section">
        <h2 className="section-title">Related Work</h2>
        <p className="text">
          Systems like BIKER use embeddings and StackOverflow posts to recommend 
          Java APIs. FetchAPI aims to expand this idea to a broader set of APIs 
          and apply IR techniques such as BM25 and semantic similarity to 
          interpret natural language queries.
        </p>
      </section>

      <section className="section">
        <h2 className="section-title">How FetchAPI Works</h2>
        <p className="text">
          • Index API descriptions and documentation  
          • Use BM25 + semantic similarity to compute relevance  
          • Rank APIs by intent, functionality, and ease of use  
          • Display summaries, metadata, and links  
        </p>
      </section>

      <section className="section">
        <h2 className="section-title">Expected Output</h2>
        <p className="text">
          A ranked list of APIs relevant to the user’s query, with summaries, 
          authentication details, and documentation snippets. The prototype will 
          demonstrate intent-based retrieval and score interpretation.
        </p>
      </section>
    </div>
  );
}