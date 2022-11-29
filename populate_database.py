""" Script to populate recommender db """
import csv
from sqlite3 import connect
from contextlib import closing


# -----------------------------------------------------------------------

_DATABASE_URL = "file:recommender.db"

# -----------------------------------------------------------------------


class Wine:
    def __init__(self, wine_id, price, country, variety, province):
        self.wine_id = wine_id
        self.price = price
        self.country = country
        self.variety = variety
        self.province = province


class Review:
    def __init__(self, review_id, wine_id, review_content, reviewer_id):
        self.review_id = review_id
        self.wine_id = wine_id
        self.review_content = review_content
        self.reviewer_id = reviewer_id


def add_to_wines(wine):
    with connect(_DATABASE_URL, uri=True) as connection:

        with closing(connection.cursor()) as cursor:

            query_str = "INSERT INTO wines (wine_id, price, country, title, province) VALUES (:wine_id, :price, :country, :title, :province)"

            query_args = {
                "wine_id": wine.id,
                "price": wine.price,
                "country": wine.country,
                "title": wine.title,
                "province": wine.province,
            }

            cursor.execute(query_str, query_args)

        connection.commit()


def add_to_reviews(review):
    with connect(_DATABASE_URL, uri=True) as connection:

        with closing(connection.cursor()) as cursor:

            query_str = "INSERT INTO reviews (review_id, wine_id, review_content, reviewer_id) VALUES (:review_id, :wine_id, :review_content, :reviewer_id)"

            query_args = {
                "review_id": review.review_id,
                "wine_id": review.wine_id,
                "review_content": review.review_content,
                "reviewer_id": review.reviewer_id,
            }

            cursor.execute(query_str, query_args)

        connection.commit()


with open("winemag-data-130k-v2.csv", newline="") as f:
    reader = csv.reader(f, delimiter=",")
    # order is: id country	description	designation	points	price	province	region_1	region_2	taster_name	taster_twitter_handle   title
    #           0   1       2           3           4       5       6           7           8           9           10                      11
    for line in reader:
        wine = Wine(line[0], line[5], line[1], line[11], line[6])
        add_to_wines(wine)

        review = Review(line[0], line[0], line[2], line[10])
        add_to_reviews(wine)
