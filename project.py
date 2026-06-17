"""Student Budget Planner.

A command-line program that helps students track monthly income and
expenses, see a category-by-category breakdown of where their money
goes, and find out how long it will take to reach a savings goal.

Run with:  python project.py
"""

import sys


CATEGORIES = [
    "Rent",
    "Food",
    "Transport",
    "Tuition",
    "Books",
    "Entertainment",
    "Subscriptions",
    "Other",
]


def validate_amount(value):
    """Convert a user-supplied string into a non-negative float.

    Accepts plain numbers ("50"), decimals ("50.25") and values that
    include a currency symbol or commas ("$1,200.50"). Raises ValueError
    on anything that is not a valid, non-negative amount.
    """
    if value is None:
        raise ValueError("No amount provided.")

    cleaned = str(value).strip().replace("$", "").replace(",", "")
    if cleaned == "":
        raise ValueError("No amount provided.")

    amount = float(cleaned)
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    return round(amount, 2)


def categorize_expenses(expenses):
    """Total a list of expenses by category.

    `expenses` is a list of (category, amount) tuples. Returns a dict
    mapping each category that appears to the sum of its amounts,
    rounded to two decimal places.
    """
    totals = {}
    for category, amount in expenses:
        totals[category] = round(totals.get(category, 0) + amount, 2)
    return totals


def category_breakdown(category_totals):
    """Turn category totals into a sorted percentage breakdown.

    Given a dict of {category: total}, returns a list of
    (category, total, percent_of_spending) tuples sorted from the
    largest total to the smallest. Percentages sum to ~100. If there is
    no spending, returns an empty list.
    """
    grand_total = sum(category_totals.values())
    if grand_total <= 0:
        return []

    breakdown = []
    for category, total in category_totals.items():
        percent = round((total / grand_total) * 100, 1)
        breakdown.append((category, round(total, 2), percent))

    breakdown.sort(key=lambda row: row[1], reverse=True)
    return breakdown


def months_to_goal(goal, current_savings, monthly_contribution):
    """Return the whole number of months needed to reach a savings goal.

    If the goal is already met, returns 0. If the monthly contribution
    is zero or negative and the goal is not yet met, the goal can never
    be reached, so returns None.
    """
    if goal <= current_savings:
        return 0
    if monthly_contribution <= 0:
        return None

    remaining = goal - current_savings
    import math

    return math.ceil(remaining / monthly_contribution)


def format_currency(amount):
    """Format a number as a US dollar string, e.g. 1200.5 -> '$1,200.50'."""
    return "${:,.2f}".format(amount)


def summarize(income, expenses):
    """Build a human-readable summary report as a single string.

    Combines the total income, total spending, remaining balance and a
    full category breakdown into formatted text suitable for printing.
    """
    totals = categorize_expenses(expenses)
    total_spent = sum(totals.values())
    remaining = round(income - total_spent, 2)

    lines = []
    lines.append("=" * 40)
    lines.append("        MONTHLY BUDGET SUMMARY")
    lines.append("=" * 40)
    lines.append(f"Income:    {format_currency(income)}")
    lines.append(f"Spent:     {format_currency(total_spent)}")
    lines.append(f"Remaining: {format_currency(remaining)}")
    lines.append("-" * 40)

    breakdown = category_breakdown(totals)
    if not breakdown:
        lines.append("No expenses recorded yet.")
    else:
        lines.append("Spending by category:")
        for category, total, percent in breakdown:
            lines.append(
                f"  {category:<14} {format_currency(total):>12}  ({percent}%)"
            )

    if remaining < 0:
        lines.append("-" * 40)
        lines.append("WARNING: You are over budget!")
    lines.append("=" * 40)
    return "\n".join(lines)


def prompt_amount(message):
    """Ask the user for an amount until they enter a valid one."""
    while True:
        try:
            return validate_amount(input(message))
        except ValueError as error:
            print(f"  Invalid amount: {error}")


def add_expense(expenses):
    """Interactively collect one expense and append it to `expenses`."""
    print("\nCategories: " + ", ".join(CATEGORIES))
    category = input("Expense category: ").strip().title()
    if category not in CATEGORIES:
        print(f"  '{category}' is not a known category; filing under 'Other'.")
        category = "Other"
    amount = prompt_amount("Amount spent: ")
    expenses.append((category, amount))
    print(f"  Added {format_currency(amount)} to {category}.")


def remove_expense(expenses, index):
    """Remove and return the expense at a 1-based position in the list.

    `index` is the number shown to the user (the first expense is 1).
    Raises IndexError if there is no expense at that position so the
    caller can warn the user instead of deleting the wrong item.
    """
    if index < 1 or index > len(expenses):
        raise IndexError("No expense at that position.")
    return expenses.pop(index - 1)


def delete_expense(expenses):
    """Interactively show the expenses and delete the one the user picks."""
    if not expenses:
        print("  There are no expenses to delete yet.")
        return

    print("\nYour expenses:")
    for position, (category, amount) in enumerate(expenses, start=1):
        print(f"  {position}) {category:<14} {format_currency(amount)}")

    choice = input("Number to delete (or blank to cancel): ").strip()
    if choice == "":
        print("  Cancelled; nothing was deleted.")
        return
    try:
        index = int(choice)
    except ValueError:
        print("  That is not a valid number.")
        return
    try:
        category, amount = remove_expense(expenses, index)
    except IndexError as error:
        print(f"  {error}")
        return
    print(f"  Deleted {format_currency(amount)} from {category}.")


def main():
    print("Welcome to the Student Budget Planner!\n")
    income = prompt_amount("Enter your total monthly income: ")
    expenses = []

    while True:
        print("\nMenu:")
        print("  1) Add an expense")
        print("  2) Delete an expense")
        print("  3) View budget summary")
        print("  4) Check a savings goal")
        print("  5) Quit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            delete_expense(expenses)
        elif choice == "3":
            print("\n" + summarize(income, expenses))
        elif choice == "4":
            goal = prompt_amount("Savings goal: ")
            current = prompt_amount("Current savings: ")
            monthly = prompt_amount("Amount you can save each month: ")
            months = months_to_goal(goal, current, monthly)
            if months is None:
                print("  With no monthly savings, you can't reach that goal.")
            elif months == 0:
                print("  Great news - you've already reached your goal!")
            else:
                print(
                    f"  At {format_currency(monthly)}/month you'll reach "
                    f"{format_currency(goal)} in {months} month(s)."
                )
        elif choice == "5":
            print("\nFinal report:")
            print(summarize(income, expenses))
            print("\nGoodbye, and happy saving!")
            sys.exit(0)
        else:
            print("  Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
