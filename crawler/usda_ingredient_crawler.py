"""
This module scrapes the USDA Database for ingredients
"""
from urllib import urlencode
from file_operations import is_empty_file
import requests
import json

url = "http://api.nal.usda.gov/ndb/search/?"
q = {}
q.update({"ds": "Standard Reference"})  # Data source - "branded+food+products" or "standard+reference"
q.update({"sort": "n"})                 # Sort by food name (n) or search relevance (r)
q.update({"max": "1500"})                 # Max rows to return
q.update({"offset": "0"})               # Offset
q.update({"format": "json"})            # JSON or XML
q.update({"api_key": "OuoCMUMjuXyOYKPVenaaGhEsKWDnIq4T93C9jz2h"})   # API Key

food_data = {"fruits": {"fg": "fruits and fruit juices", "file_name": "usda_fruits.dat", "q": "raw"},
             "veggies": {"fg": "vegetables and vegetable products", "file_name": "usda_veggies.dat", "q":"raw"},
             "spices": {"fg": "spices and herbs", "file_name": "usda_spices.dat", "q": ""},
             "dairy": {"fg": "dairy and egg products", "file_name": "usda_dairy.dat", "q": ""},
             "legumes": {"fg": "legumes and legume products", "file_name": "usda_legumes.dat", "q": "raw"}
             }


def createUSDAFile(food_type):

    if is_empty_file(food_data[food_type]["file_name"]):
        q.update({"fg": food_data[food_type]["fg"]})
        q.update({"q": food_data[food_type]["q"]})

        # Create url req
        qtr = urlencode(q)
        print url + qtr

        r = requests.get(url + qtr)
        print "Status Code:", r
        # print "JSON Data:", r.json()

        with open(food_data[food_type]["file_name"], "w") as f:
            json.dump(r.json(), f)

        return True
    return False

if __name__ == "__main__":
    createUSDAFile("fruits")
    createUSDAFile("veggies")
    createUSDAFile("spices")
    createUSDAFile("dairy")
    createUSDAFile("legumes")
