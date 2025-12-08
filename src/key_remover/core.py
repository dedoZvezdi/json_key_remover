import json
import re
from typing import Any, Dict, List, Set, Union, Optional

JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

def read_json_clean(path: str) -> JSONType:
    """
    Reads a JSON file, cleaning invalid control characters before parsing.

    Args:
        path (str): The path to the JSON file.

    Returns:
        JSONType: The parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    # Remove invalid control characters
    raw = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', raw)
    return json.loads(raw)

def write_json(data: JSONType, path: str) -> None:
    """
    Writes JSON data to a file with indentation.

    Args:
        data (JSONType): The JSON data to write.
        path (str): The destination file path.
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def collect_all_keys(data: JSONType, found_keys: Optional[Set[str]] = None) -> Set[str]:
    """
    Recursively collects all unique keys from a JSON structure.

    Args:
        data (JSONType): The JSON data to traverse.
        found_keys (Optional[Set[str]]): An accumulator set of keys.

    Returns:
        Set[str]: A set of all keys found in the JSON structure.
    """
    if found_keys is None:
        found_keys = set()
    
    if isinstance(data, dict):
        for k, v in data.items():
            found_keys.add(str(k))
            collect_all_keys(v, found_keys)
    elif isinstance(data, list):
        for item in data:
            collect_all_keys(item, found_keys)
            
    return found_keys

def filter_keys(data: JSONType, keys: Set[str], mode: str = 'remove') -> JSONType:
    """
    Recursively filters keys from a JSON structure.

    Args:
        data (JSONType): The JSON data to filter.
        keys (Set[str]): The set of keys to target.
        mode (str): 'remove' to exclude the keys, 'keep' to only include them.

    Returns:
        JSONType: The filtered JSON data.
    """
    if isinstance(data, dict):
        return {
            k: filter_keys(v, keys, mode)
            for k, v in data.items()
            if (k not in keys if mode == 'remove' else k in keys)
        }
    elif isinstance(data, list):
        return [filter_keys(item, keys, mode) for item in data]
    return data
