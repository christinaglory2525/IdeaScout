def generate_recommendations(user_idea, matches):
    """
    Generate recommendations to make an idea more differentiated
    based on the most similar existing projects and papers.
    """

    if not matches:
        return [
            {
                "title": "Explore the idea further",
                "description": "No closely related sources were found. Define the target users, core technology, and unique value clearly before implementation."
            }
        ]

    # Look at the strongest matches
    top_matches = matches[:5]

    combined_text = " ".join(
        (
            (match.get("title") or "") + " " +
            (match.get("description") or "")
        ).lower()
        for match in top_matches
    )

    recommendations = []

    # --------------------------------------------------
    # 1. Technology differentiation
    # --------------------------------------------------

    if any(word in combined_text for word in [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "computer vision"
    ]):
        recommendations.append({
            "title": "Add a stronger technical layer",
            "description": (
                "Existing solutions already use AI-based approaches. "
                "Consider adding a distinctive technical capability such as "
                "edge AI, multimodal analysis, explainable AI, adaptive learning, "
                "or real-time processing."
            )
        })
    else:
        recommendations.append({
            "title": "Introduce intelligent automation",
            "description": (
                "Consider adding an AI or automation component that solves "
                "a specific limitation of existing approaches."
            )
        })

    # --------------------------------------------------
    # 2. User / application differentiation
    # --------------------------------------------------

    if any(word in combined_text for word in [
        "mobile",
        "smartphone",
        "app",
        "web",
        "platform"
    ]):
        recommendations.append({
            "title": "Differentiate through the user experience",
            "description": (
                "Several existing solutions provide similar functionality "
                "through applications or platforms. Focus on a specific user "
                "group and design a workflow specifically for their needs."
            )
        })
    else:
        recommendations.append({
            "title": "Target a specific user group",
            "description": (
                "Instead of solving the problem broadly, focus on a clearly "
                "defined user group or environment. A specialized solution "
                "can create stronger differentiation."
            )
        })

    # --------------------------------------------------
    # 3. Real-world differentiation
    # --------------------------------------------------

    if any(word in combined_text for word in [
        "real-time",
        "camera",
        "sensor",
        "iot",
        "hardware",
        "robot"
    ]):
        recommendations.append({
            "title": "Improve real-world deployment",
            "description": (
                "Existing solutions already address real-world deployment. "
                "Consider improving cost, reliability, offline operation, "
                "energy efficiency, scalability, or ease of deployment."
            )
        })
    else:
        recommendations.append({
            "title": "Add measurable real-world impact",
            "description": (
                "Define measurable outcomes such as time saved, cost reduced, "
                "accuracy improved, or resources saved. This can make the "
                "solution more practically valuable."
            )
        })

    # --------------------------------------------------
    # 4. Avoid duplicate recommendations
    # --------------------------------------------------

    unique = []
    seen = set()

    for recommendation in recommendations:
        title = recommendation["title"]

        if title not in seen:
            seen.add(title)
            unique.append(recommendation)

    return unique[:3]