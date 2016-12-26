from config import USDA_FRUIT_DATA, USDA_VEGETABLE_DATA, USDA_SPICES_DATA, \
    VEGETABLE_DB, FRUIT_DB, SPICES_DB
from file_operations import is_empty_file
import json
import sys

"""
This module parses USDA food files. Food ingredients are saved to json format consisting
of only the ingredients themselves.
"""

food_types = {"vegetables": [USDA_VEGETABLE_DATA, VEGETABLE_DB],
              "fruits": [USDA_FRUIT_DATA, FRUIT_DB],
              "spices": [USDA_SPICES_DATA, SPICES_DB]
              }


def create_db_Of_FoodType(food_type):
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

                # Spices file needs slightly different parsing technique
                if food_type == 'spices':

                    # Spices file categorizes some spices as "Spices, <spice name>, <spice attributes>"
                    # others directly as "<spice name>, <spice attributes>"
                    if item['name'].split(',')[0].lower() == 'spices':
                        curr = item['name'].split(',')[1].lower()
                    else:
                        curr = item['name'].split(',')[0].lower()

                # Other USDA files categorize as "<ingredient>, <ingredient attributes>"
                else:
                    curr = item['name'].split(',')[0].lower()

                # Strip whitespaces
                curr = curr.strip()
                print curr

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

            with open(food_types[food_type][1], 'w') as f2:
                json.dump(food_list, f2)
                # [#] print>> sys.stderr, "Wrote %s db to disk." % food_types[food_type][1]
        return True
    return False

if __name__ == '__main__':
    # create_db_Of_FoodType('fruits')
    # create_db_Of_FoodType('vegetables')
    create_db_Of_FoodType('spices')
    pass

