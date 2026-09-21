from transformers import pipeline

nli=pipeline("text-classification",model="facebook/bart-large-mnli")

claim = "Drinking coffee before exercise increases fat burning."

evidence = [
    "Caffeine consumption before exercise increases fat oxidation.",
    "Caffeine consumption before exercise does not increase fat oxidation.",
    "Caffeine consumption before exercise has no effect on fat oxidation.",
    "Caffeine consumption before exercise may increase fat oxidation.",
    "Exercise improves cardiovascular health."
]

print("\nClaim-Evidence Reasoning:\n")

for statement in evidence:

    result=nli(
        {
            "text":statement,
            "text_pair":claim
        }
    )
    print(f"Evidence: {statement}")
    print(f"Result: {result}")
    print()

    