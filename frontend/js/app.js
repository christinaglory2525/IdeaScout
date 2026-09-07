// ========================================
// IDEASCOUT FRONTEND
// ========================================


// ========================================
// INDEX PAGE
// ========================================

const ideaInput = document.getElementById("ideaInput");
const charCount = document.getElementById("charCount");
const checkIdeaBtn = document.getElementById("checkIdeaBtn");


if (ideaInput && charCount) {

    // Character counter

    ideaInput.addEventListener("input", function () {

        const length = ideaInput.value.length;

        charCount.textContent = `${length} / 1000`;

    });


    // Analyze idea

    checkIdeaBtn.addEventListener("click", async function () {

        const idea = ideaInput.value.trim();


        if (idea.length < 10) {

            alert("Please enter a more detailed idea.");

            return;

        }


        checkIdeaBtn.disabled = true;

        checkIdeaBtn.textContent = "ANALYZING...";


        try {

            const response = await fetch(
                "https://ideascout-kj2g.onrender.com/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        idea: idea
                    })
                }
            );


            if (!response.ok) {

                throw new Error(
                    `Backend error: ${response.status}`
                );

            }


            const data = await response.json();


            // Save result

            localStorage.setItem(
                "ideaScoutResult",
                JSON.stringify(data)
            );


            // Go to results

            window.location.href = "results.html";


        } catch (error) {

            console.error(error);

            alert(
                "Could not connect to IdeaScout backend."
            );


            checkIdeaBtn.disabled = false;

            checkIdeaBtn.textContent =
                "CHECK MY IDEA →";

        }

    });

}


// ========================================
// RESULTS PAGE
// ========================================

const resultIdea =
    document.getElementById("resultIdea");


if (resultIdea) {

    const savedResult =
        localStorage.getItem("ideaScoutResult");


    if (!savedResult) {

        resultIdea.textContent =
            "No analysis found. Please check an idea first.";

    } else {

        const data =
            JSON.parse(savedResult);


        displayResults(data);

    }

}


// ========================================
// DISPLAY RESULTS
// ========================================

function displayResults(data) {

    // Idea

    document.getElementById("resultIdea")
        .textContent = data.idea || "No idea provided.";


    // Score

    const score =
        Number(data.originality_indicator || 0);


    document.getElementById("scoreNumber")
        .textContent = score.toFixed(1);


    // Score message

    let title = "";
    let description = "";


    if (score >= 70) {

        title = "Highly Original";

        description =
            "Your idea appears to have relatively low similarity to the searched existing work.";

    }

    else if (score >= 40) {

        title = "Moderately Original";

        description =
            "Your idea has some similarities with existing work, but there may be room for differentiation.";

    }

    else {

        title = "Highly Similar";

        description =
            "Several existing solutions are similar to your idea. Consider the suggested gaps and improvements.";

    }


    document.getElementById("scoreTitle")
        .textContent = title;


    document.getElementById("scoreDescription")
        .textContent = description;


    // Matches

    displayMatches(data.matches || []);


    // Gaps

    displayGaps(data.gaps || []);


    // Recommendations

    displayRecommendations(
        data.recommendations || []
    );

}


// ========================================
// MATCHES
// ========================================

function displayMatches(matches) {

    const container =
        document.getElementById("matchesContainer");


    container.innerHTML = "";


    if (matches.length === 0) {

        container.innerHTML =
            "<p>No similar results found.</p>";

        return;

    }


    matches.forEach(function (match) {

        const card =
            document.createElement("div");

        card.className = "result-card";


        const similarity =
            Number(match.similarity || 0);


        card.innerHTML = `

            <div class="result-top">

                <div>

                    <h3>
                        ${escapeHTML(match.title || "Untitled")}
                    </h3>

                    <p>
                        ${escapeHTML(match.description || "No description available.")}
                    </p>

                </div>

                <div class="similarity">
                    ${similarity.toFixed(1)}%
                </div>

            </div>

            <span class="source">
                ${escapeHTML(match.source || "Unknown")}
            </span>

        `;


        container.appendChild(card);

    });

}


// ========================================
// GAPS
// ========================================

function displayGaps(gaps) {

    const container =
        document.getElementById("gapsContainer");


    if (gaps.length === 0) {

        container.innerHTML =
            "<p>No major gaps identified.</p>";

        return;

    }


    let html = "<ul>";


    gaps.forEach(function (gap) {

        html += `
            <li>
                ${escapeHTML(String(gap))}
            </li>
        `;

    });


    html += "</ul>";


    container.innerHTML = html;

}


// ========================================
// RECOMMENDATIONS
// ========================================

function displayRecommendations(recommendations) {

    const container =
        document.getElementById(
            "recommendationsContainer"
        );


    container.innerHTML = "";


    if (recommendations.length === 0) {

        container.innerHTML =
            "<p>No recommendations available.</p>";

        return;

    }


    recommendations.forEach(function (recommendation) {

        const card =
            document.createElement("div");

        card.className = "result-card";


        card.innerHTML = `

            <h3>
                ${escapeHTML(
                    recommendation.title ||
                    "Recommendation"
                )}
            </h3>

            <p>
                ${escapeHTML(
                    recommendation.description ||
                    ""
                )}
            </p>

        `;


        container.appendChild(card);

    });

}


// ========================================
// SECURITY HELPER
// ========================================

function escapeHTML(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}