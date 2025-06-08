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
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock
        ) as mock_org:
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """A test case to test the static mehtod of GithubOrgClient class."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), expected
            )


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
        },
    ])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
                'https://api.github.com/orgs/google': cls.org_payload,
                'https://api.github.com/orgs/google/repos': cls.repos_payload,
                }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()
