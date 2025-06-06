#!/usr/bin/env python3
"""Unit tests for access_nested_map utility function."""

import unittest
from typing import Mapping, Sequence, Any
from parameterized import parameterized
from utils import access_nested_map






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
        expected: Any) -> None:
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
            missing_key: str) -> None:
        """Test that access_nested_map raises KeyError for missing keys
        and that the exception message is the missing key."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(missing_key)) 
        #key error exception internally uses repr
