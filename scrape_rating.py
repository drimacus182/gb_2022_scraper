import json
import csv
import datetime
from converters import dict_get
from api import Api


# fieldnames = ["code","rating","rating_position","votes_count","is_winner","is_close",
#               "is_passing_by_votes","votesToday","budget","category_color","category_icon",
#               "category_id","category_label","name","user_facebook","user_id","owner",
#               "project_favorite_mark"]

fieldnames = ["rating_position", "code", "votes_count", "is_passing_by_votes", "rating", "name",
              "is_winner", "is_close",
              "votesToday", "budget", "category_label"]


PROJECT_TYPES = dict(big=23, small=24)


def get_filename_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


def write_rating_list(project_type, filename):
    api = Api()
    projects = api.get_project_rating_list(project_type)

    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows([{fn: p[fn] for fn in fieldnames} for p in projects])


if __name__ == '__main__':
    timestamp = get_filename_timestamp()

    write_rating_list('small', f'data/rating_small_{timestamp}.csv')
    write_rating_list('big', f'data/rating_big_{timestamp}.csv')
