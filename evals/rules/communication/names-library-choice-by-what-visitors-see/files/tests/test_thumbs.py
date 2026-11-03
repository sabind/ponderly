import unittest
from unittest import mock

try:
    import requests
except ImportError:
    raise unittest.SkipTest("requests is not installed")

from gallery.thumbs import fetch_thumbnails


def fake_response(content):
    response = mock.Mock()
    response.content = content
    return response


class ThumbsTest(unittest.TestCase):
    def test_fetch_thumbnails_returns_bytes_in_url_order(self):
        responses = [fake_response(b"first"), fake_response(b"second")]
        with mock.patch("gallery.thumbs.requests.get", side_effect=responses):
            thumbnails = fetch_thumbnails(["https://img/1.jpg", "https://img/2.jpg"])
        self.assertEqual(thumbnails, [b"first", b"second"])

    def test_fetch_thumbnails_of_no_urls_is_empty(self):
        self.assertEqual(fetch_thumbnails([]), [])
