import re
import pandas as pd

class EntityExtractor:
    def extract_bedrooms(self, text):
        for pattern in [r'(\d+)\s*(?:bed|br|bedroom)s?', r'(\d+)bd']:
            match = re.search(pattern, text, re.I)
            if match:
                return int(match.group(1))
        return None

    def extract_bathrooms(self, text):
        match = re.search(r'(\d+(?:\.\d+)?)\s*(?:bath|ba)s?', text, re.I)
        return float(match.group(1)) if match else None

    def extract_price(self, text):
        match = re.search(r'\$?(\d{5,})', text)
        return int(match.group(1)) if match else None

    def extract_sqft(self, text):
        match = re.search(r'(\d{3,5})\s*(?:sq\.?\s*ft|square feet)', text, re.I)
        return int(match.group(1)) if match else None

    def extract_amenities(self, text, taxonomy_terms=None):
        text_lower = text.lower()
        default = ['pool', 'fireplace', 'garage', 'hardwood floors', 'granite counters',
                    'updated kitchen', 'master suite', 'mountain view', 'gated community']
        terms = taxonomy_terms or default
        return [t for t in terms if t in text_lower]

    def extract_all(self, text):
        if not isinstance(text, str):
            return {'bedrooms': None, 'bathrooms': None, 'price': None, 'sqft': None, 'amenities': []}
        return {
            'bedrooms': self.extract_bedrooms(text),
            'bathrooms': self.extract_bathrooms(text),
            'price': self.extract_price(text),
            'sqft': self.extract_sqft(text),
            'amenities': self.extract_amenities(text)
        }


if __name__ == "__main__":
    df = pd.read_csv('data/processed/listing_sample_cleaned.csv')
    extractor = EntityExtractor()
    entities = df['remarks_clean'].apply(extractor.extract_all)
    df['bedrooms_extracted'] = entities.apply(lambda e: e['bedrooms'])
    df['bathrooms_extracted'] = entities.apply(lambda e: e['bathrooms'])
    df['price_extracted'] = entities.apply(lambda e: e['price'])
    df['sqft_extracted'] = entities.apply(lambda e: e['sqft'])
    df['amenities_extracted'] = entities.apply(lambda e: e['amenities'])
    df.to_csv('data/processed/listing_sample_entities.csv', index=False)
    print("Saved data/processed/listing_sample_entities.csv")