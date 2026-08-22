import requests


def search_crossref(query):
    try:
        url = "https://api.crossref.org/works"

        params = {
            "query": query,
            "rows": 5,
            "sort": "published",
            "order": "desc"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for item in data["message"]["items"]:

            title = item.get("title", ["Unknown"])[0]

            published = item.get(
                "published",
                {}
            ).get(
                "date-parts",
                [["Unknown"]]
            )[0]

            year = published[0] if published else "Unknown"

            doi = item.get(
                "DOI",
                ""
            )

            results.append({
                "title": title,
                "year": year,
                "doi": doi
            })

        return results

    except Exception as e:

        return {
            "error": str(e)
        }