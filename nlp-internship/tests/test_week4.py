import sys
sys.path.append('scripts')
import pytest
from query_parser import QueryParser

parser = QueryParser()

@pytest.mark.parametrize("query,expected_key,expected_val", [
    ("3 bed 2 bath under 700k in Irvine", "bedrooms", 3),
    ("3 bed 2 bath under 700k in Irvine", "bathrooms", 2.0),
    ("3 bed 2 bath under 700k in Irvine", "price_max", 700000),
    ("homes over 1.2m", "price_min", 1200000),
    ("4+ bedrooms in Anaheim", "bedrooms_min", 4),
    ("2 bath condo in Alhambra", "bathrooms", 2.0),
    ("under 500k", "price_max", 500000),
    ("homes with pool", "amenities", ["pool"]),
    ("no pool please", "amenities_exclude", ["pool"]),
    ("home in Anaheim", "city", "Anaheim"),
])
def test_query_parsing(query, expected_key, expected_val):
    filters = parser.parse(query)
    assert expected_key in filters
    assert filters[expected_key] == expected_val

def test_sql_no_string_concat():
    filters = parser.parse("3 bed under 700k")
    sql, params = parser.to_sql(filters)
    assert '%s' in sql
    assert '700000' not in sql  # value should be in params, not the SQL string
    assert 700000 in params

def test_sql_injection_safe():
    filters = parser.parse("3 bed in Irvine")
    sql, params = parser.to_sql(filters)
    # city value should never be directly embedded in the SQL string
    assert 'Irvine' not in sql