import requests


def search_semantic_scholar(query):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    params = {
        "query": query,
        "limit": 5,
        "fields": "title,abstract,url,year,authors"
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            return []

        data = response.json()

        results = []

        for paper in data.get("data", []):
            results.append({
                "source": "Research Paper",
                "title": paper.get("title"),
                "description": paper.get("abstract") or "",
                "url": paper.get("url"),
                "year": paper.get("year")
            })

        return results

    except Exception:
        return []


def search_openalex(query):
    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": 5
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            return []

        data = response.json()

        results = []

        for paper in data.get("results", []):
            abstract = ""

            # OpenAlex stores abstracts as an inverted index
            abstract_index = paper.get("abstract_inverted_index")

            if abstract_index:
                words = []

                for word, positions in abstract_index.items():
                    for position in positions:
                        words.append((position, word))

                words.sort()

                abstract = " ".join(
                    word for position, word in words
                )

            results.append({
                "source": "Research Paper",
                "title": paper.get("title"),
                "description": abstract,
                "url": paper.get("doi") or paper.get("id"),
                "year": paper.get("publication_year")
            })

        return results

    except Exception:
        return []


def search_github(query):
    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": 5
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            return []

        data = response.json()

        results = []

        for repo in data.get("items", []):
            results.append({
                "source": "GitHub",
                "title": repo.get("full_name"),
                "description": repo.get("description") or "",
                "url": repo.get("html_url"),
                "year": repo.get("created_at", "")[:4]
            })

        return results

    except Exception:
        return []


def search_all(query):
    results = []

    # Search research papers
    results.extend(search_semantic_scholar(query))
    results.extend(search_openalex(query))

    # Search GitHub using the full idea
    github_results = search_github(query)

    # If no results, try a shorter query
    if not github_results:
        words = query.split()

        if len(words) > 6:
            short_query = " ".join(words[:6])
        else:
            short_query = query

        github_results = search_github(short_query)

    # If still no results, search using important keywords
    if not github_results:

        keywords = [
            "AI",
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "waste",
            "garbage",
            "sorting",
            "classification",
            "detection",
            "camera",
            "smart",
            "automation"
        ]

        found_keywords = []

        query_lower = query.lower()

        for keyword in keywords:
            if keyword.lower() in query_lower:
                found_keywords.append(keyword)

        if found_keywords:
            github_query = " ".join(found_keywords[:4])
            github_results = search_github(github_query)

    results.extend(github_results)

    return results