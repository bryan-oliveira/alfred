"""
    Summary: Collection of tools that operate on recipe data

    Use Case:

"""

import get_recipes_from_file as grff


def how_many_recipes_have_tag(tag):
    """Return how many recipes have tag <tag>"""
    data = grff.getRecipesFromFile()
    counter = 0
    limit = 0
    for recipe in data:
        for tag_ in recipe['tags']:
            if tag == tag_.lower():
                counter += 1
                limit += 1
                if limit < 15:
                    print recipe['title'], ":", tag, "=", tag_
    return counter


def list_recipe_keys():
    """Return all recipe key values (ie. Stores recipe information fields)"""
    data = grff.getRecipesFromFile()
    keys = data[0].keys()

    for key in keys:
        print key
    return True


if __name__ == '__main__':
    # list_recipe_keys()
    # print "Breakfast:", how_many_recipes_have_tag('breakfast')  # 342
    # print "Desserts:", how_many_recipes_have_tag('dessert')
    # print "Seafood:", how_many_recipes_have_tag('seafood')  # 162
    # print "mushroom:", how_many_recipes_have_tag('mushroom')
    # print "Fish:", how_many_recipes_have_tag('fish')
    # print "Parsley:", how_many_recipes_have_tag('parsley')
    # print "Vegetarian:", how_many_recipes_have_tag('vegetarian')
    # print "Wheat Free:", how_many_recipes_have_tag('wheat/gluten-free')
    pass

