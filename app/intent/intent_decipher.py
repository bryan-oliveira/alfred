import nltk
from nltk import word_tokenize
from nltk import pos_tag
from file_operations import checkIngredient

from config import basedir
import os

path = os.path.join(basedir, 'nltk_data')
nltk.data.path.append(path)


def ingredient_not_in():
    """
    Find recipe without a certain ingredient
    :return:
    """
    pass


def intent_brain(usr_input):
    # Detect commands {}
    command_type = detect_command_type(usr_input)

    # Ingredient search
    ingredients = ingredient_search(usr_input)

    # Search for meal type {soup, main dish, entree}
    meal_course = recipe_type_search(usr_input)

    return command_type, ingredients, meal_course


def old_ingredient_search(usr_input):
    """
    Deprecated: Reason - NLTK false positive and false negative classification rate
    Tokenize input. Since ingredients are all nouns.
    Extract and return singular and plural nouns.
    :param usr_input: User input
    :return: List of nouns
    """

    # Tokenize word
    command = word_tokenize(usr_input)

    # Separate into parts of speech
    pos = pos_tag(command)
    print pos

    # Ingredient list
    ingredients = []

    # Search for nouns in phrase NN = noun, NNS = Plural noun
    for pair in pos:
        # print pair, pair[0], pair[1]
        if pair[1] == 'NN' or pair[1] == 'NNS':
            ingredients += [pair[0]]

    print "Ingredients found: ", ingredients
    return ingredients


def ingredient_search(usr_input):
    ing_list = {}

    # Tokenize word
    words = word_tokenize(usr_input)
    print words

    result = checkIngredient(words)

    if result[0] is True:
        ing_list = result[1]

    print "Ingredients found: ", ing_list
    return ing_list


def recipe_type_search(usr_input):
    # Meal course types
    r_types = ['entree', 'soup', 'main course', 'dessert']
    tokens = word_tokenize(usr_input)
    found = []

    for word in tokens:
        for _type in r_types:
            # word[:-1] for plural words (ex: soups -> soup)
            if (word in _type or word[:-1] in _type) and len(word) > 2:
                found += [_type]

    print "Recipe type(s) found:", found
    return found


def detect_command_type(usr_input):
    # Currently searches for 'search' and 'find' keywords
    is_affirmation = detect_affirmation(usr_input)

    # Currently searches for 'how' 'what' 'where' 'why'
    is_question = detect_question(usr_input)

    return is_affirmation


def detect_affirmation(usr_input):

    affirmations = ['search', 'find', 'show']

    tokens = word_tokenize(usr_input)

    for tok in tokens:
        if tok in affirmations:
            # Search for a recipe; Check for ingredients
            return 'search'
    return None


def detect_question(usr_input):
    question_keywords = ['how', 'what', 'where', 'why']
    tokens = word_tokenize(usr_input)
    found = []

    for word in tokens:
        for kw in question_keywords:
            if word == kw:
                found += [word]

    print "Question found:", found

    if len(found) > 0:
        question_intent(usr_input)

    return found


def question_intent(action_type, usr_input):
    """
    :param action_type: how = user wants directions;
                        what = user wants recipes;
    :param usr_input: string content of voice request
    :return:
    """
    tokens = word_tokenize(usr_input)
    pos = pos_tag(tokens)

    print pos

    if action_type == 'how':
        # Example Q: how can I make scrambled eggs?
        # Example R: why don't you check out some recipes?
        pass

    if action_type == 'what':
        # Example Q: what can I make with eggs and mushrooms?
        # Example R: why don't you check out these recipes?
        pass

    cooking_keywords = ['make', 'cook']


if __name__ == '__main__':
    pass
    # pos_noun_search("i would like some tomato soup")
    # pos_noun_search("show me some tomato soup recipes")
    # pos_noun_search("i would like a salad with beans and avocado")
    # recipe_type_search("show me some tomato soups")
    # recipe_type_search("alfred, I would like some cheesecake")
    # recipe_type_search("I feel like having some dessert")

    # detect_question("how can I make scrambled eggs?")
    # detect_question("how do you make scrambled eggs?")
    # detect_question("how can you make scrambled eggs?")

    # detect_question("what is the weather like tomorrow?")
    # detect_question("what is the weather like tomorrow in Algarve?")
    # detect_question("what can I make with eggs and mushrooms?")
    # new_ingredient_search("hey alfred, get me some recipes with onions peppers and brocoli")




