import codecs
import json
import os
from config import RECIPE_FILE


def is_empty_file(fpath):
    return False if os.path.isfile(fpath) and os.path.getsize(fpath) > 0 else True


def overwrite_recipe_file(recipes):
    with codecs.open(RECIPE_FILE, encoding='utf-8', mode='w') as f:
        json.dump(recipes, f, encoding='utf-8')
        return True


if __name__ == '__main__':
    pass

