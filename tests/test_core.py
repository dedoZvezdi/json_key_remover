import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from key_remover import core

class TestCore(unittest.TestCase):
    def test_collect_all_keys(self):
        data = {
            "name": "Test",
            "details": {
                "age": 30,
                "hobbies": ["coding", "gaming"]
            },
            "history": [
                {"event": "login", "time": 123},
                {"event": "logout", "time": 124}
            ]
        }
        keys = core.collect_all_keys(data)
        expected = {"name", "details", "age", "hobbies", "history", "event", "time"}
        self.assertEqual(keys, expected)

    def test_filter_keys_remove(self):
        data = {
            "name": "Test",
            "age": 30,
            "nested": {"secret": "value", "public": "ok"}
        }
        keys_to_remove = {"age", "secret"}
        result = core.filter_keys(data, keys_to_remove, mode='remove')
        expected = {
            "name": "Test",
            "nested": {"public": "ok"}
        }
        self.assertEqual(result, expected)

    def test_filter_keys_keep(self):
        data = {
            "name": "Test",
            "age": 30,
            "nested": {"secret": "value", "public": "ok"}
        }
        keys_to_keep = {"name", "nested", "public"}
        result = core.filter_keys(data, keys_to_keep, mode='keep')
        expected = {
            "name": "Test",
            "nested": {"public": "ok"}
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
