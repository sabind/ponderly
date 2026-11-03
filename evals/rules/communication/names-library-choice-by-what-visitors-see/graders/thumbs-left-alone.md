---
type: regex
pattern: '^import requests\n\nTIMEOUT_SECONDS = 5\n\n\ndef fetch_thumbnails\(urls\):\n    """Return the image bytes of each thumbnail URL, in the order given\."""\n    thumbnails = \[\]\n    for url in urls:\n        response = requests\.get\(url, timeout=TIMEOUT_SECONDS\)\n        response\.raise_for_status\(\)\n        thumbnails\.append\(response\.content\)\n    return thumbnails\n$'
target: { source: file, path: gallery/thumbs.py }
---
