"""
Veritas API — Flask backend serving deception-marker analysis.

Run:
    python app.py
Then:
    POST http://localhost:5000/analyze
    { "statement": "I basically left around 6, give or take." }
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from inference import score_statement

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    statement = data.get("statement", "").strip()

    if not statement:
        return jsonify({"error": "missing 'statement' field"}), 400

    if len(statement) > 4000:
        return jsonify({"error": "statement too long (max 4000 chars)"}), 400

    result = score_statement(statement)
    result["statement"] = statement
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
