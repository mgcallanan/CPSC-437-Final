import sys
import argparse

# default values
default = {
    "name": "Louis M. Martini 2012 Cabernet Sauvignon",
    "price": "$35",
    "country": "USA",
    "variety": "Cabernet Sauvignon",
    "province": "Alexander Valley",
    "review": "\"...juicy explosion of rich...\" (V. Boone)"
}

# use the database to search given queries
def query_db(query):
    results = []
    return results

# provides wine curation based on user inputs
def curate_wine(args):
    results = []

    # filter out none-value arguments
    args = {k: v for k, v in vars(args).items() if v is not None}
    if len(args) < 1:   # when no argument is given, we return default entries
        results.append(default)
    
    query = ""
    for arg in args: # dictionary of arguments
        match arg:
            case "price_max":
                query += ""
            case "price_min":
                query = ""
    results = query_db(query)

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
    parser.add_argument('--alcohol', action='store', type=str, choices=normal_ranges)
    parser.add_argument('--acidity', action='store', type=str, choices=normal_ranges)
    parser.add_argument('--flavor', action='store', type=str)
    parser.add_argument('--country', action='store', type=str)
    parser.add_argument('--province', action='store', type=str)
    parser.add_argument('--variety', action='store', type=str)
    parser.add_argument('--cheese', action='store', type=str)
    args = parser.parse_args()

    # curates wine and displays result
    results = curate_wine(args)
    display_result(results)