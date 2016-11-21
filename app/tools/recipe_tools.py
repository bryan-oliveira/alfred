"""
    Summary: Collection of tools that operate on recipe data

    Use Case:

"""

import get_recipes_from_file

def how_many_recipes_have_tag(tag):
    """Return how many recipes have tag <tag>"""
    data = get_recipes_from_file
    counter = 0
    for recipe in data:
        if tag in recipe['tag']:
            counter += 1
    return counter


if __name__ == '__main__':
    how_many_recipes_have_tag('')