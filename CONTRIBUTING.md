# Contributing to Expense Manager

This is a small Flask + SQLite expense tracker. Contributions are welcome —
please keep changes focused and tested.

## Getting set up

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

```bash
python -m unittest discover -s tests -v
```

Tests run against `create_app(testing=True)`, which uses an in-memory
SQLite database — no files are created and the schema is applied fresh for
every test class. Any new route or validation rule should come with a test
in `tests/test_app.py`.

## Code style

- Match the existing structure: `expense_app/db.py` owns the schema and
  connection handling, `expense_app/routes.py` owns the view functions.
- Validation helpers (`_parse_amount`, `_parse_date`) return
  `(value, error_message)` tuples — follow that pattern for new fields
  rather than raising exceptions from form parsing.
- Use `flash()` for user-facing messages, and make error messages specific
  enough that a user knows exactly what to fix.
- Keep `requirements.txt` minimal; avoid adding a dependency unless it
  clearly earns its place.

## Submitting changes

1. Open an issue or PR describing the change and its motivation.
2. Run the full test suite locally before pushing — it must pass.
3. Keep commits small and focused, with a message that explains what
   changed and why.
