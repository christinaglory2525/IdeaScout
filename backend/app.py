from flask import Flask, request, jsonify
from flask_cors import CORS
from services.search import search_all
from services.analyzer import analyze_results

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "IdeaScout backend is running!"


@app.route("/analyze", methods=["POST"])
def analyze():

    # Get JSON data from frontend/request
    data = request.get_json(silent=True) or {}

    # Get user's idea
    idea = data.get("idea", "").strip()

    # Check if idea is empty
    if not idea:
        return jsonify({
            "error": "Please enter an idea."
        }), 400

    print("\n" + "=" * 60)
    print("IDEASCOUT ANALYSIS")
    print("=" * 60)

    print(f"Analyzing idea: {idea}")

    # Search research papers + GitHub projects
    results = search_all(idea)

    # Debug information
    print(f"Found {len(results)} results")
    print("Sources:", [result["source"] for result in results])

    # Analyze similarity + generate recommendations
    analysis = analyze_results(idea, results)

    print(f"Originality Indicator: {analysis['originality_indicator']}")

    print("=" * 60)

    # Send results back to frontend
    return jsonify({
    "idea": idea,
    "result_count": len(results),
    "originality_indicator": analysis["originality_indicator"],
    "matches": analysis["matches"],
    "recommendations": analysis["recommendations"],
    "gaps": analysis["gaps"]
})


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )