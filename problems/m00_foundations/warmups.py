"""Module 00 warm-ups — get the Python toolkit into your fingers.

Fill in each function. Delete the `pass` and write the body.
Run `./check 00` until everything is green.
"""
from collections import Counter, defaultdict


def char_frequency(s: str) -> dict:
    """Return a dict mapping each character in `s` to how many times it appears.

    char_frequency("aabc") -> {'a': 2, 'b': 1, 'c': 1}
    char_frequency("")     -> {}

    Do it twice: once with a plain dict and `.get(c, 0)`, then delete that and
    do it with `Counter`. Feel the difference.

    Target: O(n) time, O(k) space where k = distinct characters.
    """
    pass


def has_duplicate(nums: list) -> bool:
    """Return True if any value appears more than once.

    has_duplicate([1, 2, 3, 1]) -> True
    has_duplicate([1, 2, 3])    -> False
    has_duplicate([])           -> False

    The naive way is a nested loop: O(n^2). Don't do that.
    Use a set. This is THE trade from the notes: O(n) memory buys O(n) time.

    Target: O(n) time, O(n) space.
    """
    pass


def group_by_first_letter(words: list) -> dict:
    """Group words by their first character, preserving input order in each group.

    group_by_first_letter(["apple", "ant", "bee"])
        -> {'a': ['apple', 'ant'], 'b': ['bee']}
    group_by_first_letter([]) -> {}

    Use `defaultdict(list)` so you never write an `if key not in d` check.
    Return a plain dict (a defaultdict compares equal to one, so either passes,
    but get in the habit of `dict(d)`).

    Target: O(n) time.
    """
    pass


def make_grid(rows: int, cols: int, fill: int = 0) -> list:
    """Return a rows x cols 2-D list where every cell is `fill`.

    make_grid(2, 3) -> [[0, 0, 0], [0, 0, 0]]

    THE TRAP: `[[fill] * cols] * rows` creates `rows` references to ONE list.
    Mutating grid[0][0] would change every row. The test checks for exactly
    this. Use a list comprehension.

    Target: O(rows * cols) time and space.
    """
    pass
