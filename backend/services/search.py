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
            print("Semantic Scholar unavailable:", response.status_code)
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

    except Exception as e:
        print("Semantic Scholar error:", e)
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
            print("OpenAlex unavailable:", response.status_code)
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

    except Exception as e:
        print("OpenAlex error:", e)
        return []


def search_github(query):
    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": 5,
        "sort": "stars",
        "order": "desc"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
            headers={
                "Accept": "application/vnd.github+json"
            }
        )

        if response.status_code != 200:
            print("GitHub unavailable:", response.status_code)
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

    except Exception as e:
        print("GitHub error:", e)
        return []


def search_all(query):
    results = []

    # -------------------------------------------------
    # 1. Research papers
    # -------------------------------------------------

    results.extend(search_semantic_scholar(query))
    results.extend(search_openalex(query))

    # -------------------------------------------------
    # 2. GitHub search
    # -------------------------------------------------

    github_results = search_github(query)

    # If full idea gives no GitHub results,
    # use a shorter version.
    if not github_results:

        words = query.split()

        if len(words) > 6:
            short_query = " ".join(words[:6])
        else:
            short_query = query

        github_results = search_github(short_query)

    # -------------------------------------------------
    # 3. Keyword fallback
    # -------------------------------------------------

    if not github_results:

        keyword_groups = [
            ["waste", "garbage", "recycling"],
            ["AI", "artificial intelligence", "machine learning"],
            ["sorting", "classification", "detection"],
            ["camera", "computer vision"]
        ]

        query_lower = query.lower()

        selected = []

        for group in keyword_groups:

            for keyword in group:

                if keyword.lower() in query_lower:
                    selected.append(keyword)
                    break

        if selected:

            github_query = " ".join(selected[:4])

            print("GitHub fallback query:", github_query)

            github_results = search_github(github_query)

    # Add GitHub results
    results.extend(github_results)

    # -------------------------------------------------
    # 4. Remove duplicate results
    # -------------------------------------------------

    unique_results = []
    seen = set()

    for result in results:

        key = (
            result.get("source"),
            result.get("title")
        )

        if key not in seen:
            seen.add(key)
            unique_results.append(result)

    print("Total search results:", len(unique_results))

    return unique_results