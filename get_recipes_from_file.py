from file_operations import is_empty_file
from config import RECIPE_FILE
import json
import copy

# Recipe file defined in application config.py
RECIPE_FILE = RECIPE_FILE
N_RECIPES = 10

DEBUG = False


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
                if recipe['title'] == recipe_name:
                    return recipe
            return None


def getRecipesWithAllIngredients(ingredients):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """

    recipes_with_all_ingredients = []

    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            i = 0
            next_recipe = False
            ing_copy = ingredients

            debug = 3

            # For each recipe
            for recipe in data:

                debug -= 1

                ing_copy = copy.deepcopy(ingredients)
                recipe_output = recipe['title'] + '\n'

                if DEBUG:
                    print recipe['title']

                # For each ingredient string in recipe Ex: '1/2 onion'
                for recipe_ingredient in recipe['ingredientList']:

                    # For each ingredient we are looking for
                    for ing in ing_copy:

                        if ing in recipe_ingredient:
                            if DEBUG:
                                string = '\tFound ing: ' + ing + ' in ' + recipe_ingredient + '\n'
                                recipe_output += string
                                print 'found ->', ing, 'left:', ing_copy, len(ing_copy)

                            ing_copy.remove(ing)
                            break

                    # TODO: Check whether duplicate recipes are being inserted
                    # Old: if ing_counter == n_ings and recipe['name'] not in recipes_with_all_ingredients:
                    if len(ing_copy) == 0:
                        recipes_with_all_ingredients += [recipe]
                        next_recipe = True
                        i += 1

                        if DEBUG:
                            print "FOUND RECIPE - ", recipe_output, '\n'

                        break

                    if next_recipe is True:
                        next_recipe = False
                        break

                if i > 11:
                    print "Ingr: i > 11 - getRecipesByAllIngredient"
                    break

    # print recipes_with_ingredients
    return recipes_with_all_ingredients


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
                for recipe_ingredient in recipe['ingredientList']:
                    # For each ingredient we are looking for
                    for ing1 in ingredients:
                        # Keep the recipe names that contain the ingredients
                        if ing1 in recipe_ingredient:
                            # Don't save duplicates
                            if recipe['title'] not in recipes_with_ingredients:
                                # Old: recipes_with_ingredients += [recipe['name']]
                                recipes_with_ingredients += [recipe]
                                i += 1
                                # print "Ingr: Saving -->", recipe['name']
                                next_recipe = True
                                break

                    if next_recipe is True:
                        next_recipe = False
                        break

                if i > 11:
                    print "Ingr: i>10 getRecipesByIngredient"
                    break

    return recipes_with_ingredients


def getRecipesByKeywordInName(keywords):
    """ Input: Keyword to search in recipe name.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """
    print "Function: getRecipesByKeywordInName"
    print "Keywords:", keywords

    recipes_with_keywords = []
    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            i = 0

            # For each recipe
            for recipe in data:
                # For each keyword in said recipe
                for kw in keywords:
                    # print kw + " - in - " + recipe['name']
                    # For each ingredient we are looking for
                    if kw.lower() in recipe['title'].lower():
                        # Don't save duplicates
                        if recipe['title'] not in recipes_with_keywords:
                            # Old: recipes_with_ingredients += [recipe['name']]
                            recipes_with_keywords += [recipe]
                            i += 1
                            break

                if i > N_RECIPES:
                    print "Title: i>10 getRecipesByIngredient"
                    break

    # print recipes_with_ingredients
    return recipes_with_keywords


if __name__ == '__main__':
    pass

