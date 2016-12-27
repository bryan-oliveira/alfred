import app.database.recipes.recipe_search as rs
import logging_functions as lf
from app.intent import intent_decipher as idr
from config import DEBUG
from app.database.users.db_query import get_user_restriction_tags
from app.speech.speech_module import speech_recognition_from_file
from app import app
from os import path
from timeit import default_timer as timer


def alfred_brain(current_user, audio_phrase=None, keywords=''):

    # Get list of user restrictions
    restrictions = get_user_restriction_tags(current_user.id, 0)

    # Save all recipes to this list
    recipes_with_all_ings = []
    recipes_with_partial_ings = []
    recipes_with_tag = None
    recipe_titles = []

    if DEBUG:
        print "\nUser restrictions: %s\n" % restrictions
        print "Step 1 - Voice Recognition"
        start = timer()

    # Use text keyword search if voice sample is absent
    if audio_phrase is not None:
        # Save audio file to disk and perform speech recognition
        audio_phrase.save(path.join(app.config['UPLOAD_FOLDER'], 'test.ogg'))
        text = speech_recognition_from_file()
    else:
        text = keywords

    if DEBUG:
        print "\tText:", text
        end = timer()
        print '\t', (end - start)

        print "\nStep 2 - Remove ands, ifs and buts"
        start = timer()

    # TODO: Use intent framework to further refine results
    # Extract intent from text
    # command_type, ingredients, meal_course = idr.intent_brain(text)

    # TODO:
    # Remove adjectives, adpositions, adverbs, conjunctions, articles,
    # particles, pronouns and punctuation marks

    text = idr.remove_extraneous_from_search_terms2(text)

    if DEBUG:
        end = timer()
        print '\t', (end - start)

        print "\nStep 3 - Search for ingredients in text"
        start = timer()

    # Searches for individual ingredients in text variable
    ingredient_dict = idr.ingredient_search(text)

    # Since ingredient_search returns a dictionary, convert dictionary into a list
    ingredients = (ingredient_dict['vegetables'] +
                   ingredient_dict['fruits'] +
                   ingredient_dict['meat_poultry'] +
                   ingredient_dict['fish'] +
                   ingredient_dict['seafood'] +
                   ingredient_dict['spices'] +
                   ingredient_dict['additional_ings'])

    # Add both singular and plural version of ingredients
    ingredients = idr.add_ingredients_in_singular_plural(ingredients)

    # Use a word pre-processor to find if user submitted general words (meat, fish, ... )
    ingredients += idr.detect_general_expressions(text)

    # If still no ingredients found, return an empty array for ingredients and one for recipes
    if len(ingredients) == 0:
        return [], []

    if DEBUG:
        print "\t Ingredients found:", ingredients
        end = timer()
        print '\t', (end - start)

        print "\nStep 4 - Searching for recipes with restriction in tag"
        start = timer()

    # If user has restrictions, use them to narrow recipe results
    recipes_with_tag = rs.get_recipes_by_multiple_tags(restrictions)

    if DEBUG:
        print "\tRecipes containing restriction in tag:", len(recipes_with_tag)
        end = timer()
        print '\t', (end - start)

        print "\nStep 5 - Searching for recipes with all ingredients"
        start = timer()

    # If user has restrictions, use list of recipes built instead of the whole
    # recipe base. Recipes are sent as the last parameter of get_recipes_with_all_ingredients
    # If it is None, the function will use the default recipe file, otherwise it uses given list
    rs.get_recipes_with_all_ingredients(recipes_with_all_ings,
                                        ingredients,
                                        recipe_titles,
                                        recipes_with_tag)

    if DEBUG:
        print "\tRecipes containing all ingredients:", len(recipes_with_all_ings)
        end = timer()
        print '\t', (end - start)

        print "\nStep 6 - Searching for recipes with any of the ingredients"
        start = timer()

    # Search recipes that contain any of the ingredients
    rs.getRecipesByIngredients(recipes_with_partial_ings, ingredients, recipe_titles)

    if DEBUG:
        print "\tRecipes containing some ings:", len(recipes_with_partial_ings)
        end = timer()
        print '\t', (end - start)

        print "\nStep 7 - Searching for recipes with ingredients in title"
        start = timer()

    # Search recipes based on ingredients in recipe title
    # recipe_names += getRecipesByKeywordInName(recipe_names, ingredients)
    # print "Len recipes:", len(recipe_names)

    # Join both recipe lists
    recipe_list = recipes_with_all_ings + recipes_with_partial_ings

    # Save a copy of this order in log file
    lf.save_recipe_search_log_entry(current_user, text, ingredients)

    # Put each ingredient found in a list to send to frontend
    ingredient_list = ""
    for it in ingredients:
        ingredient_list += it[0] + ' '

    # Return recipes
    return ingredient_list, recipe_list


if __name__ == '__main__':
    # alfred_brain("")
    pass
