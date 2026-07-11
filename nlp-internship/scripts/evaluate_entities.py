import sys
sys.path.append('scripts')
import pandas as pd
from entity_extractor import EntityExtractor

df = pd.read_csv('data/processed/entity_labels.csv')
extractor = EntityExtractor()

fields = ['bedrooms', 'bathrooms', 'price', 'sqft']
results = {f: {'tp': 0, 'fp': 0, 'fn': 0} for f in fields}

for _, row in df.iterrows():
    extracted = extractor.extract_all(row['remarks_clean'])
    for f in fields:
        true_val = row.get(f'{f}_true')
        pred_val = extracted.get(f)
        has_true = pd.notna(true_val) and str(true_val).strip() != ''
        has_pred = pred_val is not None

        if has_true and has_pred:
            try:
                match = float(true_val) == float(pred_val)
            except ValueError:
                match = False
            if match:
                results[f]['tp'] += 1
            else:
                results[f]['fp'] += 1
                results[f]['fn'] += 1
        elif has_pred and not has_true:
            results[f]['fp'] += 1
        elif has_true and not has_pred:
            results[f]['fn'] += 1

print(f"{'Field':<12}{'Precision':<12}{'Recall':<12}{'F1':<12}")
for f in fields:
    tp, fp, fn = results[f]['tp'], results[f]['fp'], results[f]['fn']
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    print(f"{f:<12}{precision:<12.2%}{recall:<12.2%}{f1:<12.2%}")