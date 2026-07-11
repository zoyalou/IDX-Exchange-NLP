# Week 3: Entity Extraction Error Analysis

## Results

| Field     | Precision | Recall | F1     |
|-----------|-----------|--------|--------|
| bedrooms  | 96.20%    | 60.80% | 74.51% |
| bathrooms | 91.55%    | 65.00% | 76.02% |
| price     | 0.00%     | 0.00%  | 0.00%  |
| sqft      | 74.29%    | 69.33% | 71.72% |

None of these hit the 85% F1 target. Below are the drivers.

## Known limitations of this evaluation
- `entity_labels.csv` was generated via a semi-automated prefill (broader
  regex patterns) followed by partial manual review due to time constraints.
  Not all 250 rows received full correction, so these numbers are
  directionally indicative rather than fully precise.
- Price shows 0% because remarks text almost never states price directly —
  it lives in a separate database field (L_SystemPrice). This metric isn't
  meaningful given how few ground-truth price mentions exist in the sample.

## Observed failure patterns
1. **High precision, lower recall on bedrooms/bathrooms**: when the
   extractor finds a value it's usually correct (96% / 92% precision), but
   it misses stated values in ~35-40% of cases (61% / 65% recall). This
   points to phrasing patterns not covered by the current regex set (e.g.
   fractional bathrooms like "2 1/2 bathrooms", hyphenated forms like
   "2-bath" without "room").
2. **Sqft is the weakest field on both precision and recall.** When a
   remark mentions multiple square-footage figures (garage size, lot size,
   living space), simple regex extraction can grab the wrong one.
3. **Fractional bathrooms** ("X 1/2 bathrooms") are captured as the integer
   part only, dropping the .5 — a direct cause of bathroom recall/precision
   loss.

## Next steps if revisited
- Normalize "X 1/2" phrasing to X.5 in the bathroom extractor.
- Add context filtering to sqft extraction (exclude matches near "garage"
  or "lot") to reduce false positives.
- Add hyphenated pattern variants ("2-bath", "3-bed") to bedroom/bathroom
  regex.
- Complete full manual review of the labeled dataset for a more reliable
  F1 baseline.
- Exclude price from F1 reporting, or evaluate it separately against the
  database price field rather than the remarks text.