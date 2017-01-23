import json
from os import path
from nltk import data
from nltk import word_tokenize
from nltk import pos_tag
from app.database.recipes.recipe_search import checkIngredient
from config import basedir
from config import MEAT_POULTRY_DB, FISH_DB, FRUIT_DB, VEGETABLE_DB

# For production server
path = path.join(basedir, 'nltk_data')
data.path.append(path)


def ingredient_not_in():
    """ Find recipe without a certain ingredient """
    # TODO: Implement
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
    # [#] print>> sys.stderr, pos

    # Ingredient list
    ingredients = []

    # Search for nouns in phrase NN = noun, NNS = Plural noun
    for pair in pos:
        # print pair, pair[0], pair[1]
        if pair[1] == 'NN' or pair[1] == 'NNS':
            ingredients += [pair[0]]

    # [#] print>> sys.stderr, "Ingredients found: ", ingredients
    return ingredients


def ingredient_search(usr_input):
    ing_list = {}

    # Tokenize word
    words = word_tokenize(usr_input)

    # Check for ingredients
    result = checkIngredient(words)

    if result[0] is True:
        ing_list = result[1]

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

    # [#] print>> sys.stderr, "Recipe type(s) found:", found
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

    # [#] print>> sys.stderr, "Question found:", found

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

    # [#] print>> sys.stderr, pos

    if action_type == 'how':
        # Example Q: how can I make scrambled eggs?
        # Example R: why don't you check out some recipes?
        pass

    if action_type == 'what':
        # Example Q: what can I make with eggs and mushrooms?
        # Example R: why don't you check out these recipes?
        pass

    cooking_keywords = ['make', 'cook']


def add_ingredients_in_singular_plural(ingredient_list):
    ingredient_list = [[each] for each in ingredient_list]
    # [#] print>> sys.stderr, "Before:", ingredient_list

    for sub_list in ingredient_list:
        ing = sub_list[0]

        # -ies ending use case; Strawberries/Strawberry
        if ing[-3:] == 'ies' and ing[:-3] + 'y' not in sub_list:
            sub_list.append(ing[:-3] + 'y')

        # -oes ending; potatoes/potato
        elif ing[-3:] == 'oes' and ing[:-2] + 's' not in sub_list:
            sub_list.append(ing[:-2] + 's')

        # -s plural ending; peppers/pepper
        elif ing[-1] == 's' and ing[:-1] not in sub_list:
            sub_list.append(ing[:-1])

        # -y ending; strawberry/strawberries
        elif ing[-1] == 'y' and ing[:-1] + 'ies' not in sub_list:
            sub_list.append(ing[:-1] + 'ies')

        # -singular ending; avocado/avocados
        elif ing + 's' not in sub_list and ing[-1] is not 's':
            sub_list.append(ing + 's')

    # [#] print>> sys.stderr, "After:", ingredient_list
    return ingredient_list


def detect_general_expressions(keywords):
    """ Find general words and exchange them for their ingredient counterparts """
    synonyms = []

    # Search for meat
    if 'meat' in keywords:
        with open(MEAT_POULTRY_DB, 'r') as f:
            data = json.load(f)
            for kw in data:
                synonyms.append([kw])

    # Search for fish
    if 'fish' in keywords:
        with open(FISH_DB, 'r') as f:
            data = json.load(f)
            for kw in data:
                synonyms.append([kw])

    # Search for Fruit
    if 'fruit' in keywords or 'fruits' in keywords:
        with open(FRUIT_DB, 'r') as f:
            data += json.load(f)
            for kw in data:
                synonyms.append([kw])

    # Search for Vegetables
    if 'vegetable' in keywords or 'vegetables' in keywords:
        with open(VEGETABLE_DB, 'r') as f:
            data += json.load(f)
            for kw in data:
                synonyms.append([kw])

    return synonyms


def remove_extraneous_from_search_terms(keywords):
    """ *** Deprecated. Isn't classifying words correctly. ***

    Remove adjectives, adpositions, adverbs, conjunctions, articles,
    particles, pronouns and punctuation marks.
    :return string of words separated by a whitespace
    :rtype string
    """
    # Tokenize input
    tokens = word_tokenize(keywords)

    # Parts of Speech tagger
    kw = pos_tag(tokens)

    print "\t", kw

    final = ''
    for word, pos in kw:
        if pos == 'ADJ' or pos == 'ADP' or pos == 'ADV' or pos == 'CONJ' or pos == 'DET' or \
           pos == 'PRT' or pos == 'PRON' or pos == ',' or pos == 'CC' or pos == 'PRP' or \
           pos == 'DT' or pos == 'IN' or pos == '.':
            continue
        final += word + ' '

    print "\t", final
    return final


def remove_extraneous_from_search_terms2(keywords):
    """ Remove adjectives, adpositions, adverbs, conjunctions, articles,
    particles, pronouns and punctuation marks.
    :return string of words separated by a whitespace
    :rtype string
    """

    # Tokenize input
    tokens = word_tokenize(keywords)

    stopwords = ['i', 'with', 'get', 'me', 'like', 'some']

    final = ''

    for word in tokens:
        if word in stopwords:
            continue
        final += word + ' '

    return final


def find_time_in_search_term(text):
    """Searches the text for word representations of numbers and converts them to integers"""
    tokens = word_tokenize(text)
    numbers = {
        'zero'     : 0,
        'one'      : 1,
        'two'      : 2,
        'three'    : 3,
        'four'     : 4,
        'five'     : 5,
        'six'      : 6,
        'seven'    : 7,
        'eight'    : 8,
        'nine'     : 9,
        'ten'      : 10,
        'eleven'   : 11,
        'twelve'   : 12,
        'thirteen' : 13,
        'fourteen' : 14,
        'fifteen'  : 15,
        'sixteen'  : 16,
        'seventeen': 17,
        'eighteen' : 18,
        'nineteen' : 19,
        'twenty'   : 20,
        'thirty'   : 30,
        'forty'    : 40,
        'fifty'    : 50,
        'sixty'    : 60,
        'seventy'  : 70,
        'eighty'   : 80,
        'ninety'   : 90
    }

    total_time = 0

    for token in tokens:
        if token in numbers:
            # print "#", token
            total_time += int(numbers[token])
    # print "Total time:", total_time
    return total_time

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

    # ingredient_search("with onion pepper and broccoli")

    remove_extraneous_from_search_terms("I would like some meat and peppers please")
    remove_extraneous_from_search_terms("Set a timer please")
    remove_extraneous_from_search_terms("Alfred, time 10 minutes!")
