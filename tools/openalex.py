import requests


def search_openalex(query):

    try:

        url = "https://api.openalex.org/works"

        params = {
            "search": query,
            "per-page": 5
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data.get("results", []):

            results.append({
                "title": item.get(
                    "display_name",
                    "Unknown"
                ),
                "publication_date": item.get(
                    "publication_date",
                    "Unknown"
                ),
                "doi": item.get(
                    "doi",
                    ""
                )
            })

        return results

    except Exception as e:

        return {
            "error": str(e)
        }