"""
1431. Kids With the Greatest Number of Candies  ·  Easy  ·  Arrays & Hashing
https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/
(Not in the Blind 75. Extra practice.)

For each kid, say whether giving THEM all the extra candies would leave them
with the greatest number among all the kids. Ties count as greatest.
Constraints: 2 <= n <= 100, 1 <= candies[i] <= 100, 1 <= extraCandies <= 50.

Pattern:     precompute one value, then a single pass
Complexity:  O(n) time, O(n) for the output (O(1) besides it)
Solved:      2026-10-07

Key insight
    The extras are a "what if" for one kid at a time, so nobody else's count
    ever changes. That means the bar is fixed: max(candies) of the ORIGINAL
    list. Compute it once, then every kid is a single comparison.

    Easy to miss: if you recomputed the maximum inside the loop, the answers
    would still be right, but the work becomes O(n^2) for no reason.

Run the tests:  python3 leetcode/01_arrays_hashing/1431_kids_with_the_greatest_number_of_candies.py
"""
from typing import List


# ------------------------- my solution, as submitted -------------------------

# 1431. Kids With the Greatest Number of Candies (Easy)
#
# input : candies: list of ints, extraCandies: int
# output: list of booleans, same length as candies
# todo  : result[i] is True if candies[i] + extraCandies reaches the greatest
#         count among all kids (ties count as greatest)
# constraints: 2 <= n <= 100, 1 <= candies[i] <= 100, 1 <= extraCandies <= 50
#
# ideas:
#   1. find the greatest count in the ORIGINAL array, once, before the loop
#   2. for each kid, check if their count + extraCandies reaches that greatest
#   3. the comparison is already True/False, so append it directly
#
#   [2,3,5,1,3] extra=3   best = 5
#   2+3=5 >= 5 True | 3+3=6 True | 5+3=8 True | 1+3=4 False | 3+3=6 True
#
# remember:
#   - use >= not >: multiple kids can tie for greatest
#   - the extras go to ONE kid at a time, so the others keep their original
#     counts; that is why max(candies) is computed once, not recomputed
#   - never put max(candies) inside the loop: that makes it O(n^2)
#   - "for c in candies" instead of "for i in range(len(candies))":
#     use it whenever the index itself is never needed
#   - a comparison IS a boolean, so no if/else is needed to append True/False
#   - complexity: O(n) time, O(n) space for the result
#   - test: [2,3,5,1,3],3 -> [T,T,T,F,T] | [4,2,1,1,2],1 -> [T,F,F,F,F]
#           [12,1,12],10 -> [T,F,T]

class Solution:
    def kidsWithCandies(self, candies: list[int], extraCandies: int) -> list[bool]:
        # step 1: the greatest count among the kids right now
        best = max(candies)                           # computed once, before the loop

        # step 2: check each kid against the best
        result = []
        for c in candies:
            result.append(c + extraCandies >= best)   # >= because ties still count

        # step 3: return the boolean array
        return result

# ------------------------------------------------------------------------------


class SolutionFirstDraft:
    """My earlier version: an index loop and an explicit if/else.

    Same answers and the same complexity. Kept to show the two changes that
    make the final version shorter (see notes 3 and 4).
    """

    def kidsWithCandies(self, candies: list[int], extraCandies: int) -> list[bool]:
        greatest = max(candies)
        result = []
        for i in range(0, len(candies)):
            if candies[i] + extraCandies >= greatest:
                result.append(True)
            else:
                result.append(False)
        return result


def kids_with_candies_comprehension(candies: List[int], extra: int) -> List[bool]:
    """The same loop as a list comprehension: the usual Python version."""
    best = max(candies)
    return [c + extra >= best for c in candies]


# Review notes
#
# 1. Correct. Checked against a brute force that literally does what the
#    problem describes (copy the list, add the extras to kid i, then ask
#    whether that kid now holds the maximum) on 5,000 random inputs.
#
# 2. `>=` instead of `>` is the single most important character here, and
#    your note says why: ties count. It matters exactly when a kid lands ON
#    the maximum rather than above it. Example 1 is that case: kid 1 has
#    2 + 3 = 5, which equals the best, so `>` would answer
#    [False, True, True, False, True] instead of [True, True, True, False, True].
#    (Example 3 doesn't catch this: there the extras overshoot the maximum,
#    so `>` and `>=` agree. Worth testing the exact-tie case on purpose.)
#
# 3. Dropping the index (`for c in candies`) is the right call whenever you
#    never use `i`. Also, `range(0, len(candies))` and `range(len(candies))`
#    are identical: 0 is the default start.
#
# 4. `result.append(c + extra >= best)` instead of if/else is the bigger
#    improvement, and it generalises: `x > y` already evaluates to True or
#    False, so `if cond: return True else: return False` is always just
#    `return cond`.
#
# 5. Space: the output is O(n), but besides it you keep only one number, so
#    say "O(1) extra space" in an interview (cheatsheets/00_complexity.md).
#
# 6. `max(candies)` would raise ValueError on an empty list. The constraints
#    promise at least 2 kids, so it's safe here. Worth noticing rather than
#    guarding: "n >= 2, so max() is safe" is a good thing to say out loud.


# ----------------------------------- tests ------------------------------------

def _brute_force(candies, extra):
    """Do exactly what the problem says, one kid at a time."""
    out = []
    for i in range(len(candies)):
        hypothetical = list(candies)
        hypothetical[i] += extra
        out.append(hypothetical[i] == max(hypothetical))
    return out


if __name__ == "__main__":
    import random

    versions = {
        "my solution": lambda c, e: Solution().kidsWithCandies(list(c), e),
        "first draft": lambda c, e: SolutionFirstDraft().kidsWithCandies(list(c), e),
        "comprehension": lambda c, e: kids_with_candies_comprehension(list(c), e),
        "brute force": _brute_force,
    }

    T, F = True, False
    cases = [
        ("example 1",                  [2, 3, 5, 1, 3],  3,  [T, T, T, F, T]),
        ("example 2",                  [4, 2, 1, 1, 2],  1,  [T, F, F, F, F]),
        ("example 3",                  [12, 1, 12],      10, [T, F, T]),
        ("exact tie decides it",       [2, 5],           3,  [T, T]),
        ("two kids (smallest n)",      [1, 2],           1,  [T, T]),
        ("everyone already equal",     [5, 5, 5],        1,  [T, T, T]),
        ("extras enough for everyone", [1, 2, 3],        50, [T, T, T]),
        ("one kid far ahead",          [100, 1, 1],      1,  [T, F, F]),
        ("largest allowed values",     [100] * 100,      50, [T] * 100),
    ]
    for name, candies, extra, want in cases:
        for label, fn in versions.items():
            got = fn(candies, extra)
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(5000):
        candies = [rng.randint(1, 100) for _ in range(rng.randint(2, 100))]
        extra = rng.randint(1, 50)
        want = _brute_force(candies, extra)
        for label in ("my solution", "first draft", "comprehension"):
            assert versions[label](candies, extra) == want, f"{label} on {candies}, {extra}"
    print("5000 random inputs: all versions match the literal 'give the extras to kid i' check")

    # Note 2: why >= and not >.
    def with_strict_greater(candies, extra):
        best = max(candies)
        return [c + extra > best for c in candies]
    assert with_strict_greater([2, 3, 5, 1, 3], 3) == [F, T, T, F, T]
    assert Solution().kidsWithCandies([2, 3, 5, 1, 3], 3) == [T, T, T, F, T]
    assert with_strict_greater([12, 1, 12], 10) == Solution().kidsWithCandies([12, 1, 12], 10)
    print("note 2 confirmed: with > instead of >=, example 1 drops kid 1, who ties "
          "exactly ([F,T,T,F,T] instead of [T,T,T,F,T]); example 3 wouldn't catch it")

    # Note 4: a comparison is already a boolean.
    assert (3 >= 2) is True and isinstance(3 >= 2, bool)
    print("note 4 confirmed: `3 >= 2` IS True, so if/else around it adds nothing")

    # Note 6: max() needs a non-empty list; the constraints guarantee one.
    try:
        max([])
        raise AssertionError("expected ValueError")
    except ValueError:
        print("note 6 confirmed: max([]) raises ValueError, but n >= 2 rules that out")
