from sentence_transformers import SentenceTransformer
from transformers import pipeline

claim = "Drinking coffee before exercise increases fat burning."

evidence = [
    """
    Caffeine consumption before exercise may affect fat oxidation
    and energy expenditure. Previous studies have reported that
    caffeine intake can alter substrate utilization during exercise,
    although the magnitude of the effect varies between individuals.
    """,

    """
    This study investigated the effects of caffeine consumption
    before exercise on fat oxidation. The results showed no
    significant difference in fat oxidation between the caffeine
    and placebo conditions.
    """
]

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

nli_model = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli"
)

claim_embedding = embedding_model.encode(claim)

print("\nClaim-Evidence Analysis:\n")

for statement in evidence:

    evidence_embedding = embedding_model.encode(statement)

    similarity = embedding_model.similarity(
        claim_embedding,
        evidence_embedding
    )

    nli_result = nli_model(
        {
            "text": statement,
            "text_pair": claim
        }
    )

    label = nli_result["label"]

    if label == "entailment":
        relationship = "SUPPORT"

    elif label == "contradiction":
        relationship = "CONTRADICT"

    else:
        relationship = "UNCLEAR"

    result = {
        "evidence": statement,
        "similarity": float(similarity[0][0]),
        "relationship": relationship,
        "nli_score": nli_result["score"]
    }

    print(result)