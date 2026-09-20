import string
import spacy
import os
import requests
import time
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


nlp = spacy.load("en_core_web_sm")


claim = input("Enter a claim: ")


clean_text = "".join(
    char for char in claim if char not in string.punctuation
).lower()


doc = nlp(clean_text)

print("\nProcessed Claim:")

for token in doc:
    print(token.text, token.pos_, token.dep_)


load_dotenv()

api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")


def search_semantic_scholar(query, api_key=None, limit=20, max_retries=5):

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

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

papers=search_semantic_scholar(clean_text,limit=20,api_key=api_key)

claim_embedding=embedding_model.encode(clean_text)

for paper in papers:

    abstract=paper.get("abstract") or None

    if abstract:
        paper_embedding=embedding_model.encode(abstract)

        similarity=embedding_model.similarity(claim_embedding,paper_embedding)

        paper['similarity']=float(similarity[0][0])

    else:
        paper['similarity']=None

papers.sort(
    key=lambda paper:paper["similarity"]
    if paper["similarity"] is not None else -1,
    reverse=True
)

top_papers=papers[:5]

print("\nTop Evidence\n")

for i,paper in enumerate(top_papers,start=1):

    print(f"{i}. {paper['title']}")

    if(paper["similarity"] is not None):
        print(f"   Similarity: {paper['similarity']:.4f}")

    else:
        print("   Similarity: unavailable (no abstract)")

    print(f"   Year: {paper['year']}")
    print()
    


