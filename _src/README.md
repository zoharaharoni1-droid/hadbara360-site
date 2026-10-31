# Site source (הדברה 360)

- `gen/content.py`, `gen/deep_*.py` – page content.
- `gen/reviews.json` – Google reviews shown on the site (5-star only are displayed). To add new reviews: add entries (newest first), update `count`/`updated`, then run `bash _src/publish.sh`, commit and push.
- `site/assets/` – CSS, JS, images.
