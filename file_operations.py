import os
import json
from config import VEGETABLE_DB


def is_empty_file(fpath):
    return False if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else True


def checkIngredient(ingredient_list):
    """
    Check whether input contains ingredients. Return dictionary of ingredient types, and names, if any.
    Ingredient name is always singular (opposite of plural form).
    :param ingredient_list: string
    :return: False, Error msg | True, Ingredient dictionary
    """

    # TODO: Iterate over all relevant files
    # check = [ VEGETABLE_DB ]
    ing_dict = {"vegetables": [], "fruit": []}

    if not is_empty_file(VEGETABLE_DB):
        with open(VEGETABLE_DB, 'r') as f:
            data = json.load(f)

            """
            for item in data:
                print "item:", item, " --- ", ingredient_list
                for ing in ingredient_list:
                    if ing in item:
                        print "### --- ", ing, "-", item
                        ing_dict['vegetables'] = ing
            """
            a = set(ingredient_list)
            b = set(data)
            c = a.intersection(b)

            # if len(ing_dict['vegetables']) > 0 or len(ing_dict['fruit']) > 0:
            #    return True, ing_dict
            return True, c

    return False, "Not found"


if __name__ == '__main__':
    pass
