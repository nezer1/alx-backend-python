#!/usr/bin/env python3
"""Unit tests for access_nested_map and get_json
utility functions in utils module.
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """Test case class for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        expected: Any
    ) -> None:
        """Test that access_nested_map returns the correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        missing_key: str
    ) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths
        and that the exception message matches the missing key.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(missing_key))


class TestGetJson(unittest.TestCase):
    """Test case class for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict[str, Any]
    ) -> None:
        """
        Test that get_json returns the expected payload by mocking
        requests.get to avoid real HTTP calls.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("utils.requests.get",) as mock_get:
            mock_get.return_value = mock_response
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Test case class for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches result and a_method is only called once."""

        class TestClass:
            """Test class with a memoized property."""

            def a_method(self) -> int:
                """Dummy method that returns 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Memoized version of a_method."""
                return self.a_method()

        test_obj = TestClass()

        with patch.object(test_obj,
            'a_method',
            wraps=test_obj.a_method
            ) as mock:
            first_result = test_obj.a_property
            second_result = test_obj.a_property

            self.assertEqual(first_result, 42)
            self.assertEqual(second_result, 42)
            mock.assert_called_once()
