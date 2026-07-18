import sys
sys.path.append('scripts')
import json
from query_parser import QueryParser

with open('data/processed/sample_queries.json') as f:
    data = json.load(f)

parser = QueryParser()
total = len(data['queries'])
parsed_something = 0

for item in data['queries']:
    filters = parser.parse(item['query'])
    if filters:
        parsed_something += 1
    else:
        print(f"NO FILTERS EXTRACTED: {item['query']}")

print(f"\n{parsed_something}/{total} queries produced at least one filter ({parsed_something/total:.1%})")