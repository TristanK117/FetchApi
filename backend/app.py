from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/bm25", methods=["GET"])
def bm25():
    query = request.args.get("query")
    pass

if __name__ == "__main__":
    app.run(port=5000, debug=True)