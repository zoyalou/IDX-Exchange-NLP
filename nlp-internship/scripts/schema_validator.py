import mysql.connector

class SchemaValidator:
    def __init__(self):
        conn = mysql.connector.connect(
            host='localhost', user='root', password='root', database='real_estate'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT L_City FROM rets_property WHERE L_City IS NOT NULL")
        self.valid_cities = set(row[0] for row in cursor.fetchall())
        conn.close()

    def validate_query(self, filters):
        errors = []

        if 'city' in filters:
            if filters['city'] not in self.valid_cities:
                errors.append(f"City '{filters['city']}' not found in database")

        for key in ['price_max', 'price_min']:
            if key in filters:
                if filters[key] < 50000 or filters[key] > 20000000:
                    errors.append(f"Price {filters[key]} outside typical range")

        for key in ['bedrooms', 'bedrooms_min']:
            if key in filters:
                if filters[key] < 1 or filters[key] > 10:
                    errors.append(f"Bedroom count {filters[key]} seems invalid")

        for key in ['bathrooms', 'bathrooms_min']:
            if key in filters:
                if filters[key] < 1 or filters[key] > 10:
                    errors.append(f"Bathroom count {filters[key]} seems invalid")

        return len(errors) == 0, errors