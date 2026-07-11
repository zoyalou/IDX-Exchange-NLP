import sys
sys.path.append('scripts')
import pandas as pd
import pytest
from text_cleaning import TextCleaner

cleaner = TextCleaner()

def test_price_k():
    assert '450000' in cleaner.normalize_prices('priced at 450k')

def test_price_m():
    assert '1200000' in cleaner.normalize_prices('$1.2m home')

def test_price_uppercase_k():
    assert '450000' in cleaner.normalize_prices('priced at 450K')

def test_abbrev_br():
    assert 'bedroom' in cleaner.expand_abbreviations('3 br home')

def test_abbrev_ba():
    assert 'bathroom' in cleaner.expand_abbreviations('2 ba')

def test_html_removed():
    assert '<' not in cleaner.remove_html('<p>Nice home</p>')

def test_sqft_normalization():
    assert 'square feet' in cleaner.normalize_measurements('2,000 sqft home')

def test_empty_string():
    assert cleaner.clean_text('') == ''

def test_non_string_input():
    assert cleaner.clean_text(None) is None

def test_already_clean_text():
    result = cleaner.clean_text('Beautiful home with great view')
    assert 'Beautiful home' in result

def test_profile_has_null_rate():
    df = pd.DataFrame({'remarks': ['a', None, 'b']})
    profile = cleaner.profile_column(df, 'remarks')
    assert 'null_rate' in profile
    assert profile['null_rate'] == 1/3

def test_profile_avg_length():
    df = pd.DataFrame({'remarks': ['abc', 'de']})
    profile = cleaner.profile_column(df, 'remarks')
    assert profile['avg_length'] == 2.5

@pytest.mark.parametrize("input_text,expected_fragment", [
    ("mbr with fp", "master bedroom"),
    ("lg kit", "large"),
    ("w/ pool", "with pool"),
    ("upgr kitchen", "upgraded kitchen"),
    ("renov bath", "renovated"),
    ("nr schools", "near schools"),
    ("appx 2000 sqft", "approximately"),
    ("2 bd 1 ba", "bedroom"),
    ("hoa fees low", "homeowners association"),
    ("gar 2 car", "garage"),
])
def test_abbrev_cases(input_text, expected_fragment):
    result = cleaner.expand_abbreviations(input_text)
    assert expected_fragment in result

@pytest.mark.parametrize("price_text,expected", [
    ("100k", "100000"),
    ("999k", "999000"),
    ("2.5m", "2500000"),
    ("0.5m", "500000"),
])
def test_price_cases(price_text, expected):
    assert expected in cleaner.normalize_prices(price_text)