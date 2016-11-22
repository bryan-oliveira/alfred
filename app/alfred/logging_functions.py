import config as cfg
import json as jsn
import datetime as dt


def save_recipe_search_log_entry(usr_name, text, ingredients):
    with open(cfg.RECIPE_REQUESTS_LOG, 'a+') as f:
        entry = {'timestamp': str(dt.datetime.utcnow()),
                 'username': usr_name,
                 'full_text': text,
                 'ingredients': ingredients}
        f.write(jsn.dumps(entry))
        f.write('\n')


def output_recipe_search_log_file():
    """Print search terms log file"""
    with open(cfg.RECIPE_REQUESTS_LOG, 'r') as f:
        for line in f:
            out = jsn.loads(line)
            print out


if __name__ == '__main__':
    output_recipe_search_log_file()
