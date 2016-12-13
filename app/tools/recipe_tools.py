"""
    Summary: Collection of tools that operate on recipe data

    Use Case:

"""
import app.database.recipes.recipe_search as rs


def how_many_recipes_have_tag(tag):
    """Return how many recipes have tag <tag>"""
    data = rs.get_recipes_from_file()
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
    data = rs.get_recipes_from_file()
    keys = data[0].keys()

    for key in keys:
        print key
    return True


def list_every_unique_recipe_tag():
    """Return all recipe tag """
    data = rs.get_recipes_from_file()
    tag_list = []
    for recipe in data:
        for tag in recipe['tags']:
            if tag.lower() not in tag_list:
                tag_list.append(tag.lower())
    tag_list.sort()
    print len(tag_list), tag_list
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
    list_every_unique_recipe_tag()

    pass

