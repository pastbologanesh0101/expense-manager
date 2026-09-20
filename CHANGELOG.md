# Changelog

All notable changes to this project are documented in this file.

## [0.1.0] - 2025-09-17

Initial release.

### Added

- Flask application factory (`create_app()`) with SQLite storage via the
  standard library `sqlite3` module.
- `expense` table (date, category, amount, note) created automatically on
  startup, plus a `flask init-db` CLI command.
- Routes for adding an expense (with server-side validation of date,
  category, and amount), listing all expenses, and a summary page.
- Summary page with grand total, totals grouped by category, and totals
  grouped by month (`YYYY-MM`).
- Two entry points: `app.py` (`python app.py`) and `wsgi.py`
  (`flask run` / production WSGI servers).
- In-memory SQLite database support for tests via `create_app(testing=True)`.
- Server-rendered Jinja2 templates and plain CSS (no frontend framework).
- Unit test suite (`tests/test_app.py`) covering happy-path and validation
  error cases using Flask's test client.
- GitHub Actions CI running the test suite on Python 3.11 and 3.12.
- MIT license.
