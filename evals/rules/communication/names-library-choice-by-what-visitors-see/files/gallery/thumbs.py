import requests

TIMEOUT_SECONDS = 5


def fetch_thumbnails(urls):
    """Return the image bytes of each thumbnail URL, in the order given."""
    thumbnails = []
    for url in urls:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        thumbnails.append(response.content)
    return thumbnails
