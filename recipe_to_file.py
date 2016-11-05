import json
import codecs
from file_operations import is_empty_file
from config import RECIPE_FILE

# NEW_RECIPE_FILE = RECIPE_FILE


class Recipe(object):
    def __init__(self, ingredients, directions, name):
        self.ingredients = ingredients
        self.directions = directions
        self.name = name


def save_recipe(new_recipe):
    """ Input: one recipe; Python dict format.
        Output: Saves recipes in JSON format. """

    # Two cases, file is empty or not
    empty_file = is_empty_file(RECIPE_FILE)

    # Case 1: Empty file, we just write to disk
    if empty_file:

        with codecs.open(RECIPE_FILE, encoding='utf-8', mode='w') as f:
            json.dump(new_recipe, f, encoding='utf-8')

        print "Saved %d recipes to file." % len(new_recipe)
    # Case 2: Non empty file. We must append recipe to current structure
    else:

        json_structure = []

        with open(RECIPE_FILE, 'r') as f:
            json_structure = json.load(f)

        # Erase 
        open(RECIPE_FILE, 'w')

        for recipe in new_recipe:
            json_structure.append(recipe)

        with codecs.open(RECIPE_FILE, encoding='utf-8', mode='w') as f:
            json.dump(json_structure, f, encoding='utf-8')

        print "Saved %d recipes to file." % len(json_structure)

    return True


def eliminateIrregularRecipes():

    new_list = []
    with open(RECIPE_FILE, 'r') as data_file:
        data = json.load(data_file)

        for r in data:
            if r is not None:
                new_list += [r]

    with codecs.open(RECIPE_FILE, encoding='utf-8', mode='w') as f:
        json.dump(new_list, f, encoding='utf-8')
