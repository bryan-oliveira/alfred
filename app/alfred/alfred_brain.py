from app.speech import speech_module as ss
from app.intent import intent_decipher as idr
from get_recipes_from_file import getRecipesByIngredients, getRecipeByName, getRecipesByKeywordInName
from app import app
import os


def alfred_brain(audio_phrase):

    # Save audio file to disk
    audio_phrase.save(os.path.join(app.config['UPLOAD_FOLDER'], 'test.ogg'))

    # Perform voice recognition
    text = ss.speech_recognition_from_file()

    # Extract intent from text
    # command_type, ingredients, meal_course = idr.intent_brain(text)

    # Searches for ingredients within text
    ingredients = idr.ingredient_search(text)

    # Test with custom ingredients DEBUG
    # ings = ['tomato', 'soup']

    # Search recipes based on ingredients received from intent
    recipe_names = getRecipesByIngredients(ingredients)

    # Search recipes based on ingredients in recipe title
    recipe_names += getRecipesByKeywordInName(ingredients)

    # Get recipes
    recipe_list = []
    for r in recipe_names:
        recipe_list += [getRecipeByName(r)]
        # print r

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

