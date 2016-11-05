from file_operations import is_empty_file
from config import RECIPE_FILE
import json
import copy

# Recipe file defined in application config.py
RECIPE_FILE = RECIPE_FILE
N_RECIPES = 10


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


def getRecipesWithAllIngredients(recipe_names, ingredients):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """

    recipes_with_all_ingredients = recipe_names

    DEBUG = False
    # print "getRecipesWithAllIngredients\tDEBUG:", DEBUG

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
                # print "###########################\n", recipe['title']
                if recipe['title'] is None or recipe['title'] == "null":
                    continue
                ing_copy = copy.deepcopy(ingredients)
                recipe_output = recipe['title'] + '\n'

                if DEBUG:
                    print recipe['title']

                for title in recipe['ingredientList']:

                    # For each ingredient string in recipe Ex: '1/2 onion'
                    for recipe_ingredient in recipe['ingredientList'][title]:

                        # print recipe_ingredient, ing_copy

                        # For each ingredient we are looking for
                        for ing in ing_copy:
                            # print "\t", "ing:", ing, "recipe ing:", recipe_ingredient
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
                            break

                    if next_recipe is True:
                        next_recipe = False
                        break
                if i > 11:
                    print "Ingr: i > 11 - getRecipesByAllIngredient"
                    break

    # print recipes_with_all_ingredients
    return recipes_with_all_ingredients


def getRecipesByIngredients(recipe_names, ingredients):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """

    recipes_with_ingredients = recipe_names
    DEBUG = False
    # print "getRecipesByIngredients\tDEBUG:", DEBUG

    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            i = 0
            x = 0
            next_recipe = False  # When ingredient found, skip to next recipe
            skip = False  # If recipe already in list, go to next

            # For each recipe
            for recipe in data:
                # Skip if current recipe is already in list
                for xs in recipes_with_ingredients:
                    # print recipe['title'], xs['title'], ":", (recipe['title'] == xs['title'])
                    if recipe['title'] == xs['title']:
                        skip = True

                if skip is True:
                    skip = False
                    continue

                # For each subtype (if available) in ingList
                x += 1
                if DEBUG:
                    print "Title:", recipe['title'], x

                for title in recipe['ingredientList']:
                    # For each ingredient in said recipe
                    if DEBUG:
                        print "Title", title
                    for recipe_ingredient in recipe['ingredientList'][title]:
                        if DEBUG is True:
                            print "Ingredient:", recipe_ingredient
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
                            break

                    if next_recipe is True:
                        next_recipe = False
                        break

                if i > 11:
                    print "Ingr: i>10 getRecipesByIngredient"
                    break

    return recipes_with_ingredients


def getRecipesByKeywordInName(recipe_names, keywords):
    """ Input: Keyword to search in recipe name.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """
    print "getRecipesByKeywordInName"
    print "Keywords:", keywords

    recipes_with_keywords = recipe_names
    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)

            i = 0

            # For each recipe
            for recipe in data:
                skip = False
                # Skip if current recipe is already in list
                for xs in recipes_with_keywords:
                    print recipe['title'], xs['title'], ":", (recipe['title'] == xs['title'])
                    if recipe['title'] == xs['title']:
                        skip = True

                if skip is True:
                    skip = False
                    continue

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

