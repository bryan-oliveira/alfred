import copy
import json
import sys
from config import VEGETABLE_DB, FRUIT_DB, MEAT_POULTRY_DB, FISH_DB, SEAFOOD_DB, RECIPE_FILE
from file_operations import is_empty_file, overwrite_recipe_file

N_RECIPES = 14


def checkIngredient(ingredient_list):
    """
    Check whether input contains ingredients. Return dictionary of ingredient types, and names, if any.
    Ingredient name is always singular form (opposite of plural).

    :param ingredient_list: string
    :return: False, Error msg | True, Ingredient dictionary
    """

    food_types = {"vegetables": VEGETABLE_DB,
                  "fruits": FRUIT_DB,
                  "meat_poultry": MEAT_POULTRY_DB,
                  "fish": FISH_DB,
                  "seafood": SEAFOOD_DB}

    ing_dict = {"vegetables": [],
                "fruits": [],
                "meat_poultry": [],
                "fish": [],
                "seafood": []}

    for name in food_types:
        if not is_empty_file(food_types[name]):
            with open(food_types[name], 'r') as f:
                data = json.load(f)

                # Check for ingredients
                a = set(ingredient_list)
                b = set(data)
                c = a.intersection(b)

                # print a, b, c

                # Add found ingredient to matching food type
                [ing_dict[name].append(ing) for ing in c]

                # Remove identified ingredients from list
                ingredient_list = a.difference(c)

    # print ing_dict
    return True, ing_dict


if __name__ == '__main__':
    checkIngredient(["orange", "onion", "pepper", "avocado", "apple"])
    checkIngredient(["crab", "chicken", "steak"])


def get_recipes_from_file():

    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)
            return data
    return False


def get_recipe_by_name(recipe_name):

    if not is_empty_file(RECIPE_FILE):
        with open(RECIPE_FILE, 'r') as data_file:
            data = json.load(data_file)
            for recipe in data:
                # print 'Recipe list:',recipe['name'],' ; Recipe search:', recipe_name
                if recipe['title'] == recipe_name:
                    return recipe
            return None


def get_recipes_by_tag(tag, recipes=[]):
    """Return all recipes that contain <tag>"""
    data = get_recipes_from_file()
    recipes = recipes
    for recipe in data:
        for tag_ in recipe['tags']:
            if tag == tag_.lower() and recipe not in recipes:
                recipes += [recipe]

    # print tag, "found", len(recipes)
    return recipes


def get_recipes_with_all_ingredients(recipe_names, ingredients, recipe_titles, restricted_recipes=None):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """

    recipes_with_all_ingredients = recipe_names
    DEBUG = False

    if restricted_recipes is not None:
        data = restricted_recipes
    else:
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

        for title in recipe['ingredientList']:

            # For each ingredient string in recipe Ex: '1/2 onion'
            for recipe_ingredient in recipe['ingredientList'][title]:
                # print recipe_ingredient, ing_copy

                for sub_list in ing_copy:
                    # For each ingredient we are looking for
                    for ing in sub_list:
                        # print "\t", "ing:", ing, "recipe ing:", recipe_ingredient
                        if ing in recipe_ingredient:
                            if DEBUG:
                                string = '\tFound ing: ' + ing + ' in ' + recipe_ingredient + '\n'
                                recipe_output += string
                                # [#] print>> sys.stderr, 'found ->', ing, 'left:', ing_copy, len(ing_copy)

                            ing_copy.remove(sub_list)
                            break

                # TODO: Check whether duplicate recipes are being inserted
                if len(ing_copy) == 0:
                    recipes_with_all_ingredients += [recipe]
                    recipe_titles.append(recipe['title'])
                    next_recipe = True
                    i += 1
                    break

                if next_recipe is True:
                    break

            if next_recipe is True:
                next_recipe = False
                break
        # Break when x recipes found
        if i > 20 and False:
            # print "Ingr: i > 20 - getRecipesByAllIngredient"
            break

    # print recipes_with_all_ingredients
    return recipes_with_all_ingredients


def getRecipesByIngredients(recipe_names, ingredients, recipe_titles):
    """ Input: Ingredients to search in recipes.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """

    data = get_recipes_from_file()
    recipe_count = 0
    next_recipe = False  # When ingredient found, skip to next recipe

    # For each recipe
    for recipe in data:

        # Skip duplicate recipes
        if recipe['title'] in recipe_titles:
            continue

        for title in recipe['ingredientList']:
            # For each ingredient in said recipe
            for recipe_ingredient in recipe['ingredientList'][title]:

                for sublist in ingredients:
                    # For each ingredient we are looking for
                    for ing in sublist:
                        # Keep the recipe names that contain the ingredients
                        if ing in recipe_ingredient:
                            recipe_names += [recipe]
                            recipe_count += 1
                            next_recipe = True
                            break

                if next_recipe is True:
                    break

            if next_recipe is True:
                next_recipe = False
                break

        if recipe_count > 11:
            break


def get_recipes_by_keyword_in_name(recipe_names, keywords):
    """ Input: Keyword to search in recipe name.
        Output: Return N_RECIPES amount of recipes.
        TODO: Change from i to N_RECIPES. """
    # [#] print>> sys.stderr, "getRecipesByKeywordInName"
    # [#] print>> sys.stderr, "Keywords:", keywords

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
                    # [#] print recipe['title'], xs['title'], ":", (recipe['title'] == xs['title'])
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
                    # [#] print>> sys.stderr, "Title: i>10 getRecipesByIngredient"
                    break

    # print recipes_with_ingredients
    return recipes_with_keywords


def remove_recipes_with_missing_fields():
    """
    Iterates over recipe list and removes recipes with missing fields.
    :return: True, Number of recipes removed
    """
    recipes = get_recipes_from_file()
    # title, image, description, chef notes, nutrition, ingredient list
    counter = [0, 0, 0, 0, 0, 0]
    i = 0  # index - used to remove recipe

    for recipe in recipes:

        if recipe['title'] is None:
            counter[0] += 1
            del recipes[i]
        elif recipe["imgURL"] is None:
            counter[1] += 1
        elif recipe["description"] is None:
            counter[2] += 1
        elif recipe["ingredientList"] is None:
            counter[3] += 1
        elif recipe["nutritionInfo"] is None:
            counter[4] += 1
        elif recipe["chefNotes"] is None:
            counter[5] += 1

        i += 1

    print "Recipes missing:\n\tTitle:%d\n\tImage:%d\n\tDescription:%d\n\tChef Notes:%d\n\tNutrition Info:%d\n" \
          "\tIngredients:%d" % (counter[0], counter[1], counter[2], counter[5], counter[4], counter[3])
    print "Total:", len(recipes)

    # Update recipe file
    overwrite_recipe_file(recipes)

    return True


def remove_recipe_by_name(name):
    recipes = get_recipes_from_file()
    name = name.lower()
    index = 0
    for recipe in recipes:

        if name in recipe['title'].lower():

            inp = raw_input("Delete recipe: %s (y/N)?" % recipe['title'])
            if inp == 'y' or inp == 'Y':
                del recipes[index]
                print sys.stderr, "Removed:", recipe['title']

                # Update recipe file
                overwrite_recipe_file(recipes)
                print "Updated recipe db"
                return True
        index += 1
    print "Recipe title not found"
    return False