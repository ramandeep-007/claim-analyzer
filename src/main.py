import string
import spacy
import os
import requests
import time
from dotenv import load_dotenv


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


def search_semantic_scholar(query, api_key=None, limit=5, max_retries=5):

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


x = search_semantic_scholar(
    clean_text,
    api_key=api_key
)

print(x)