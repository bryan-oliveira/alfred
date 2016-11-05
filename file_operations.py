import os
import json
from config import INGREDIENT_TRANSLATION_FILE


def is_empty_file(fpath):
    return False if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else True


def checkIngredient(ingredient_list):
    """
    Check whether input contains ingredients. Return dictionary of ingredient types, and names, if any.
    Ingredient name is always singular (opposite of plural form).
    :param ingredient_list: string
    :return: False, Error msg | True, Ingredient dictionary
    """
    if not is_empty_file(INGREDIENT_TRANSLATION_FILE):
        with open(INGREDIENT_TRANSLATION_FILE, 'r') as f:
            data = json.load(f)

            ing_dict = {"vegetables": [], "dairy": [], "meat": [], "fruit": []}

            # Ex: vegetable / fruit / dairy
            for ing_type in data:
                # print "Type:", ing_type

                # Ex: strawberry / strawberries
                for ings in data[ing_type]:
                    # print "\tIngs:", ings

                    for word in ingredient_list:
                        # print "\t\tWords:", word, "-", word, " in ", ings, ":", word in ings

                        if word in ings:
                            ing_dict[ing_type].append(ings[0])

            if len(ing_dict) > 0:
                return True, ing_dict

    return False, "Not found"


def parseUSDAIngredients():
    if not is_empty_file("usda_fruits.dat"):
        with open("usda_fruits.dat", "r") as f:
            data = json.load(f)
            print "Total:", data['list']['total']
            for items in data['list']['item']:
                print items['name']


if __name__ == '__main__':
    parseUSDAIngredients()
