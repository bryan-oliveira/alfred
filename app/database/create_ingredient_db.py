"""
This module parses USDA food files. Food ingredients are then saved to json format.
"""

from config import USDA_FRUIT_DATA, USDA_VEGETABLE_DATA, DATA_FOLDER, VEGETABLE_DB
from file_operations import is_empty_file
import json
import os


def createFruitDB():
    if not is_empty_file(USDA_VEGETABLE_DATA):
        with open(USDA_VEGETABLE_DATA, 'r') as f:
            # Get data from file
            data = json.load(f)

            # Point to fruit items
            items = data['list']['item']
            veggie_list = []
            count = 0

            for item in items:
                curr = item['name'].split(',')[0].lower()
                if curr not in veggie_list:
                    veggie_list.append(curr)
                    count += 1

            print "Total veggies:", data['list']['total'], "Unique", count
            print veggie_list

            with open(VEGETABLE_DB, 'w') as f2:
                json.dump(veggie_list, f2)
                print "Wrote vegetable db to disk."
        return True
    return False

if __name__ == '__main__':
    # createFruitDB()
    pass
