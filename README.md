# Expense Manager

A small, self-contained personal expense tracker built with **Flask** and
**SQLite**. Add expenses through a plain HTML form, browse them in a table,
and see totals broken down by category and by month.

## Features

- Add an expense with a date, category, amount, and optional note.
- View all expenses in a sortable-by-date table.
- Summary page showing:
  - Grand total spent.
  - Totals grouped by category.
  - Totals grouped by month (`YYYY-MM`).
- Server-rendered HTML with Jinja2 templates and plain CSS — no JS framework.
- Flask application factory (`create_app`) so tests can spin up an isolated,
  in-memory database.

## Project layout

```
expense-manager/
├── app.py                  # `python app.py` entry point
├── wsgi.py                 # `flask run` entry point
├── expense_app/
│   ├── __init__.py         # create_app() application factory
│   ├── db.py                # SQLite connection helpers + schema
│   ├── routes.py            # add / list / summary routes
│   ├── templates/           # Jinja2 templates
│   └── static/style.css     # plain CSS
├── tests/
│   └── test_app.py          # Flask test-client unit tests
└── .github/workflows/tests.yml
```

## Running locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 1
python app.py

# Option 2
export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
flask run
```

Then open http://127.0.0.1:5000 in your browser. The app creates a SQLite
database at `instance/expenses.sqlite` on first run.

## Example usage

1. Go to **Add Expense**, fill in:
   - Date: `2026-09-01`
   - Category: `Groceries`
   - Amount: `54.20`
   - Note: `Weekly shopping`
2. Click **Save Expense** — you're redirected to **Expenses**, where the new
   row appears at the top of the table.
3. Add a couple more expenses in different categories/months, then visit
   **Summary** to see:
   - `Grand total: $XXX.XX`
   - A table of totals per category (e.g. `Groceries — $54.20`)
   - A table of totals per month (e.g. `2026-09 — $54.20`)

## Running the tests

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Tests use `create_app(testing=True)`, which points the app at an in-memory
SQLite database, so no files are created and no dev server is started.

## Continuous Integration

`.github/workflows/tests.yml` runs the full test suite on every push and pull
request using GitHub Actions (`actions/checkout@v4`, `actions/setup-python@v5`,
Python 3.11).

## License

MIT — see [LICENSE](LICENSE).
