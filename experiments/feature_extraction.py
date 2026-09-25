from sentence_transformers import SentenceTransformer
from transformers import pipeline

data = [
    {
        "claim": "Drinking coffee before exercise increases fat burning.",
        "evidence": "Caffeine consumption before exercise increases fat oxidation.",
        "label": "SUPPORT"
    },
    {
        "claim": "Drinking coffee before exercise increases fat burning.",
        "evidence": "Caffeine consumption before exercise does not increase fat oxidation.",
        "label": "CONTRADICT"
    },
    {
        "claim": "Drinking coffee before exercise increases fat burning.",
        "evidence": "Exercise improves cardiovascular health.",
        "label": "UNCLEAR"
    },
    {
        "claim": "Regular exercise improves sleep quality.",
        "evidence": "Physical exercise has been associated with improved sleep quality.",
        "label": "SUPPORT"
    },
    {
        "claim": "Regular exercise improves sleep quality.",
        "evidence": "Exercise showed no significant improvement in sleep quality.",
        "label": "CONTRADICT"
    },
    {
        "claim": "Regular exercise improves sleep quality.",
        "evidence": "Regular exercise can improve cardiovascular fitness.",
        "label": "UNCLEAR"
    }
]

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

nli_model = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli"
)

for item in data:

    claim_embedding = embedding_model.encode(item["claim"])
    evidence_embedding = embedding_model.encode(item["evidence"])

    similarity = embedding_model.similarity(
        claim_embedding,
        evidence_embedding
    )

    nli_result = nli_model(
        {
            "text": item["evidence"],
            "text_pair": item["claim"]
        }
    )

    print("Claim:", item["claim"])
    print("Evidence:", item["evidence"])
    print(f"Similarity: {float(similarity[0][0]):.4f}")
    print(f"NLI: {nli_result['label']}")
    print(f"NLI Score: {nli_result['score']:.4f}")
    print("Actual label:", item["label"])
    print()