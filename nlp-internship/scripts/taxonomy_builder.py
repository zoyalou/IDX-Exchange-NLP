import nltk
from collections import Counter
from nltk.util import ngrams
import pandas as pd

df = pd.read_csv('data/processed/listing_sample.csv')

# Extract bigrams from remarks
all_text = ' '.join(df['remarks'].dropna().str.lower())
tokens = nltk.word_tokenize(all_text)
bigrams = list(ngrams(tokens, 2))
freq = Counter(bigrams)

# Top 200 bigrams become taxonomy seed
for bigram, count in freq.most_common(200):
    print(f"{' '.join(bigram)}: {count}")


import json

categories = {
    "property_type": ["condo", "single family", "townhouse", "duplex", "ranch"],
    "amenities": ["pool", "fireplace", "garage", "hardwood floors", "granite counters"],
    "condition": ["updated", "renovated", "move in ready", "fixer upper", "new construction"],
    "location": ["cul de sac", "corner lot", "gated community", "walk to", "near"],
    "financing": ["seller financing", "assumable loan", "no hoa", "low hoa"],
    "size_layout": ["open floor plan", "master suite", "vaulted ceilings", "bonus room"],
    "outdoor": ["backyard", "patio", "deck", "landscaped", "mountain view"],
    "urgency_marketing": ["priced to sell", "must see", "won't last", "motivated seller"]
}

terms = []
term_id = 1
for cat, words in categories.items():
    for w in words:
        terms.append({"id": f"t{term_id:04d}", "term": w, "category": cat})
        term_id += 1

for bigram, count in freq.most_common(200):
    terms.append({"id": f"t{term_id:04d}", "term": " ".join(bigram), "category": "uncategorized", "count": count})
    term_id += 1

with open("data/processed/taxonomy.json", "w") as f:
    json.dump({"terms": terms}, f, indent=2)

print(f"Wrote {len(terms)} terms to taxonomy.json")