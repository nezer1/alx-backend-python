#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.org.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Test case for GithubOrgClient.
    """
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the correct data
        and calls get_json exactly once with the expected URL.
        """
        expected_payload = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        output = client.org
        self.assertEqual(output, expected_payload)

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @parameterized.expand([
            ("google",),
            ("abc",)
    ])
    def test_public_repos_url(self, org_name: str) -> None:
        """
        Test that _public_repos_url
        returns the expected value
        from the mocked .org property.
        """
        payload = {"repos_url":
                   "https://api.github.com/orgs/google/repos"}
        bad_payload = {message": "Not Found",
                       "status": "404"}
        with patch('client.GithubOrgClient.org',
                     new_callable=PropertyMock) as mock_org:
            if org_name == 'google':
                mock_org.return_value = payload
                client = GithubOrgClient("google")
                self.assertEqual(
                    client._public_repos_url,
                    payload["repos_url"])
            else:
                mock_org.return_value = bad_payload
                with self.assertRaises(KeyError):
                    client._public_repos_url
    
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Tests the test_public_repos."""
        payload = [
            {
                "name": "google-repo-one",
                "license": {
                    "key": "apache-2.0"
                    }
            },
            {
                "name": "google-repo-two",
                "license": {
                    "key": "mit"
                    }
            },
            {
                "name": "google-repo-three",
                "license": None
            },
            {
                "name": "google-repo-four"
            }
        ]
        mock_get_json.return_value = payload
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = """
            https://api.github.com/orgs/google/repos
            """
            client = GithubOrgClient('google')
            public_repo = client.public_repos()
            expected_public_repo = [
                "google-repo-one", "google-repo-two",
                "google-repo-three", "google-repo-four"
                ]
            self.assertEqual(public_repo, expected_public_repo)
            mock_get_json.assert_called_once()
            mock_public_repos_url.assert_called_once()
