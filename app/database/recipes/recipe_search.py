import copy
import json
import sys
from file_operations import is_empty_file, overwrite_recipe_file
from config import VEGETABLE_DB, FRUIT_DB, MEAT_POULTRY_DB, \
    FISH_DB, SEAFOOD_DB, RECIPE_FILE, ADDITIONAL_INGS_DB, SPICES_DB, TAG_DB
from timeit import default_timer as timer
from nltk import word_tokenize

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
                  "seafood": SEAFOOD_DB,
                  "spices": SPICES_DB,
                  "additional_ings": ADDITIONAL_INGS_DB}

    ing_dict = {"vegetables": [],
                "fruits": [],
                "meat_poultry": [],
                "fish": [],
                "seafood": [],
                "spices": [],
                "additional_ings": []}

    for name in food_types:
        if not is_empty_file(food_types[name]):
            with open(food_types[name], 'r') as f:
                data = json.load(f)

                # Check for ingredients using set intersection. Quicker than pythonic
                # keyword 'in' list method
                a = set(ingredient_list)
                b = set(data)
                c = a.intersection(b)

                # print a
                # print b
                # print c

                # Add found ingredient to matching food type
                [ing_dict[name].append(ing) for ing in c]

                # Remove identified ingredients from list
                ingredient_list = a.difference(c)

    # print ing_dict
    return True, ing_dict


def checkTagInText(tag_list):
    tags = []
    tag_list = tag_list.split()

    with open(TAG_DB, 'r') as f:
        data = json.load(f)
        for tag in tag_list:
            for tag_ in data:
                if tag.lower() == tag_.lower():
                    tags.append(tag)

    print "tag_list:", tag_list
    search_nonalcoholic = False
    for tag in tag_list:
        if tag.lower() == 'soup':
            tags.append('soup/stew')
        if tag.lower() == 'non':
            search_nonalcoholic = True
        if tag.lower() == 'alcoholic' and search_nonalcoholic:
            tags.append('non-alcoholic')

    return tags


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
                if recipe['title'].strip() == recipe_name.strip():
                    return recipe
            return None


def get_recipes_by_multiple_tags(tag_list):
    """ Return all recipes that contain tags contained in tag_list """
    data = get_recipes_from_file()
    recipes = []

    # List comprehension of lowercase tag set
    tag_list_set = set(t.lower() for t in tag_list)

    for recipe in data:
        recipe_tag_set = set(rt.lower() for rt in recipe['tags'])

        if len(tag_list_set.intersection(recipe_tag_set)) > 0:
            recipes += [recipe]

    return recipes


def get_recipes_by_tag(tag):
    """ Return all recipes that contain <tag> """
    data = get_recipes_from_file()
    recipes = []
    tag = tag.lower()
    for recipe in data:
        for tag_ in recipe['tags']:
            if tag == tag_.lower():
                recipes += [recipe]

    # print tag, "found", len(recipes)
    return recipes


def get_recipes_with_all_ingredients(recipe_names,
                                     ingredients,
                                     recipe_titles,
                                     recipes_with_partial_ings,
                                     restricted_recipes=None):
    """
    :param recipes_with_partial_ings:
    :param restricted_recipes: if present, use only recipes from this list
    :param recipe_names empty list, populate with recipes found
    :param ingredients ingredients to search for
    :param recipe_titles: save titles of recipes
    """

    data = []
    recipes_with_all_ingredients = recipe_names
    DEBUG = True

    # print "Len:", len(restricted_recipes)

    if len(restricted_recipes) > 0:
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

                            # Add recipe to partial ingredients list
                            recipes_with_partial_ings += [recipe]
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

                if i > 23:
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
    # overwrite_recipe_file(recipes)

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


def print_all_unique_tags():
    """ Prints every unique tag available """
    data = get_recipes_from_file()
    tags = []
    for recipe in data:
        for tag_ in recipe['tags']:
            if tag_ not in tags:
                tags.append(tag_)
    tags.sort()
    for t in tags:
        print t

    return True


def check_recipes_with_no_ings():
    data = get_recipes_from_file()
    counter = 0
    limit = 0
    for recipe in data:
        limit += 1
        # print recipe['ingredientList']
        if len(recipe['ingredientList']) == 0:
            counter += 1

    print counter


if __name__ == '__main__':
    # checkIngredient(["orange", "onion", "pepper", "avocado", "apple"])
    # checkIngredient(["crab", "chicken", "steak"])
    # remove_recipes_with_missing_fields()
    #print_all_unique_tags()
    # get_recipes_by_tag('cheesecake')
    get_recipes_by_keyword_in_name([], ['cheesecake'])
    # checkTagInText(['lunch'])
    pass

