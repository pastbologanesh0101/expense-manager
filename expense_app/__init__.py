import os

from flask import Flask

from .db import close_db, get_db, init_db


def create_app(testing=False, db_path=None):
    """Application factory for the Expense Manager app.

    Args:
        testing: When True, configures the app for the test suite (enables
            Flask's TESTING mode and propagates exceptions).
        db_path: Optional explicit path to the SQLite database file. When not
            given, defaults to ``instance/expenses.sqlite`` for normal runs,
            or an in-memory database when ``testing`` is True.
    """
    app = Flask(__name__, instance_relative_config=True)

    if db_path is None:
        db_path = ":memory:" if testing else os.path.join(
            app.instance_path, "expenses.sqlite"
        )

    app.config.update(
        SECRET_KEY="dev-secret-key",
        DATABASE=db_path,
        TESTING=testing,
    )

    if db_path != ":memory:":
        os.makedirs(app.instance_path, exist_ok=True)

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db(app)

    from . import routes

    app.register_blueprint(routes.bp)

    return app
