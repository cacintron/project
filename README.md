# Student Budget Planner

#### Video Demo: <URL HERE>

#### Description:

The Student Budget Planner is a command-line program written in Python that
helps a student take control of their monthly money. As a student myself, I
wanted a project that solved a real problem I actually have: knowing where my
money goes each month and figuring out how long it will take to save up for
something I want. Instead of opening a spreadsheet and fighting with formulas,
this program lets me type in my income, log my expenses one at a time, and
instantly see a clean summary of my spending broken down by category, along
with a projection of how many months it will take to reach a savings goal.

When you run the program with `python project.py`, it greets you and asks for
your total monthly income. From there it presents a simple menu loop with four
choices: add an expense, view a budget summary, check a savings goal, or quit.
This menu repeats until you choose to quit, so you can add as many expenses as
you like and view your summary as often as you want. Each expense is filed
under one of eight categories (Rent, Food, Transport, Tuition, Books,
Entertainment, Subscriptions, or Other). If you type a category the program
does not recognize, it gently files the expense under "Other" rather than
crashing or throwing the entry away. When you quit, the program prints one
final report so you leave with a complete picture of your month.

#### Files

**project.py** is the heart of the project. It contains the `main` function and
several additional functions, all defined at the top level so they can be
imported and tested individually. `main` runs the welcome message and the menu
loop that ties everything together. The supporting functions each do one small,
well-defined job:

- `validate_amount` takes whatever string the user types and converts it into a
  clean, non-negative float. It strips out dollar signs, commas and surrounding
  whitespace, so input like `$1,200.50` is accepted just as easily as `50`. If
  the input is empty, negative, or not a number, it raises a `ValueError`, which
  the program catches so it can re-prompt the user instead of crashing.
- `categorize_expenses` takes the running list of `(category, amount)` tuples
  and totals them up into a dictionary keyed by category. This is the function
  that turns a long list of individual purchases into meaningful subtotals.
- `category_breakdown` takes those category totals and converts them into a
  sorted list of `(category, total, percent)` tuples, ordered from the biggest
  spending category to the smallest. The percentages show what share of your
  total spending each category represents, which is the single most useful piece
  of information for spotting where your money is really going.
- `months_to_goal` answers the savings question. Given a goal amount, your
  current savings, and how much you can put aside each month, it returns the
  whole number of months you need, rounding partial months up. If you have
  already met your goal it returns `0`, and if you are saving nothing each month
  it returns `None` to signal that the goal can never be reached.
- `format_currency` is a small helper that formats any number as a tidy US
  dollar string with commas and two decimal places, keeping all the output
  consistent.
- `summarize`, `prompt_amount`, and `add_expense` handle the presentation and
  interactive input. `summarize` builds the full report as a single string,
  which makes it easy to read and would make it easy to test as well.

**test_project.py** contains pytest tests for five of the custom functions
(`validate_amount`, `categorize_expenses`, `category_breakdown`,
`months_to_goal`, and `format_currency`). The assignment only requires three,
but I tested five because the pure, logic-only functions are exactly the ones
where a quiet bug would do the most damage. Each test checks normal cases as
well as edge cases, such as empty input, negative amounts, already-met goals,
and the unreachable-goal case. You can run them all with the `pytest` command
from inside the project folder.

**requirements.txt** lists the one external library the project depends on,
`pytest`, which is needed to run the test suite. The program itself uses only
the Python standard library (`sys` and `math`), so it runs anywhere without
extra installation.

#### Design choices

A few decisions are worth explaining. First, I deliberately separated the
"thinking" functions from the "talking" functions. Functions like
`categorize_expenses` and `months_to_goal` take plain arguments and return plain
values, never calling `input` or `print`. This keeps them easy to test and easy
to reason about, while the interactive parts (`main`, `add_expense`,
`prompt_amount`) handle the messy job of talking to the user. Second, I chose to
make the program forgiving: bad amounts trigger a re-prompt instead of a crash,
and unknown categories fall back to "Other." Third, I used `math.ceil` in
`months_to_goal` because saving "3.2 months" is meaningless in practice — you
need a whole fourth month to actually cross the finish line. Finally, I kept the
data in memory for a single session rather than saving to a file, because the
goal was a clear, self-contained planning tool, and that scope let me focus on
getting the budgeting logic correct and thoroughly tested.

#### Acknowledgments

A few of the simpler helper functions in `project.py` — namely
`format_currency` and `validate_amount` — were initially generated by ChatGPT
(OpenAI). I then attached that starter code to my project and adapted it to fit
my needs, adjusting the currency formatting style, the input cleaning rules, and
the error handling so they matched the rest of the program. All of the core
budgeting logic, the menu flow, and the test suite were written and assembled by
me.
