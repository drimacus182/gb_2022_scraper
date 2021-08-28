import json
import csv
from tqdm import tqdm
from api import Api
import multiprocessing as mp
import datetime
from converters import dict_get

concurrency = 5
fieldnames = ['code','name','link','status','user.name','budget.value','votes.value','currency','category.name',
              'district.name']


def get_filename_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


if __name__ == '__main__':
    api = Api()
    project_list = api.get_project_list()
    project_list_active = [p for p in project_list if p['status'] != 'rejected_final']

    timestamp = get_filename_timestamp()
    with open(f'data/projects_{timestamp}.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows([{fn: dict_get(p, fn) for fn in fieldnames} for p in project_list])

    pool = mp.Pool(concurrency)
    projects_full = list(
        tqdm(
            pool.imap(api.get_project, [p['code'] for p in project_list_active]),
            total=len(project_list_active)
        )
    )

    with open(f'data/{timestamp}.jsonl', 'w') as f:
        f.writelines([json.dumps(p) for p in projects_full])

    votes_full = []
    for p in projects_full:
        for v in p['votes_table']:
            votes_full.append({'code': p['code'], **v})

    with open(f'data/votes_{timestamp}.csv', 'w') as f:
        writer = csv.DictWriter(f, ['code', 'name', 'datetime'])
        writer.writeheader()
        for v in votes_full:
            writer.writerow(v)

