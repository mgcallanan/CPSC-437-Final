import sys
import argparse
from database import get_wine_from_filters, get_cheese_pairings, Pairing

class PairingResult:
    def __init__(self, name, price, country, variety, province, review, cheese_list):
        self.name = name
        self.variety = variety
        self.price = price
        self.country = country
        self.province = province
        self.review = review
        self.cheese_list = cheese_list

# default entries
default = {
    "name": "Louis M. Martini 2012 Cabernet Sauvignon",
    "price": "$35",
    "country": "USA",
    "variety": "Cabernet Sauvignon",
    "province": "Alexander Valley",
    "review": "\"...juicy explosion of rich...\" (V. Boone)"
}

def wine_and_cheese_to_pairingresult(wine, cheese_list):
    return {"name": wine.title, "variety": wine.variety,"price": wine.price, "country":wine.country, "province":wine.province, "review": wine.description, "cheese_list":cheese_list}

# use the database to search given queries
def query_db(filters):
    # first get all wines
    wines = get_wine_from_filters(filters)
    # pick the top 5
    top_pairings = []
    idx = 0
    while len(top_pairings) < 5:
        # get the best cheeses for each variety
        cur_wine = wines[idx]
        pairings = get_cheese_pairings(cur_wine.variety)
        if pairings != None:
            cheese_list = pairings[0].cheese_list
            top_pairings.append(wine_and_cheese_to_pairingresult(cur_wine, cheese_list))
        idx += 1
        continue
    
    # print(top_pairings)
    return top_pairings

# provides wine curation based on user inputs
def curate_wine(args):
    results = []

    # filter out none-value arguments
    args = {k: v for k, v in vars(args).items()}
    if len(args) < 1:   # when no argument is given, we return default entries
        results.append(default)
    
    query = ""
    filters = {}
    for arg in args: # dictionary of arguments
        match arg:
            case "price_max":
                filters["price_max"] = args["price_max"]
            case "price_min":
                filters["price_min"] = args["price_min"]
            case "flavor":
                filters["flavor"] = args['flavor'].split(",")
                # print(filters["flavor"])
            case "country":
                filters["country"] = args['country']
            case "province":
                filters["province"] = args['province']
            case "variety":
                filters["variety"] = args['variety']

    results = query_db(filters)

    return results

# displays CLI result obtained from curate_wine()
def display_result(results):
    p = "\nHere is your curation result:\n"
    for i, result in enumerate(results):
        p += "  {}. {}\n".format(i + 1, result["name"])
        for key, value in result.items():
            p += "    {}: {}\n".format(key.title(), value)
        p += "\n"
    print(p)


if __name__ == "__main__":
    # query options
    cheese_options = ["cheddar", "pecorino", "parmesan", "manchego", "grana padano", "asiago d'allevo"]
    normal_ranges = ["low", "medium", "high"]    # used for attributes such as alcohol, acidity

    # CLI argument parser
    parser = argparse.ArgumentParser(prog='wine_curation',
                                    description='Provides personal curation based on known wine characteristics')
    parser.add_argument('--price_max', action='store', type=int)
    parser.add_argument('--price_min', action='store', type=int)
    # parser.add_argument('--alcohol', action='store', type=str, choices=normal_ranges)
    # parser.add_argument('--acidity', action='store', type=str, choices=normal_ranges)
    parser.add_argument('--flavor', action='store', type=str)
    parser.add_argument('--country', action='store', type=str)
    parser.add_argument('--province', action='store', type=str)
    parser.add_argument('--variety', action='store', type=str)
    # parser.add_argument('--cheese', action='store', type=str)
    args = parser.parse_args()

    # curates wine and displays result
    results = curate_wine(args)
    display_result(results)