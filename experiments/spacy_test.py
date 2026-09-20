import spacy
from sentence_transformers import SentenceTransformer

model=SentenceTransformer("sentence-transformers/all-MiniLm-L6-v2")

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Drinking coffee before exercise increases fat burning.")

# keywords = []

# for token in doc:
#     if token.pos_ in ["NOUN", "VERB", "ADJ"]:
#         keywords.append(token.lemma_)

# query=" ".join(keywords)

# print("\nSearch Query")
# print(query)
# print("\nNoun Chunks:")

# for chunk in doc.noun_chunks:
#     print(chunk.text)

sentences = [
    "coffee",
    "caffeine",
    "fat burning",
    "fat oxidation"
]

embeddings=model.encode(sentences)

similarities=model.similarity(embeddings,embeddings)

print(similarities)