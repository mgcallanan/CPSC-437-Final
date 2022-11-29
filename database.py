#!/usr/bin/env python

from sqlite3 import connect
from contextlib import closing


_DATABASE_URL = "file:recommender.db"


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

