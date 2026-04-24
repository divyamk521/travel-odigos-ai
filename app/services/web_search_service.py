import requests
from app.services.search_service import build_search_query


def search_places(destination: str):
    headers = {
        "User-Agent": "travel-odigos-ai/1.0"
    }

    try:
        query = build_search_query(destination)

        search_url = "https://en.wikipedia.org/w/api.php"

        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }

        res = requests.get(search_url, params=params, headers=headers)
        data = res.json()

        titles = [item["title"] for item in data["query"]["search"][:7]]

        full_text = ""

        for title in titles:
            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
            r = requests.get(summary_url, headers=headers)

            if r.status_code == 200:
                full_text += r.json().get("extract", "") + "\n"

        return full_text

    except Exception as e:
        print("❌ Web error:", e)
        return ""