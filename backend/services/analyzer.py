from models.embeddings import calculate_similarity


def analyze_results(user_idea, results):

    if not results:
        return {
            "originality_indicator": 100,
            "matches": [],
            "message": "No similar results were found."
        }

    texts = []

    for result in results:
        title = result.get("title") or ""
        description = result.get("description") or ""

        texts.append(f"{title}. {description}")

    scores = calculate_similarity(user_idea, texts)

    matches = []

    for result, score in zip(results, scores):

        match = result.copy()

        match["similarity"] = round(float(score) * 100, 2)

        matches.append(match)

    # Highest similarity first
    matches.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    highest_similarity = matches[0]["similarity"]

    # Temporary MVP indicator
    originality_indicator = round(
        max(0, 100 - highest_similarity),
        2
    )

    return {
        "originality_indicator": originality_indicator,
        "matches": matches
    }