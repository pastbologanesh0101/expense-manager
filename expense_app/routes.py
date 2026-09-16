from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("expenses", __name__)


def _parse_amount(raw_amount):
    """Return (amount, error_message). amount is None if invalid."""
    if raw_amount is None or raw_amount.strip() == "":
        return None, "Amount is required."
    try:
        amount = float(raw_amount)
    except ValueError:
        return None, "Amount must be a number."
    if amount <= 0:
        return None, "Amount must be greater than zero."
    return amount, None


def _parse_date(raw_date):
    """Return (date_string, error_message)."""
    if raw_date is None or raw_date.strip() == "":
        return None, "Date is required."
    try:
        datetime.strptime(raw_date, "%Y-%m-%d")
    except ValueError:
        return None, "Date must be in YYYY-MM-DD format."
    return raw_date, None


@bp.route("/")
def index():
    return redirect(url_for("expenses.list_expenses"))


@bp.route("/add", methods=("GET", "POST"))
def add_expense():
    errors = []
    form = {
        "date": date.today().isoformat(),
        "category": "",
        "amount": "",
        "note": "",
    }

    if request.method == "POST":
        form["date"] = request.form.get("date", "")
        form["category"] = request.form.get("category", "").strip()
        form["amount"] = request.form.get("amount", "")
        form["note"] = request.form.get("note", "").strip()

        clean_date, date_error = _parse_date(form["date"])
        if date_error:
            errors.append(date_error)

        if not form["category"]:
            errors.append("Category is required.")

        clean_amount, amount_error = _parse_amount(form["amount"])
        if amount_error:
            errors.append(amount_error)

        if not errors:
            db = get_db()
            db.execute(
                "INSERT INTO expense (date, category, amount, note)"
                " VALUES (?, ?, ?, ?)",
                (clean_date, form["category"], clean_amount, form["note"]),
            )
            db.commit()
            flash("Expense added.", "success")
            return redirect(url_for("expenses.list_expenses"))

        for error in errors:
            flash(error, "error")

    return render_template("add_expense.html", form=form)


@bp.route("/expenses")
def list_expenses():
    db = get_db()
    rows = db.execute(
        "SELECT id, date, category, amount, note FROM expense"
        " ORDER BY date DESC, id DESC"
    ).fetchall()
    return render_template("list_expenses.html", expenses=rows)


@bp.route("/summary")
def summary():
    db = get_db()
    by_category = db.execute(
        "SELECT category, SUM(amount) AS total"
        " FROM expense GROUP BY category ORDER BY total DESC"
    ).fetchall()
    by_month = db.execute(
        "SELECT substr(date, 1, 7) AS month, SUM(amount) AS total"
        " FROM expense GROUP BY month ORDER BY month DESC"
    ).fetchall()
    grand_total = db.execute("SELECT SUM(amount) AS total FROM expense").fetchone()[
        "total"
    ]
    return render_template(
        "summary.html",
        by_category=by_category,
        by_month=by_month,
        grand_total=grand_total or 0,
    )
