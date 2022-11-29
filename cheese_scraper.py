import requests
from bs4 import BeautifulSoup
from database import add_cheese

URL = "https://www.webstaurantstore.com/guide/869/types-of-cheese.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="guide-section")

cheeses = soup.find_all("div", class_="textimage-left-template")

for cheese in cheeses:
    # print(cheese, end="\n"*2)
    cheese_name = cheese.find("h3")
    cheese_attrs = cheese.find_all("strong")
    # print(cheese_test)
    cheese_rows = [attr.parent for attr in cheese_attrs]

    cheese_milk_type = [s for s in cheese_rows if s and "Type of Milk" in s.text]
    cheese_flavor_notes = [s for s in cheese_rows if s and "Flavor Notes" in s.text]
    cheese_texture = [s for s in cheese_rows if s and "Texture" in s.text]
    cheese_wine = [s for s in cheese_rows if s and "Wine" in s.text]
    cheese_accomp = [s for s in cheese_rows if s and "Accompaniments" in s.text]
    cheese_beer = [s for s in cheese_rows if s and "Beer" in s.text]



    if cheese_name:
        print(cheese_name.text.strip())
        cheese_name = cheese_name.text.strip()
        cheese_milk_type = cheese_milk_type[0].text.split(":")[1].strip() if cheese_milk_type else ""
        cheese_flavor_notes = cheese_flavor_notes[0].text.split(":")[1].strip() if cheese_flavor_notes else ""
        cheese_texture = cheese_texture[0].text.split(":")[1].strip() if cheese_texture else ""
        cheese_wine = cheese_wine[0].text.split(":")[1].strip() if cheese_wine else ""
        cheese_accomp = cheese_accomp[0].text.split(":")[1].strip() if cheese_accomp else ""
        cheese_beer = cheese_beer[0].text.split(":")[1].strip() if cheese_beer else ""

        add_cheese(cheese_name,
                   cheese_milk_type,
                   cheese_flavor_notes,
                   cheese_texture,
                   cheese_wine,
                   cheese_accomp,
                   cheese_beer)
    else:
        # print(cheese)
        sum = 1
    print()