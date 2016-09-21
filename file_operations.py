import os


def is_empty_file(fpath):
    return False if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else True


def removeDuplicateRecipes():
    # TODO: Implement this
    pass


def removeRecipesWithoutPhotos():
    # TODO: Implement this
    pass

