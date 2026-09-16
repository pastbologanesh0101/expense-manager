"""WSGI/CLI entry point for ``flask run``.

Usage:
    export FLASK_APP=wsgi.py
    flask run
"""

from expense_app import create_app

app = create_app()
