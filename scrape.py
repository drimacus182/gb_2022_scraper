import json
from tqdm import tqdm
from api import Api
import multiprocessing as mp
import functools

concurrency = 5

if __name__ == '__main__':
    api = Api()
    project_list = api.get_project_list()

    pool = mp.Pool(concurrency)
    projects_full = tqdm(pool.imap(api.get_project, [p['code'] for p in project_list]), total=len(project_list))

    with open('data.jsonl', 'w') as f:
        f.writelines([json.dumps(p) for p in projects_full])
