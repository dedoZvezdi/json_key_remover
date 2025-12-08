"""
JSON Key Remover Package.

This package provides tools to clean and filter keys from JSON data.
"""

from .core import (
    read_json_clean,
    write_json,
    collect_all_keys,
    filter_keys,
    JSONType
)
from .gui import main

__all__ = [
    'read_json_clean',
    'write_json',
    'collect_all_keys',
    'filter_keys',
    'JSONType',
    'main'
]

__version__ = '2.1.0'
