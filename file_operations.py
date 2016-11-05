import os
import json
from config import VEGETABLE_DB, FRUIT_DB, RECIPE_FILE
import codecs


def is_empty_file(fpath):
    return False if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else True


def overwrite_recipe_file(recipes):
    with codecs.open(RECIPE_FILE, encoding='utf-8', mode='w') as f:
        json.dump(recipes, f, encoding='utf-8')
        return True


def checkIngredient(ingredient_list):
    """
    Check whether input contains ingredients. Return dictionary of ingredient types, and names, if any.
    Ingredient name is always singular (opposite of plural form).
    :param ingredient_list: string
    :return: False, Error msg | True, Ingredient dictionary
    """

    food_types = {"vegetables": VEGETABLE_DB, "fruits": FRUIT_DB}
    ing_dict = {"vegetables": [], "fruits": []}

    for name in food_types:
        if not is_empty_file(food_types[name]):
            with open(food_types[name], 'r') as f:
                data = json.load(f)

                # Check for ingredients
                a = set(ingredient_list)
                b = set(data)
                c = a.intersection(b)

                print a, b, c

                # Add found ingredient to matching food type
                [ing_dict[name].append(ing) for ing in c]

                # Remove identified ingredients from list
                ingredient_list = a.difference(c)

    # Return set elements
    print "Debug:", ing_dict
    return True, ing_dict


if __name__ == '__main__':
    checkIngredient(["onion", "pepper", "avocado", "apple"])
