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

for item in data:
    print(item)