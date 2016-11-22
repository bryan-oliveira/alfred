# from rdflib.plugins.parsers.pyRdfa.rdfs.process import return_graph

from app.speech import speech_module as ss
from app.intent import intent_decipher as idr
from get_recipes_from_file import getRecipesByIngredients, getRecipesByKeywordInName, getRecipesWithAllIngredients
import os
from app import app
from config import DEBUG


def alfred_brain(audio_phrase):
    # Save all recipes to this list
    recipes_with_all_ings = []
    recipes_with_partial_ings = []
    recipe_titles = []

    # [#] print>> sys.stderr, "Step 1"
    # Save audio file to disk
    # print "\taudio file path:", os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg')
    audio_phrase.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg'))

    if DEBUG:
        print "Step 2"

    # Perform voice recognition
    text = ss.speech_recognition_from_file()

    if DEBUG:
        print "Text:", text

    # Extract intent from text
    # command_type, ingredients, meal_course = idr.intent_brain(text)

    # [#] print>> sys.stderr, "Step 3"
    # Searches for ingredients within text

    # Test with custom ingredients DEBUG
    # ingredients = ['pepper', 'beans']

    # ingredient_dict = idr.ingredient_search("hey alfred, I have leftover pepper onion avocado")
    ingredient_dict = idr.ingredient_search(text)

    # Maintain compatibility: All search functions look for ingredients in a list
    ingredients = ingredient_dict['vegetables'] + ingredient_dict['fruits']

    ingredients = idr.add_ingredients_in_singular_plural(ingredients)

    if DEBUG:
        print "Searching for:", ingredients

    # [#] print>> sys.stderr, "Step 3.5"
    getRecipesWithAllIngredients(recipes_with_all_ings, ingredients, recipe_titles)
    # [#] print>> sys.stderr, "Recipes containing all ingredients:", len(recipes_with_all_ings)

    # [#] print>> sys.stderr, "Step 4"
    # Search recipes based on ingredients received from intent
    getRecipesByIngredients(recipes_with_partial_ings, ingredients, recipe_titles)
    # [#] print>> sys.stderr, "Recipes containing some ings:", len(recipes_with_partial_ings)

    # [#] print>> sys.stderr, "Step 5"
    # Search recipes based on ingredients in recipe title
    # recipe_names += getRecipesByKeywordInName(recipe_names, ingredients)
    # print "Len recipes:", len(recipe_names)

    # [#] print>> sys.stderr, "Step 6"
    recipe_list = recipes_with_all_ings + recipes_with_partial_ings

    # [#] print>> sys.stderr, "Step 7"
    # Return recipes

    return recipe_list

if __name__ == '__main__':
    alfred_brain("")
