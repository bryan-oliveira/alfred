from rdflib.plugins.parsers.pyRdfa.rdfs.process import return_graph

from app.speech import speech_module as ss
from app.intent import intent_decipher as idr
from get_recipes_from_file import getRecipesByIngredients, getRecipeByName, getRecipesByKeywordInName, getRecipesWithAllIngredients
from app import app
import os


def alfred_brain(audio_phrase):
    # Save all recipes to this list
    recipe_all_ings = []
    recipe_partial_ings = []

    print "Step 1"
    # Save audio file to disk
    # print "\taudio file path:", os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg')

    # audio_phrase.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg'))

    print "Step 2"
    # Perform voice recognition

    # text = ss.speech_recognition_from_file()

    # Extract intent from text
    # command_type, ingredients, meal_course = idr.intent_brain(text)

    print "Step 3"
    # Searches for ingredients within text

    # Test with custom ingredients DEBUG
    # ingredients = ['pepper', 'beans']

    # Ex: {"fruits":["apple","strawberry"],"vegetables":["pepper","onion"]}
    # ingredient_dictionary = idr.ingredient_search(text)
    ingredient_dictionary = idr.ingredient_search("hey alfred, I have leftover peppers milk apple onions chicken and avocado")

    # Maintain compatibility: add all ings to list regardless of type
    ingredients = []
    for ing_type in ingredient_dictionary:
        for ing in ingredient_dictionary[ing_type]:
            ingredients.append(ing)
    print "DEBUG:", ingredients

    print "Step 3.5"
    getRecipesWithAllIngredients(recipe_all_ings, ingredients)
    print "Recipes containing all ingredients:", len(recipe_all_ings)

    print "Step 4"
    # Search recipes based on ingredients received from intent
    getRecipesByIngredients(recipe_partial_ings, ingredients)
    print "Recipes containing some ings:", len(recipe_partial_ings)

    print "Step 5"
    # Search recipes based on ingredients in recipe title
    # recipe_names += getRecipesByKeywordInName(recipe_names, ingredients)
    # print "Len recipes:", len(recipe_names)

    print "Step 6"
    recipe_list = recipe_all_ings + recipe_partial_ings

    print "Step 7"
    # Return recipes

    return recipe_list

if __name__ == '__main__':
    alfred_brain("")
