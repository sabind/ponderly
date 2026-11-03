# gallery

A photo gallery for a photographer's clients. After a shoot, the photographer sends the client a link, and the gallery page shows the shoot's photos as a grid of thumbnails. `gallery/thumbs.py` loads the thumbnails from the image store for each page.

## Open decision: requests or httpx

`gallery/thumbs.py` loads thumbnails with `requests` today. Switching it to `httpx` has been proposed, and the decision has not been made.

What we measured for a gallery page of 40 thumbnails:

| Field | `requests` (now) | `httpx` |
| --- | --- | --- |
| How thumbnails load | one after another | all at once |
| Time until a visitor sees the full gallery | about 4 seconds | under 1 second |
| What a visitor sees while it loads | thumbnails filling in row by row | the grid appearing together |
| Cost to the project | none | one new dependency, `thumbs.py` rewritten, its tests rewritten |

Who waits: a photographer's client opening the gallery link after a shoot.
