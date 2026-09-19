import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Tesla announced a new battery technology in India in 2025.")

# for token in doc:
#     print(token.text,"->",token.head.text,"->",token.dep_)

for ent in doc.ents:
    print(ent.text,ent.label_)