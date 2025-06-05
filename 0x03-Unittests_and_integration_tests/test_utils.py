#!/usr/bin/env python3
"""Unit tests for access_nested_map utility function."""

import unittest
from typing import Mapping, Sequence, Any
from parameterized import parameterized
from utils import access_nested_map, get_json,memoize
from unittest.mock import patch, Mock
from client import GithubOrgClient




class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
            self,
            nested_map: Mapping,
            path: Sequence[str],
            expected: Any
    ) -> None:
        """Test access_nested_map with various nested structures."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence[str],
            missing_key: str
    ) -> None:
        """Test that access_nested_map raises KeyError for missing keys
        and that the exception message is the missing key."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(missing_key)) 
        #key error exception internally uses repr



class TestGetJson(unittest.TestCase):

    """Test case for the get_json function."""
    @parameterized.expand([
        ("valid_example_url", "http://example.com", {"payload": True}),
        ("valid_holberton_url", "http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self, 
        name: str, 
        test_url: str, 
        test_payload: dict
        ) -> None:
        """Test get_json returns expected payload from mocked request."""
       
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch("utils.requests.get") as mocked_get:
            mocked_get.return_value = mock_response
            
            result = get_json(test_url)
            mocked_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)
            



# class TestMemoize(unittest.TestCase):
#     """
#     Test case for memoize decorator.
#     """

#     def test_memoize(self) -> None:
#         """
#         Test that memoize caches the result of a method.
#         """

#         class TestClass:
#             """A sample class for testing memoization."""

#             def a_method(self) -> int:
#                 """A method to return 42."""
#                 return 42

#             @memoize
#             def a_property(self) -> int:
#                 """A memoized property that calls a_method."""
#                 return self.a_method()

#         with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
#             obj = TestClass()
#             result1 = obj.a_property
#             result2 = obj.a_property

#             self.assertEqual(result1, 42)
#             self.assertEqual(result2, 42)
#             mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
