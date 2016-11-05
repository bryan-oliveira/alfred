"""
This module parses USDA food files. Food ingredients are then saved to json format.
"""

from config import USDA_FRUIT_DATA, USDA_VEGETABLE_DATA, VEGETABLE_DB, FRUIT_DB
from file_operations import is_empty_file
import json

food_types = {"vegetables": [USDA_VEGETABLE_DATA, VEGETABLE_DB],
              "fruits": [USDA_FRUIT_DATA, FRUIT_DB]
              }


def create_DB_Of_FoodType(food_type):
    if food_type not in food_types:
        return False, "Food type not found."

    if not is_empty_file(food_types[food_type][0]):
        with open(food_types[food_type][0], 'r') as f:
            # Get data from file
            data = json.load(f)

            # Point to fruit items
            items = data['list']['item']
            food_list = []
            count = 0

            for item in items:
                curr = item['name'].split(',')[0].lower()

                # Discard repeat vegetable names
                if curr not in food_list:
                    food_list.append(curr)
                    count += 1

                # Strawberries -> Strawberry
                if curr[-3:] == 'ies' and (curr[:-3] + 'y') not in food_list:
                    food_list.append(curr[:-3] + 'y')
                # Bananas - > Banana
                elif curr[-1] == 's' and curr[:-1] not in food_list:
                    food_list.append(curr[:-1])

            print "Total ingredients:", data['list']['total'], "Unique", count
            print food_list

            with open(food_types[food_type][1], 'w') as f2:
                json.dump(food_list, f2)
                print "Wrote %s db to disk." % food_types[food_type][1]
        return True
    return False

if __name__ == '__main__':
    # create_DB_Of_FoodType("fruits")
    # create_DB_Of_FoodType("vegetables")
    pass

