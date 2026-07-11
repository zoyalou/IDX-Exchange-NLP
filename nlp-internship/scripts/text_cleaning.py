import re
import pandas as pd

class TextCleaner:
    def __init__(self):
        self.abbrev_map = {
            'br': 'bedroom', 'ba': 'bathroom', 'sqft': 'square feet',
            'w/': 'with', 'w/o': 'without', 'mbr': 'master bedroom',
            'fp': 'fireplace', 'gar': 'garage', 'lg': 'large',
            'kit': 'kitchen', 'liv': 'living', 'din': 'dining',
            'ac': 'air conditioning', 'hw': 'hardwood',
            'nr': 'near', 'appx': 'approximately', 'rm': 'room',
            'bldg': 'building', 'apt': 'apartment', 'ft': 'feet',
            'mstr': 'master', 'upgr': 'upgraded', 'renov': 'renovated',
            'assoc': 'association', 'hoa': 'homeowners association',
            'yr': 'year', 'mo': 'month', 'bd': 'bedroom',
            'dr': 'dining room', 'lr': 'living room', 'cul-de-sac': 'cul de sac',
            'vw': 'view', 'lndry': 'laundry'
        }

    def normalize_unicode(self, text):
        return text.encode('ascii', 'ignore').decode('ascii') if isinstance(text, str) else text

    def normalize_prices(self, text):
        text = re.sub(r'(\d+)k', lambda m: str(int(m.group(1)) * 1000), text, flags=re.I)
        text = re.sub(r'(\d+\.?\d*)m', lambda m: str(int(float(m.group(1)) * 1000000)), text, flags=re.I)
        return text

    def normalize_measurements(self, text):
        text = re.sub(r'(\d{1,3}(?:,\d{3})*)\s*sq\.?\s*ft\.?', lambda m: f"{m.group(1).replace(',', '')} square feet", text, flags=re.I)
        return text

    def expand_abbreviations(self, text):
        for abbr, full in self.abbrev_map.items():
            pattern = re.escape(abbr)
            if abbr[0].isalnum():
                pattern = r'\b' + pattern
            if abbr[-1].isalnum():
                pattern = pattern + r'\b'
            else:
                pattern = pattern + r'(?=\s|$)'
            text = re.sub(pattern, full, text, flags=re.I)
        return text

    def remove_html(self, text):
        return re.sub(r'<[^>]+>', '', text)

    def clean_text(self, text):
        if not isinstance(text, str):
            return text
        text = self.remove_html(text)
        text = self.normalize_unicode(text)
        text = self.normalize_prices(text)
        text = self.normalize_measurements(text)
        text = self.expand_abbreviations(text)
        return text.strip()

    def profile_column(self, df, column_name):
        return {
            'null_rate': df[column_name].isnull().mean(),
            'avg_length': df[column_name].str.len().mean(),
            'price_mentions': df[column_name].str.contains(r'\$\d', na=False).sum(),
            'has_html': df[column_name].str.contains('<', na=False).sum(),
        }

if __name__ == "__main__":
    df = pd.read_csv('data/processed/listing_sample.csv')
    cleaner = TextCleaner()

    profile = cleaner.profile_column(df, 'remarks')
    print("Profile before cleaning:", profile)

    df['remarks_clean'] = df['remarks'].apply(cleaner.clean_text)
    df.to_csv('data/processed/listing_sample_cleaned.csv', index=False)
    print("Saved cleaned dataset")