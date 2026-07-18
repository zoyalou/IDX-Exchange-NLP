import re

class QueryParser:
    def parse(self, query):
        filters = {}
        query_lower = query.lower()

        # Price: "under $700k", "below 500k", "less than $1.2m"
        if match := re.search(r'(?:under|below|less than)\s+\$?(\d+(?:\.\d+)?)\s*([km]?)', query_lower):
            filters['price_max'] = self._parse_number(match.group(1), match.group(2))

        if match := re.search(r'(?:over|above|more than)\s+\$?(\d+(?:\.\d+)?)\s*([km]?)', query_lower):
            filters['price_min'] = self._parse_number(match.group(1), match.group(2))

        if match := re.search(r'between\s+\$?(\d+(?:\.\d+)?)\s*([km]?)\s+and\s+\$?(\d+(?:\.\d+)?)\s*([km]?)', query_lower):
            filters['price_min'] = self._parse_number(match.group(1), match.group(2))
            filters['price_max'] = self._parse_number(match.group(3), match.group(4))

        # Bedrooms: "3 bed", "3+ bed", "3 bedroom"
        if match := re.search(r'(\d+)\+?\s*(?:bed|br|bedroom)s?', query_lower):
            if '+' in query_lower[match.start():match.end()]:
                filters['bedrooms_min'] = int(match.group(1))
            else:
                filters['bedrooms'] = int(match.group(1))

        # Bathrooms
        if match := re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:bath|ba)s?', query_lower):
            if '+' in query_lower[match.start():match.end()]:
                filters['bathrooms_min'] = float(match.group(1))
            else:
                filters['bathrooms'] = float(match.group(1))

        # City: "in Irvine", "in Los Angeles"
        if match := re.search(r'\bin\s+([a-z\s]+?)(?:\s+under|\s+over|\s+with|\s+near|$)', query_lower):
            filters['city'] = match.group(1).strip().title()

        # Amenities (simple keyword presence)
        amenity_map = {
            'pool': 'pool', 'fireplace': 'fireplace', 'garage': 'garage',
            'view': 'view', 'spa': 'spa'
        }
        found_amenities = [v for k, v in amenity_map.items() if k in query_lower]
        if found_amenities:
            filters['amenities'] = found_amenities

        # Negation: "no pool", "without garage"
        neg_amenities = []
        for k, v in amenity_map.items():
            if re.search(rf'(?:no|without|not)\s+{k}', query_lower):
                neg_amenities.append(v)
                if v in filters.get('amenities', []):
                    filters['amenities'].remove(v)
        if neg_amenities:
            filters['amenities_exclude'] = neg_amenities

        return filters

    def _parse_number(self, num_str, suffix):
        num = float(num_str)
        if suffix == 'k':
            num *= 1000
        elif suffix == 'm':
            num *= 1000000
        return int(num)

    def to_sql(self, filters):
        conditions = []
        params = []

        if 'price_max' in filters:
            conditions.append('L_SystemPrice <= %s')
            params.append(filters['price_max'])
        if 'price_min' in filters:
            conditions.append('L_SystemPrice >= %s')
            params.append(filters['price_min'])
        if 'bedrooms' in filters:
            conditions.append('L_Keyword2 = %s')
            params.append(filters['bedrooms'])
        if 'bedrooms_min' in filters:
            conditions.append('L_Keyword2 >= %s')
            params.append(filters['bedrooms_min'])
        if 'bathrooms' in filters:
            conditions.append('LM_Dec_3 = %s')
            params.append(filters['bathrooms'])
        if 'bathrooms_min' in filters:
            conditions.append('LM_Dec_3 >= %s')
            params.append(filters['bathrooms_min'])
        if 'city' in filters:
            conditions.append('L_City = %s')
            params.append(filters['city'])
        if 'amenities' in filters:
            for a in filters['amenities']:
                if a == 'pool':
                    conditions.append("PoolPrivateYN = 'Y'")
                elif a == 'fireplace':
                    conditions.append("FireplaceYN = 'Y'")
                elif a == 'garage':
                    conditions.append("GarageYN = 1")

        where_clause = ' AND '.join(conditions) if conditions else '1=1'
        sql = f"SELECT * FROM rets_property WHERE {where_clause}"
        return sql, params