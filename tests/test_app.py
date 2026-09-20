import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from expense_app import create_app
from expense_app.db import close_db


class ExpenseManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

    def tearDown(self):
        memory_db = getattr(self.app, "_memory_db", None)
        if memory_db is not None:
            memory_db.close()
        with self.app.app_context():
            close_db()

    def add_expense(self, date="2026-01-15", category="Food", amount="20.00",
                     note="Lunch"):
        return self.client.post(
            "/add",
            data={"date": date, "category": category, "amount": amount, "note": note},
            follow_redirects=True,
        )

    def test_add_expense_success(self):
        response = self.add_expense()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Expense added.", response.data)
        self.assertIn(b"Food", response.data)

    def test_list_expenses_shows_added_expense(self):
        self.add_expense(category="Rent", amount="900.00", note="September rent")
        response = self.client.get("/expenses")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Rent", response.data)
        self.assertIn(b"900.00", response.data)

    def test_list_expenses_empty_state(self):
        response = self.client.get("/expenses")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No expenses yet.", response.data)

    def test_summary_totals_by_category_and_month(self):
        self.add_expense(date="2026-01-05", category="Food", amount="10.00")
        self.add_expense(date="2026-01-20", category="Food", amount="15.00")
        self.add_expense(date="2026-02-01", category="Travel", amount="100.00")

        response = self.client.get("/summary")
        self.assertEqual(response.status_code, 200)
        body = response.data.decode()

        # Category totals: Food = 25.00, Travel = 100.00
        self.assertIn("Food", body)
        self.assertIn("25.00", body)
        self.assertIn("Travel", body)
        self.assertIn("100.00", body)

        # Month totals: 2026-01 = 25.00, 2026-02 = 100.00
        self.assertIn("2026-01", body)
        self.assertIn("2026-02", body)

        # Grand total: 125.00
        self.assertIn("125.00", body)

    def test_add_expense_rejects_missing_category(self):
        response = self.add_expense(category="")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Category is required.", response.data)

        # Confirm nothing was persisted.
        list_response = self.client.get("/expenses")
        self.assertIn(b"No expenses yet.", list_response.data)

    def test_add_expense_rejects_invalid_amount(self):
        response = self.add_expense(amount="not-a-number")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amount must be a number.", response.data)

    def test_add_expense_rejects_non_positive_amount(self):
        response = self.add_expense(amount="0")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amount must be greater than zero.", response.data)

    def test_add_expense_rejects_negative_amount(self):
        response = self.add_expense(amount="-15.00")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Amount must be greater than zero.", response.data)

        # Confirm nothing was persisted.
        list_response = self.client.get("/expenses")
        self.assertIn(b"No expenses yet.", list_response.data)

    def test_add_expense_rejects_whitespace_only_category(self):
        response = self.add_expense(category="   ")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Category is required.", response.data)

    def test_add_expense_rejects_bad_date_format(self):
        response = self.add_expense(date="15-01-2026")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Date must be in YYYY-MM-DD format.", response.data)

    def test_add_expense_get_renders_form(self):
        response = self.client.get("/add")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Expense", response.data)


if __name__ == "__main__":
    unittest.main()
