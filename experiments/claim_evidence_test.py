from sentence_transformers import SentenceTransformer

claim="Drinking coffee before exercise increases fat burning."

evidence=["Caffeine consumption before exercise may increase fat oxidation.",
    "Caffeine consumption before exercise showed no significant effect on fat oxidation.",
    "Regular exercise is associated with improved cardiovascular health."
    ]

model=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

claim_embedding= model.encode(claim)

print("\nClaim-Evidence Similarity:\n")

for statement in evidence:
    evidence_embedding=model.encode(statement)

    similarity=model.similarity(claim_embedding,evidence_embedding)

    print(f"Evidence: {statement}")
    print(f"Similarity: {float(similarity[0][0]):.4f}")
    print()