#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.org.
"""

import unittest
from unittest.mock import patch
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
        Test that _public_repos_url returns the expected value
        from the mocked .org property.
        """
        payload = {"repos_url": 
                   "https://api.github.com/orgs/google/repos"}
        bad_payload = {message": "Not Found",
                "status": "404"}
        with patch(
            'client.GithubOrgClient.org', 
            new_callable=PropertyMock) 
        as mock_org:
            if org_name == 'google':
                mock_org.return_value = payload
                client = GithubOrgClient("google")
                self.assertEqual(client._public_repos_url, payload["repos_url"])
            else:
                mock_org.return_value = bad_payload
                with self.assertRaises(KeyError):
                    client._public_repos_url
                
    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Unit test GithubOrgClient.public_repos:
        - mock get_json to return a custom payload
        - mock _public_repos_url property
        - assert repos list matches expected
        - check mocks called exactly once
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        expected_repos = ["repo1", "repo2", "repo3"]

        # Mock get_json to return test_payload
        mock_get_json.return_value = test_payload

        with patch("client._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = """
            https://api.github.com/orgs/testorg/repos
            """
            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, expected_repos)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean for given repo/license_key"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
        
if __name__ == "__main__":
    unittest.main()
