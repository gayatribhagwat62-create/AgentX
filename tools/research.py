import requests
from datetime import date


def search_research(query, limit=5):
    """
    Search scientific research published up to today.
    """

    url = "https://api.openalex.org/works"

    today = date.today().isoformat()

    params = {
        "search": query,
        "per-page": 25,
        "filter": f"from_publication_date:1900-01-01,to_publication_date:{today}",
        "sort": "publication_date:desc",
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for work in data.get("results", []):

            title = work.get("title") or "Untitled"
            publication_date = work.get("publication_date")

            if not publication_date:
                continue

            results.append({
                "title": title,
                "publication_date": publication_date,
                "doi": work.get("doi"),
            })

            if len(results) >= limit:
                break

        return results

    except requests.RequestException as e:

        return {
            "error": f"Research search failed: {str(e)}"
        }


if __name__ == "__main__":

    query = input("Enter research topic: ")

    results = search_research(query)

    print("\n🔬 RESEARCH RESULTS\n")

    if isinstance(results, dict):

        print("❌", results["error"])

    elif not results:

        print("⚠️ No valid research results found.")

    else:

        for i, paper in enumerate(results, 1):

            print(f"{i}. {paper['title']}")
            print(f"   Date: {paper['publication_date']}")
            print(f"   DOI: {paper['doi']}")
            print()