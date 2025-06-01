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
            expected: Any
    ) -> None:
        """Test access_nested_map with various nested structures."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        