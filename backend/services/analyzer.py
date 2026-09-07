from models.embeddings import calculate_similarity
from services.recommendations import generate_recommendations
from services.gap_analysis import analyze_gaps


def analyze_results(user_idea, results):

    if not results:
        recommendations = generate_recommendations(
            user_idea,
            []
        )

        gaps = analyze_gaps(
            user_idea,
            []
        )

        return {
            "originality_indicator": 100,
            "matches": [],
            "recommendations": recommendations,
            "gaps": gaps,
            "message": "No similar results were found."
        }

    texts = []

    for result in results:

        title = result.get("title") or ""
        description = result.get("description") or ""

        texts.append(
            f"{title}. {description}"
        )

    # Calculate semantic similarity
    scores = calculate_similarity(
        user_idea,
        texts
    )

    matches = []

    for result, score in zip(results, scores):

        match = result.copy()

        match["similarity"] = round(
            float(score) * 100,
            2
        )

        matches.append(match)

    # Highest similarity first
    matches.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    # Highest similarity
    highest_similarity = matches[0]["similarity"]

    # MVP originality indicator
    originality_indicator = round(
        max(0, 100 - highest_similarity),
        2
    )

    # Generate differentiation recommendations
    recommendations = generate_recommendations(
        user_idea,
        matches
    )

    # Analyze potential gaps
    gaps = analyze_gaps(
        user_idea,
        matches
    )

    return {
        "originality_indicator": originality_indicator,
        "matches": matches,
        "recommendations": recommendations,
        "gaps": gaps
    }