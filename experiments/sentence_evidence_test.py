import spacy
from sentence_transformers import SentenceTransformer
from transformers import pipeline

nli_model = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli"
)

nlp = spacy.load("en_core_web_sm")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

claim = "Drinking coffee before exercise increases fat burning."

abstract = """
Caffeine consumption before exercise may affect fat oxidation and energy expenditure.
Previous studies have reported that caffeine intake can alter substrate utilization during exercise.
The study included trained participants who completed exercise trials after caffeine consumption.
The results showed that caffeine increased fat oxidation during exercise.
However, the magnitude of the effect varied between individuals.
"""

doc = nlp(abstract)

claim_embedding = embedding_model.encode(claim)

print("Sentence Relevance:\n")

for i, sentence in enumerate(doc.sents, start=1):

    sentence_embedding = embedding_model.encode(sentence.text)

    similarity = embedding_model.similarity(
        claim_embedding,
        sentence_embedding
    )

    nli_result = nli_model(
        {
            "text": sentence.text,
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

    print(f"{i}. {sentence.text}")
    print(f"   Similarity: {float(similarity[0][0]):.4f}")
    print(f"   Relationship: {relationship}")
    print(f"   NLI Score: {nli_result['score']:.4f}")
    print()
