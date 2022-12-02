#!/usr/bin/env python

from sqlite3 import connect
from contextlib import closing


_DATABASE_URL = "file:recommender.db"

class Pairing:
    def __init__(self, title, variety, cheese_list):
        self.title = title
        self.variety = variety
        self.cheese_list = cheese_list


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

            query_args = {"name": name,
                          "milk_type": milk_type,
                          "flavor_notes": flavor_notes,
                          "texture": texture,
                          "wine": wine,
                          "accomps": accomps,
                          "beer": beer}

            cursor.execute(query_str, query_args)

        connection.commit()

    return 0

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
                print(row)
                pairing = Pairing(str(row[0]), str(row[1]), str(row[2]))
                pairings.append(pairing)
                row = cursor.fetchone()

        return pairings

