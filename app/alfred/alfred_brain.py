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
    audio_phrase.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg'))
    print "\taudio file path:", os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg')

    print "Step 2"
    # Perform voice recognition

    text = ss.speech_recognition_from_file()

    # Extract intent from text
    command_type, ingredients, meal_course = idr.intent_brain(text)

    print "Step 3"
    # Searches for ingredients within text

    # Test with custom ingredients DEBUG
    ingredients = ['pepper', 'beans']

    ingredients = idr.ingredient_search(text)

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
    # Get recipes TODO: Main bottleneck is currently here

    # Old: recipe_list = []
    recipe_list = recipe_all_ings + recipe_partial_ings

    # for r in recipe_names:
    #    recipe_list += [getRecipeByName(r)]
    #    print r

    print "Step 7"
    # Return recipes

    return recipe_list

if __name__ == '__main__':

    if "test whether we get recipes based on ingredients provided":
        ingredients = ['tomato', 'soup']
        # Search recipes based on ingredients received from intent
        recipe_names1 = getRecipesByIngredients(ingredients)

        # print recipe_names1

        # Get recipes
        recipes = []
        for recipe in recipe_names1:
            recipes += [getRecipeByName(recipe)]
        # print recipes

