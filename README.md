# TimeLens — Historical Timeline Explorer

A working educational Software Engineering prototype with a responsive interface, a SQLite database, a JSON API, an interactive year timeline, before/after image slider, and a record submission form.

## Requirements
Python 3.10+ only. No pip packages or API keys are required.

## Run
1. Extract the ZIP.
2. Open a terminal in the `TimeLens_Project` folder.
3. Run `python server.py` (on some Windows machines: `py server.py`).
4. Open http://localhost:8000 in your browser.
5. Stop with Ctrl+C.

The database `timelens.db` is created automatically on first run.

## Test
Run `python -m unittest discover -s tests -v` from the project folder. The tests use a temporary server and a temporary database; they do not edit your main database.

## Demo sequence
Open Explore → select 1920, 1960 and 2020 → drag the Then & Now slider → add a sample record with a bundled illustration → reload to show it persists.

## Important data disclaimer
Heritage Square is fictional. All bundled scene SVGs are original illustrative artwork, not historical photographs. Dates and descriptions are illustrative. The application does not implement AI restoration, automatic image alignment, verified archives, account authentication, or an upload facility. Those are future-scope features, not completed features.

## API
- `GET /api/health`
- `GET /api/places`
- `GET /api/records?place_id=1`
- `POST /api/records` JSON fields: `place_id`, `year`, `title`, `description`, `source`, `image` (one of the three bundled SVG paths).

## Project layout
`server.py` — HTTP API and SQLite initialization; `index.html` — accessible page structure; `static/style.css` — styling; `static/app.js` — client interactions; `static/assets` — original SVG illustrations; `tests` — automated tests; `docs` — report and diagrams.

## Limitations
Localhost demo only. Public deployment requires authentication, moderation, CSRF protections, hardened server configuration, and an archival licensing workflow. Do not present illustrative content as historical evidence.
