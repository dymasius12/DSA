"""
1672. Richest Customer Wealth  ·  Easy  ·  Arrays & Hashing
https://leetcode.com/problems/richest-customer-wealth/
(Not in the Blind 75. Extra practice.)

accounts[i][j] is how much money customer i has in bank j. A customer's wealth
is their row's total. Return the largest wealth.
Constraints: 1 <= m, n <= 50, 1 <= accounts[i][j] <= 100.

Pattern:     nested loop over a grid, keeping a running maximum
Complexity:  O(m * n) time, O(1) space
Solved:      2026-09-24

Key insight
    A row is one customer, a column is one bank. So the answer is "the biggest
    row total", and you never need to store the individual totals: compare
    each one against the best so far and move on.

Run the tests:  python3 leetcode/01_arrays_hashing/1672_richest_customer_wealth.py
"""
from typing import List


# ------------------------- my solution, as submitted -------------------------

# input : accounts grid, accounts[i][j] = money of customer i in bank j
# output: the wealth of the richest customer
# todo  : wealth = sum of one customer's row; return the biggest wealth
# constraints: 1 <= m, n <= 50, 1 <= accounts[i][j] <= 100
#
# idea:
#   1. each row is one customer; sum the row to get their wealth
#   2. keep the biggest wealth seen so far (richest)
#   3. if a new customer's wealth is bigger, replace richest
#   4. return richest

class Solution:
    def maximumWealth(self, accounts: list[list[int]]) -> int:
        # step 1: richest wealth so far starts at 0
        richest = 0

        # step 2: go through each customer (each row)
        for customer in accounts:
            # add up all of this customer's bank accounts
            wealth = 0
            for money in customer:
                wealth += money

            # if this customer is richer, replace richest
            if wealth > richest:
                richest = wealth

        # step 3: return the richest wealth
        return richest

# ------------------------------------------------------------------------------


def maximum_wealth_short(accounts: List[List[int]]) -> int:
    """Your own shorter version: sum() per row, max() to keep the best."""
    richest = 0
    for customer in accounts:
        richest = max(richest, sum(customer))
    return richest


def maximum_wealth_one_line(accounts: List[List[int]]) -> int:
    """The same thing in one line. map(sum, ...) sums every row."""
    return max(map(sum, accounts))


# Review notes
#
# 1. Correct and optimal: you have to look at every amount at least once, so
#    O(m * n) is the floor. Space is O(1), since only two numbers are kept.
#
# 2. Starting `richest` at 0 is safe HERE, and it's worth knowing exactly why:
#    the constraints say every amount is at least 1, so no wealth can be
#    negative. If negative balances were allowed, starting at 0 would return 0
#    for a grid of all-negative rows, which is wrong. The habit that always
#    works is to start from the first row's total, or float('-inf').
#    (The tests show the all-negative case failing that way.)
#
# 3. Your note "don't name a variable max" is a good one. `max = 0` replaces
#    the built-in max() for the rest of that scope, so a later max(a, b)
#    raises TypeError: 'int' object is not callable. Same for list, sum, str,
#    id, type. The tests confirm this.
#
# 4. Your shorter version is the one to write in an interview: the explicit
#    inner loop adds nothing once you know sum(). max(map(sum, accounts)) is
#    shorter still, but the loop version reads more clearly to more people.


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random

    versions = {
        "my solution": lambda a: Solution().maximumWealth(a),
        "short": maximum_wealth_short,
        "one line": maximum_wealth_one_line,
    }

    cases = [
        ("example 1, tie",        [[1, 2, 3], [3, 2, 1]],            6),
        ("example 2",             [[1, 5], [7, 3], [3, 5]],          10),
        ("example 3",             [[2, 8, 7], [7, 1, 3], [1, 9, 5]], 17),
        ("one customer, one bank", [[100]],                          100),
        ("one customer, many banks", [[1, 2, 3, 4]],                 10),
        ("many customers, one bank", [[1], [50], [7]],               50),
        ("richest is first",      [[9, 9], [1, 1]],                  18),
        ("largest allowed grid",  [[100] * 50] * 50,                 5000),
    ]
    for name, accounts, want in cases:
        for label, fn in versions.items():
            got = fn([row[:] for row in accounts])
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(1000):
        m, n = rng.randint(1, 8), rng.randint(1, 8)
        accounts = [[rng.randint(1, 100) for _ in range(n)] for _ in range(m)]
        want = max(sum(row) for row in accounts)
        for label, fn in versions.items():
            assert fn(accounts) == want, f"{label} on {accounts}"
    print("1000 random grids: all versions agree")

    # Note 2: why richest = 0 is only safe because amounts are >= 1.
    negative = [[-5, -2], [-9, -1]]
    assert Solution().maximumWealth(negative) == 0        # wrong, if it were allowed
    assert maximum_wealth_one_line(negative) == -7        # the true biggest row total
    print("note 2 confirmed: with negative balances, starting at 0 would return 0 "
          "instead of -7 (the constraints rule this out)")

    # Note 3: shadowing a built-in.
    try:
        max = 0                                            # noqa: A001
        max(1, 2)
        raise AssertionError("expected TypeError")
    except TypeError:
        del max
        print("note 3 confirmed: naming a variable `max` makes max(1, 2) raise TypeError")
