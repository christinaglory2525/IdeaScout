from flask import Flask, request, jsonify
from services.search import search_all
from services.analyzer import analyze_results

app = Flask(__name__)


@app.route("/")
def home():
    return "IdeaScout backend is running!"


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json(silent=True) or {}

    idea = data.get("idea", "").strip()

    if not idea:
        return jsonify({
            "error": "Please enter an idea."
        }), 400

    print(f"\nAnalyzing idea: {idea}")

    # Search existing papers and GitHub projects
    results = search_all(idea)

    print(f"Found {len(results)} results")

    # Analyze similarity
    analysis = analyze_results(idea, results)

    return jsonify({
        "idea": idea,
        "result_count": len(results),
        "originality_indicator": analysis["originality_indicator"],
        "matches": analysis["matches"]
    })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )