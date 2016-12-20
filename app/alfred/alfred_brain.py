from os import path as os_path
import app.database.recipes.recipe_search as rs
import logging_functions as lf
from app import app
from app.intent import intent_decipher as idr
from config import DEBUG
from app.database.users.db_query import get_user_restriciton_tags
from app.speech.speech_module import speech_recognition_from_file


def alfred_brain(current_user, audio_phrase):

    # Get list of user restrictions
    restrictions = get_user_restriciton_tags(current_user.id, 0)
    # print "User restrictions:", restrictions

    # Save all recipes to this list
    recipes_with_all_ings = []
    recipes_with_partial_ings = []
    recipes_with_tag = None
    recipe_titles = []

    # Save audio file to disk
    audio_phrase.save(os_path.join(app.config['UPLOAD_FOLDER'], 'test.ogg'))

    if DEBUG:
        print "Step 2 - Voice Recognition"

    # Perform voice recognition
    # text = speech_recognition_from_file()
    text = "mushrooms chicken"

    if DEBUG:
        print "\tText:", text

    # Extract intent from text
    # command_type, ingredients, meal_course = idr.intent_brain(text)

    if DEBUG:
        print "Step 3 - Search for ingredients in text"

    # Searches for ingredients within text
    ingredient_dict = idr.ingredient_search(text)

    # Ingredient_search returns dict; Join all ingredients regardless of type
    ingredients = (ingredient_dict['vegetables'] +
                   ingredient_dict['fruits'] +
                   ingredient_dict['meat_poultry'] +
                   ingredient_dict['fish'] +
                   ingredient_dict['seafood'])

    # Add both singular and plural version of ingredients
    ingredients = idr.add_ingredients_in_singular_plural(ingredients)

    if DEBUG:
        print "\t Ingredients found:", ingredients
        print "Step 5 - Searching for recipes with restriction in tag"

    # If user has restrictions, use them to narrow recipe results
    for tag in restrictions:
        recipes_with_tag = rs.get_recipes_by_tag(tag)
    # print "Recipes containing restriction in tag:", len(recipes_with_all_ings)

    if DEBUG:
        print "Step 4 - Searching for recipes with all ingredients", ingredients

    # If user has restrictions, use list of recipes built instead of the whole
    # recipe base. Recipes are sent as the last parameter of get_recipes_with_all_ingredients
    # If it is None, the function will use the default recipe file, otherwise it uses given list
    rs.get_recipes_with_all_ingredients(recipes_with_all_ings,
                                        ingredients,
                                        recipe_titles,
                                        recipes_with_tag)

    # print "Recipes containing all ingredients:", len(recipes_with_all_ings)

    if DEBUG:
        print "Step 6 - Searching for recipes with any of the ingredients", ingredients

    # Search recipes that contain any of the ingredients
    # rs.getRecipesByIngredients(recipes_with_partial_ings, ingredients, recipe_titles)
    # print "Recipes containing some ings:", len(recipes_with_partial_ings)

    if DEBUG:
        print "Step 7 - Searching for recipes with ingredients in title"

    # Search recipes based on ingredients in recipe title
    # recipe_names += getRecipesByKeywordInName(recipe_names, ingredients)
    # print "Len recipes:", len(recipe_names)

    # Join both recipe lists
    recipe_list = recipes_with_all_ings + recipes_with_partial_ings

    # Save a copy of this order in log file
    lf.save_recipe_search_log_entry(current_user, text, ingredients)

    # Return recipes
    return recipe_list


if __name__ == '__main__':
    alfred_brain("")
