from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import re
from rank_bm25 import BM25Okapi

app = Flask(__name__)
CORS(app)

#load the data
df = pd.read_csv("../data/cleaned/apis_cleaned.csv")

def preprocess(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.replace("\u2028", " ").replace("\u2029", " ")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

NAME_WEIGHT = 4
CATEGORY_WEIGHT = 2

def build_weighted_text(row):
    name = preprocess(row["name"])
    desc = preprocess(row["description"])
    cat = preprocess(row["category"])

    # Weighted text string
    weighted = (
        (name + " ") * NAME_WEIGHT +
        (cat + " ") * CATEGORY_WEIGHT +
        desc
    )

    return weighted.strip()

df["weighted_text"] = df.apply(build_weighted_text, axis=1)

corpus = df["weighted_text"].tolist()
tokenized = [doc.split() for doc in corpus]
bm25 = BM25Okapi(tokenized)

@app.route("/api/bm25", methods=["GET"])
def bm25_search():
    query = request.args.get("query")
    # print("QUERY:", query)
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    clean_query = preprocess(query)
    q_tokens = clean_query.split()
    scores = bm25.get_scores(q_tokens)

    top_n = 10
    top_idx = scores.argsort()[::-1][:top_n]

    results = []
    for idx in top_idx:
        if scores[idx] <= 0:
            continue
        rec = df.iloc[idx].to_dict()
        rec["score"] = float(scores[idx])
        results.append(rec)

    # print("TOP INDEXES:", top_idx)
    # print("RESULTS:", results)
    return jsonify({
        "query": query,
        "results": results
    })

@app.route("/api/recommend/<api_id>", methods=["GET"])
def recommend(api_id):
    try:
        item = df[df["id"] == api_id]
        if item.empty:
            return jsonify({"error": "API ID not found"}), 404

        query_text = item.iloc[0]["weighted_text"]
        q_tokens = query_text.split()

        scores = bm25.get_scores(q_tokens)

        top_idx = scores.argsort()[::-1][:6]   # 6 because one will be itself

        results = []
        for idx in top_idx:
            if df.iloc[idx]["id"] == api_id:
                continue  

            if scores[idx] <= 0:
                continue
            
            rec = df.iloc[idx].to_dict()
            rec["score"] = float(scores[idx])
            results.append(rec)

        return jsonify({"id": api_id, "recommendations": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)