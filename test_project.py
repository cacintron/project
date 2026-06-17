"""Tests for the Student Budget Planner.

Run with:  pytest
"""

import pytest

from project import (
    validate_amount,
    categorize_expenses,
    category_breakdown,
    months_to_goal,
    format_currency,
    remove_expense,
)


def test_validate_amount():
    assert validate_amount("50") == 50.0
    assert validate_amount("50.25") == 50.25
    assert validate_amount("$1,200.50") == 1200.50
    assert validate_amount("  10  ") == 10.0
    with pytest.raises(ValueError):
        validate_amount("abc")
    with pytest.raises(ValueError):
        validate_amount("-5")
    with pytest.raises(ValueError):
        validate_amount("")


def test_categorize_expenses():
    expenses = [
        ("Food", 10.0),
        ("Food", 5.50),
        ("Transport", 20.0),
    ]
    totals = categorize_expenses(expenses)
    assert totals == {"Food": 15.50, "Transport": 20.0}
    assert categorize_expenses([]) == {}


def test_category_breakdown():
    totals = {"Food": 25.0, "Transport": 75.0}
    breakdown = category_breakdown(totals)
    assert breakdown[0] == ("Transport", 75.0, 75.0)
    assert breakdown[1] == ("Food", 25.0, 25.0)
    assert sum(row[2] for row in breakdown) == 100.0
    assert category_breakdown({}) == []


def test_months_to_goal():
    assert months_to_goal(1000, 700, 100) == 3
    assert months_to_goal(1000, 700, 99) == 4
    assert months_to_goal(500, 500, 100) == 0
    assert months_to_goal(500, 600, 100) == 0
    assert months_to_goal(1000, 0, 0) is None


def test_format_currency():
    assert format_currency(0) == "$0.00"
    assert format_currency(1200.5) == "$1,200.50"
    assert format_currency(5) == "$5.00"


def test_remove_expense():
    expenses = [("Food", 10.0), ("Rent", 800.0), ("Transport", 20.0)]
    removed = remove_expense(expenses, 2)
    assert removed == ("Rent", 800.0)
    assert expenses == [("Food", 10.0), ("Transport", 20.0)]
    with pytest.raises(IndexError):
        remove_expense(expenses, 5)
    with pytest.raises(IndexError):
        remove_expense(expenses, 0)
    with pytest.raises(IndexError):
        remove_expense([], 1)
