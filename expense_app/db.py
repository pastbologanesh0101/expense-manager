import sqlite3

import click
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    note TEXT
);
"""


def _connect(app):
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=False,
    )
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Return a request-scoped SQLite connection.

    For the default file-backed database a fresh connection is opened per
    request and cleaned up in ``close_db``. For the in-memory database used
    in tests, a single connection is kept alive on the app object for the
    app's lifetime, since a new ``:memory:`` connection would otherwise be a
    blank, schema-less database.
    """
    if current_app.config["DATABASE"] == ":memory:":
        if not hasattr(current_app, "_memory_db"):
            current_app._memory_db = _connect(current_app)
        return current_app._memory_db

    if "db" not in g:
        g.db = _connect(current_app)
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    db = get_db() if app.config["DATABASE"] == ":memory:" else _connect(app)
    db.executescript(SCHEMA)
    db.commit()
    if app.config["DATABASE"] != ":memory:":
        db.close()


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db(current_app)
    click.echo("Initialized the database.")
