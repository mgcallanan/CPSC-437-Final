#!/usr/bin/env python

from sqlite3 import connect
from contextlib import closing


_DATABASE_URL = "file:recommender.db"


class Pairing:
    def __init__(self, title, variety, cheese_list):
        self.title = title
        self.variety = variety
        self.cheese_list = cheese_list


class WineWithDescription:
    def __init__(self, title, variety, price, country, province, description):
        self.title = title
        self.variety = variety
        self.price = price
        self.country = country
        self.province = province
        self.description = description


def add_cheese(name, milk_type, flavor_notes, texture, wine, accomps, beer):
    """
    Runs a SQLlite query to add a new cheese into the database
    """

    with connect(_DATABASE_URL, uri=True) as connection:

        with closing(connection.cursor()) as cursor:

            query_str = """
                INSERT INTO cheeses (name, milk_type, flavor_notes, texture, wine_pairings, accompaniments, beer_pairings)
                VALUES (:name, :milk_type, :flavor_notes, :texture, :wine, :accomps, :beer)
            """

            query_args = {
                "name": name,
                "milk_type": milk_type,
                "flavor_notes": flavor_notes,
                "texture": texture,
                "wine": wine,
                "accomps": accomps,
                "beer": beer,
            }

            cursor.execute(query_str, query_args)

        connection.commit()

    return 0


def get_sql_query_with_filters(filters):
    """
    Filters dictionary has these keys:
        price_max
        price_min
        flavors
        country
        province
        variety
    """
    columns = ["title", "variety", "price", "country", "province", "review_content"]
    select_clause = "SELECT " + ", ".join(columns)
    from_clause = "FROM wines JOIN reviews ON wines.wine_id = review_id"
    where_clause = ""
    if filters:
        where_clauses = []
        for col, filt in filters.items():
            if col in ["country", "variety", "province"]:
                if filt is None:
                    continue
                where_clauses.append(f"{col} LIKE '%{filt}%'")
            if col == "flavor":
                if filt is None:
                    continue
                flavors = filters["flavor"].split(",")
                for flavor in flavors:
                    where_clauses.append(f"review_content LIKE '%{flavor}%'")
            if "price" in col:
                if col == "price_max":
                    if filt is None:
                        filters["price_max"] = "(SELECT MAX(price) FROM wines)"
                if col == "price_min":
                    if filt is None:
                        filters["price_min"] = "0"
        where_clauses.append(
            f"price BETWEEN {filters['price_min']} AND {filters['price_max']}"
        )
        where_clause = "WHERE " + " AND ".join(where_clauses)
    return " ".join([select_clause, from_clause, where_clause]) + ";"


def get_wine_from_filters(filters):
    """
    Runs a SQLlite query to get wines based on filters
    """
    wines = []

    with connect(_DATABASE_URL, uri=True) as connection:

        with closing(connection.cursor()) as cursor:
            query_string = get_sql_query_with_filters(filters)
            print(query_string)
            cursor.execute(query_string)

            row = cursor.fetchone()
            if row is None:
                return None  # wine doesnt exist

            while row is not None:
                # print(row)
                # "title", "variety", "price", "country", "province", "review_content"
                wine = WineWithDescription(
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3]),
                    str(row[4]),
                    str(row[5]),
                )
                wines.append(wine)
                row = cursor.fetchone()
        # print(wines)
        return wines


def get_cheese_pairings(wine_variety):
    """
    Runs a SQLlite query to get cheese pairings given a wine variety
    """

    pairings = []

    with connect(_DATABASE_URL, uri=True) as connection:
        wine_variety_str = f"%{wine_variety}%"

        with closing(connection.cursor()) as cursor:

            query_str = """
                SELECT wines.title, wines.variety, GROUP_CONCAT(DISTINCT cheeses.name) AS cheese_pairings FROM wines
                JOIN cheeses
                ON cheeses.wine_pairings LIKE '%'||wines.variety||'%'
                WHERE wines.variety LIKE :wine_variety
                GROUP BY wines.title
            """

            query_args = {"wine_variety": wine_variety_str}

            cursor.execute(query_str, query_args)

            row = cursor.fetchone()
            if row is None:
                return None  # wine doesnt exist

            while row is not None:
                # print(row)
                pairing = Pairing(str(row[0]), str(row[1]), str(row[2]))
                pairings.append(pairing)
                row = cursor.fetchone()

        return pairings
