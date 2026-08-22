import requests
from datetime import date


def search_news(query, limit=5):

    today = date.today().isoformat()

    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "per-page": limit,
        "filter": f"from_publication_date:2025-01-01,to_publication_date:{today}",
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

            results.append({
                "title": work.get("title") or "Untitled",
                "date": work.get("publication_date"),
                "doi": work.get("doi")
            })

            if len(results) >= limit:
                break

        return results

    except Exception as e:

        return {
            "error": str(e)
        }


if __name__ == "__main__":

    query = input("Enter news topic: ")

    results = search_news(query)

    print("\n📰 NEWS RESULTS\n")

    # Error handling
    if isinstance(results, dict):

        print("❌ Error:", results.get("error"))

    elif not results:

        print("⚠️ No results found.")

    else:

        for i, item in enumerate(results, 1):

            print(f"{i}. {item['title']}")
            print(f"   Date: {item['date']}")
            print(f"   DOI: {item['doi']}")
            print()