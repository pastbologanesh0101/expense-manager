"""Print a plain-text monthly spending report from the expense database.

This demonstrates reading the app's data programmatically without going
through the web UI — useful for a quick end-of-month review, or as a
starting point for exporting data to another tool.

Usage:

    python3 examples/monthly_report.py [YYYY-MM]

If no month is given, defaults to the current month. Reads from the same
database `python app.py` uses (`instance/expenses.sqlite`), so run this
after you've added a few expenses through the app.
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from expense_app import create_app  # noqa: E402
from expense_app.db import get_db  # noqa: E402


def monthly_report(month):
    app = create_app()
    with app.app_context():
        db = get_db()
        rows = db.execute(
            "SELECT category, amount, note FROM expense"
            " WHERE substr(date, 1, 7) = ? ORDER BY amount DESC",
            (month,),
        ).fetchall()
        total = sum(row["amount"] for row in rows)

    if not rows:
        print(f"No expenses recorded for {month}.")
        return

    print(f"Spending report for {month}")
    print("-" * 40)
    for row in rows:
        note = f" ({row['note']})" if row["note"] else ""
        print(f"  {row['category']:<15} ${row['amount']:>8.2f}{note}")
    print("-" * 40)
    print(f"  {'Total':<15} ${total:>8.2f}")


if __name__ == "__main__":
    target_month = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime("%Y-%m")
    monthly_report(target_month)
