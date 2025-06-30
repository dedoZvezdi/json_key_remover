import json
import re

def read_json_clean(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    raw = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', raw)
    return json.loads(raw)

def write_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def collect_all_keys(data, found_keys=None):
    if found_keys is None:
        found_keys = set()
    if isinstance(data, dict):
        for k, v in data.items():
            found_keys.add(k)
            collect_all_keys(v, found_keys)
    elif isinstance(data, list):
        for item in data:
            collect_all_keys(item, found_keys)
    return found_keys

def filter_keys(data, keys, mode='remove'):
    if isinstance(data, dict):
        return {
            k: filter_keys(v, keys, mode)
            for k, v in data.items()
            if (k not in keys if mode == 'remove' else k in keys)
        }
    elif isinstance(data, list):
        return [filter_keys(item, keys, mode) for item in data]
    return data
