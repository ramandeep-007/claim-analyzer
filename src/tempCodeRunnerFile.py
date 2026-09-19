import requests
import time

def search_semantic_scholar(query, limit=5, api_key=None, max_retries=3):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,authors"
    }
    headers = {"x-api-key": api_key} if api_key else {}

    for attempt in range(max_retries):
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 429:
            wait = 5 * (attempt + 1)  # simple backoff: 5s, 10s, 15s
            print(f"Rate limited. Waiting {wait}s before retrying...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        data = response.json()

        for i, paper in enumerate(data.get("data", []), start=1):
            title = paper.get("title", "No title")
            year = paper.get("year", "n/a")
            print(f"{i}. {title} ({year})")
        return

    print("Failed after multiple retries due to rate limiting.")

search_semantic_scholar("caffeine before exercise fat oxidation")