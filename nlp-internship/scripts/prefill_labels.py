import re
import pandas as pd

def prefill_bedrooms(text):
    patterns = [
        r'(\d+)\s*(?:bed|br|bedroom)s?\b',
        r'(\d+)bd\b',
        r'(\d+)-bedroom',
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return int(m.group(1))
    return ''

def prefill_bathrooms(text):
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:full\s+)?bath(?:room)?s?\b',
        r'(\d+(?:\.\d+)?)\s*ba\b',
        r'(\d+)-bathroom',
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return float(m.group(1))
    return ''

def prefill_sqft(text):
    patterns = [
        r'([\d,]{3,6})\s*(?:square feet|sq\.?\s*ft\.?|sqft)',
        r'approximately\s+([\d,]{3,6})',
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return int(m.group(1).replace(',', ''))
    return ''

def prefill_price(text):
    m = re.search(r'\$\s?([\d,]{5,10})', text)
    if m:
        return int(m.group(1).replace(',', ''))
    return ''

df = pd.read_csv('data/processed/entity_labels_TEMPLATE.csv')
df['bedrooms_true'] = df['remarks_clean'].apply(prefill_bedrooms)
df['bathrooms_true'] = df['remarks_clean'].apply(prefill_bathrooms)
df['sqft_true'] = df['remarks_clean'].apply(prefill_sqft)
df['price_true'] = df['remarks_clean'].apply(prefill_price)

df.to_csv('data/processed/entity_labels_PREFILLED.csv', index=False)
print("Saved entity_labels_PREFILLED.csv")