"""Entry point for running the Expense Manager app with ``python app.py``.

For development you can also use ``flask run`` after setting:

    export FLASK_APP=wsgi.py
"""

from expense_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
