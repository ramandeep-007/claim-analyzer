import requests
import time
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

def search_semantic_scholar(query, limit=20, api_key=None, max_retries=5):

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





model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

claim = "Drinking coffee before exercise increases fat burning."

papers = search_semantic_scholar(
    "coffee exercise fat burning",
    api_key=api_key
)

claim_embedding = model.encode(claim)

for paper in papers:
    abstract = paper.get("abstract")

    if abstract:
        paper_embedding = model.encode(abstract)

        similarity = model.similarity(
            claim_embedding,
            paper_embedding
        )

        paper["similarity"] = float(similarity[0][0])
    else:
        paper["similarity"] = None

papers.sort(
    key=lambda paper: paper["similarity"]
    if paper["similarity"] is not None else -1,
    reverse=True
)

top_papers = papers[:5]

print("\nRanked Papers:\n")

for i, paper in enumerate(top_papers, start=1):
    if paper["similarity"] is not None:
        print(
        f"{i}. {paper['title']} "
        f"→ similarity: {paper['similarity']:.4f}"
    )
    else:
        print(
        f"{i}. {paper['title']} "
        f"→ similarity: unavailable (no abstract)"
    )