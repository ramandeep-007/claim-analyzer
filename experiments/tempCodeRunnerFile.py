import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

def search_semantic_scholar(query, limit=5, api_key=None, max_retries=5):

    url = "https://api.semanticscholar.org/graph/v1/paper/search"


    params = {
        "query": query,
        "limit": limit,
        "fields": "title,year,authors,abstract,citationCount"
    }

    l_result = []

    headers = {"x-api-key": api_key} if api_key else {}

    for attempt in range(max_retries):

        response = requests.get(
            url,
            params=params,
            headers=headers
        )


        if response.status_code == 429:
            wait = 5 * (attempt + 1)
            print(f"Rate limited. Waiting {wait}s before retrying...")
            time.sleep(wait)
            continue

        response.raise_for_status()

        data = response.json()

        for paper in data.get("data", []):

            title = paper.get("title", "No title")
            year = paper.get("year", "n/a")
            authors = paper.get("authors", [])
            abstract = paper.get("abstract", "n/a")
            citationCount = paper.get("citationCount", 0)

            result = {
                "title": title,
                "year": year,
                "authors": authors,
                "abstract": abstract,
                "citationCount": citationCount
            }

            l_result.append(result)

        return l_result

    print("Failed after multiple retries due to rate limiting.")
    return []


claim_concepts = ["coffee", "exercise", "fat", "burning"]

paper_text = """
Caffeine consumption before exercise may affect fat oxidation
and energy expenditure.
"""

score = 0

for concept in claim_concepts:
    if concept in paper_text.lower():
        score += 1

print("Relevance score:", score)