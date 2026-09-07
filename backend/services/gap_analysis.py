def analyze_gaps(user_idea, matches):

    if not matches:
        return [
            "No closely related solutions were found in the searched sources.",
            "Clearly define the target users and core technology.",
            "Validate the idea with additional research before implementation."
        ]

    top_matches = matches[:5]

    combined_text = " ".join(
        (
            (match.get("title") or "") + " " +
            (match.get("description") or "")
        ).lower()
        for match in top_matches
    )

    gaps = []

    # Camera / Computer Vision
    if "camera" in combined_text or "computer vision" in combined_text:
        gaps.append(
            "Camera-based detection is already common in the searched sources; "
            "consider differentiating through the next step after detection."
        )

    # Real-time systems
    if "real-time" in combined_text:
        gaps.append(
            "Real-time processing appears in existing solutions; "
            "consider improving reliability, latency, or offline operation."
        )

    # Mobile / Smartphone
    if "mobile" in combined_text or "smartphone" in combined_text:
        gaps.append(
            "Mobile-based approaches already exist; consider a more specialized "
            "workflow for a clearly defined user group."
        )

    # IoT / Sensors
    if "iot" in combined_text or "sensor" in combined_text:
        gaps.append(
            "Connected hardware approaches are represented; consider reducing "
            "deployment cost or improving scalability."
        )

    # General differentiation
    gaps.append(
        "Consider focusing on a specific underserved use case rather than "
        "solving the problem broadly."
    )

    gaps.append(
        "Consider adding measurable real-world improvements such as lower cost, "
        "higher reliability, faster processing, or easier deployment."
    )

    return gaps[:5]