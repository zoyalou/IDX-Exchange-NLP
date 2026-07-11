import pandas as pd

df = pd.read_csv('data/processed/listing_sample_cleaned.csv')
df = df.dropna(subset=['remarks', 'remarks_clean'])

# Only keep rows where cleaning actually changed the text
changed = df[df['remarks'] != df['remarks_clean']]
print(f"{len(changed)} of {len(df)} remarks were changed by cleaning ({len(changed)/len(df):.1%})")

sample = changed.sample(min(10, len(changed)), random_state=1)

with open('data/processed/before_after_examples.md', 'w') as f:
    f.write("# Text Cleaning: Before / After Examples\n\n")
    f.write(f"*{len(changed)} of {len(df)} remarks ({len(changed)/len(df):.1%}) were modified by cleaning.*\n\n")
    for i, (_, row) in enumerate(sample.iterrows(), 1):
        f.write(f"## Example {i}\n\n")
        f.write(f"**Before:** {row['remarks'][:300]}\n\n")
        f.write(f"**After:** {row['remarks_clean'][:300]}\n\n")
        f.write("---\n\n")

print("Saved data/processed/before_after_examples.md")

