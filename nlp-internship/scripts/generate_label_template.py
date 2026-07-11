import pandas as pd

df = pd.read_csv('data/processed/listing_sample_cleaned.csv')
df = df.dropna(subset=['remarks_clean'])

sample = df[['remarks_clean']].sample(250, random_state=1).reset_index(drop=True)
sample['bedrooms_true'] = ''
sample['bathrooms_true'] = ''
sample['price_true'] = ''
sample['sqft_true'] = ''

sample.to_csv('data/processed/entity_labels_TEMPLATE.csv', index=False)
print(f"Saved template with {len(sample)} remarks to label")