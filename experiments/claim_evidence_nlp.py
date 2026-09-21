import spacy

nlp = spacy.load("en_core_web_sm")

claim = "Drinking coffee before exercise increases fat burning."

evidence = [
    "Caffeine consumption before exercise may increase fat oxidation.",
    "Caffeine consumption before exercise showed no significant effect on fat oxidation.",
    "Regular exercise is associated with improved cardiovascular health."
]

print("CLAIM\n")

doc = nlp(claim)

for token in doc:
    print(token.text, "->", token.head.text, "->", token.dep_)

print("\nEVIDENCE\n")

for statement in evidence:
    print("\n", statement)

    doc = nlp(statement)

    for token in doc:
        print(token.text, "->", token.head.text, "->", token.dep_)