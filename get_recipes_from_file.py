from file_operations import is_empty_file
from config import RECIPE_FILE
import json

# Recipe file defined in application config.py
RECIPE_FILE = RECIPE_FILE


def getRecipesFromFile():

    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            return data


def getRecipeByName(recipe_name):

    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)
            for recipe in data:
                # print 'Recipe list:',recipe['name'],' ; Recipe search:', recipe_name
                if recipe['name'] == recipe_name:
                    return recipe
            return None


def getRecipesByIngredients(ingredients):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """
    recipes_with_ingredients = []
    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            i = 0
            next_recipe = False  # When ingredient found, skip to next recipe

            # For each recipe
            for recipe in data:
                # For each ingredient in said recipe
                for recipe_ingredient in recipe['ingredients']:
                    # For each ingredient we are looking for
                    for ing1 in ingredients:
                        # Keep the recipe names that contain the ingredients
                        if ing1 in recipe_ingredient:
                            # Don't save duplicates
                            if recipe['name'] not in  recipes_with_ingredients:
                                recipes_with_ingredients += [recipe['name']]
                                i += 1
                                print "Ingr: Saving -->", recipe['name']
                                next_recipe = True
                                break

                    if next_recipe is True:
                        next_recipe = False
                        break

                if i > 11:
                    print "Ingr: i>10 getRecipesByIngredient"
                    break

    # print recipes_with_ingredients
    return recipes_with_ingredients


def getRecipesByKeywordInName(keywords):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """
    print "Function: getRecipesByKeywordInName"
    print "Keywords:", keywords

    recipes_with_ingredients = []
    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            i = 0

            # For each recipe
            for recipe in data:
                # For each keyword in said recipe
                for kw in keywords:
                    print kw + " - in - " + recipe['name']
                    # For each ingredient we are looking for
                    if kw.lower() in recipe['name'].lower():
                        # Don't save duplicates
                        if recipe['name'] not in recipes_with_ingredients:
                            recipes_with_ingredients += [recipe['name']]
                            i += 1
                            print "Title Saving -->", recipe['name']
                            break

                if i > 11:
                    print "Title: i>10 getRecipesByIngredient"
                    break

    # print recipes_with_ingredients
    return recipes_with_ingredients


if __name__ == '__main__':
    pass

