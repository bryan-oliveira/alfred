import config as cfg
import json as jsn
import datetime as dt


def save_recipe_search_log_entry(user, text, ingredients):
    with open(cfg.RECIPE_REQUESTS_LOG, 'a+') as f:
        timestamp = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        entry = {'timestamp': timestamp,
                 'username': user.username,
                 'id': user.id,
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
