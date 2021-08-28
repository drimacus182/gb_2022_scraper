import re


def dict_get(data: dict, path: str, default=None):
    path_list = re.split(r'\.', path, flags=re.IGNORECASE)
    result = data
    for key in path_list:
        try:
            key = int(key) if key.isnumeric() else key
            result = result[key]
        except:
            result = default
            break

    return result
