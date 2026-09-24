"""
412. Fizz Buzz  ·  Easy  ·  Math & Geometry
https://leetcode.com/problems/fizz-buzz/
(Not in the Blind 75. Extra practice.)

For 1..n return "FizzBuzz" when a number divides by both 3 and 5, "Fizz" for 3,
"Buzz" for 5, otherwise the number as a string.
Constraints: 1 <= n <= 10^4.

Pattern:     simulation with ordered if/elif conditions
Complexity:  O(n) time, O(n) space for the answer list
Solved:      2026-09-24

Key insight
    Check the most specific case FIRST. 15 divides by 3 and by 5, so if the
    "divisible by 3" test comes first, 15 wrongly becomes "Fizz". Ordering the
    conditions from most to least specific is the whole problem.

Run the tests:  python3 leetcode/18_math_geometry/0412_fizz_buzz.py
"""
from typing import List


# ------------------------- my solution, as submitted -------------------------

# input : n: int
# output: list of n strings, numbered 1 to n
# todo  : for each number from 1 to n
#           divisible by 3 and 5 -> "FizzBuzz"
#           divisible by 3       -> "Fizz"
#           divisible by 5       -> "Buzz"
#           otherwise            -> the number itself as a string
# constraints: 1 <= n <= 10^4
#
# idea:
#   1. loop i from 1 to n
#   2. check divisible by 3 AND 5 first (the most specific case)
#   3. then 3, then 5, else the number as a string
#   4. append each result and return the list

class Solution:
    def fizzBuzz(self, n: int) -> list[str]:
        # step 1: declare the array of strings
        answer = []

        # step 2: loop from 1 to n
        # start at 1 because the answer is 1-indexed, n + 1 so n is included
        for i in range(1, n + 1):
            # divisible by 3 and 5: check this first
            if i % 3 == 0 and i % 5 == 0:
                answer.append("FizzBuzz")
            # divisible by 3 only
            elif i % 3 == 0:
                answer.append("Fizz")
            # divisible by 5 only
            elif i % 5 == 0:
                answer.append("Buzz")
            # otherwise the number itself, as a string
            else:
                answer.append(str(i))

        # step 3: return the array of strings
        return answer

# ------------------------------------------------------------------------------


def fizz_buzz_built(n: int) -> List[str]:
    """Build the word instead of listing every case.

    "Fizz" * True is "Fizz" and "Fizz" * False is "", so the two pieces join
    themselves, and `or str(i)` covers the empty case. Neat, and worth knowing,
    but the if/elif chain is easier for a reader to check at a glance.
    """
    return [("Fizz" * (i % 3 == 0) + "Buzz" * (i % 5 == 0)) or str(i)
            for i in range(1, n + 1)]


# Review notes
#
# 1. Correct, and both of your ordering notes are right. The tests below check
#    them by breaking the code on purpose:
#      - testing 3 before "3 and 5" turns 15 into "Fizz"
#      - using four separate `if`s instead of elif gives 15 three entries of
#        its own, so 1..15 produces 17 strings instead of 15
#
# 2. `i % 15 == 0` is the same test as `i % 3 == 0 and i % 5 == 0`, because a
#    number divisible by both 3 and 5 is divisible by 15 (they share no
#    factors). Either is fine; yours states the rule as the problem does.
#
# 3. `range(1, n + 1)` is exactly right: the list is 1-indexed and n itself
#    must be included. Off-by-one here is the other classic slip.
#
# 4. `str(i)` matters because the list holds strings. Returning ints passes
#    nothing: "1" != 1.
#
# 5. This is famous as an interview screening question. The point isn't
#    difficulty, it's whether the conditions are ordered correctly and the
#    loop bounds are right, first time.


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    versions = {"my solution": lambda n: Solution().fizzBuzz(n), "built": fizz_buzz_built}

    cases = [
        ("n = 1 (smallest allowed)", 1,  ["1"]),
        ("example 1",                3,  ["1", "2", "Fizz"]),
        ("example 2",                5,  ["1", "2", "Fizz", "4", "Buzz"]),
        ("example 3, reaches 15",    15, ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
                                          "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]),
    ]
    for name, n, want in cases:
        for label, fn in versions.items():
            got = fn(n)
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    # Largest allowed input, checked against the rules directly.
    n = 10_000
    got = Solution().fizzBuzz(n)
    assert len(got) == n
    for i, word in enumerate(got, start=1):
        if i % 15 == 0:
            assert word == "FizzBuzz", i
        elif i % 3 == 0:
            assert word == "Fizz", i
        elif i % 5 == 0:
            assert word == "Buzz", i
        else:
            assert word == str(i), i
    print(f"n = {n} (largest allowed): every entry follows the rules")

    # Note 1: the two mistakes your notes warn about, shown failing.
    def wrong_order(n):
        out = []
        for i in range(1, n + 1):
            if i % 3 == 0:                      # checked too early
                out.append("Fizz")
            elif i % 3 == 0 and i % 5 == 0:
                out.append("FizzBuzz")
            elif i % 5 == 0:
                out.append("Buzz")
            else:
                out.append(str(i))
        return out
    assert wrong_order(15)[14] == "Fizz" and Solution().fizzBuzz(15)[14] == "FizzBuzz"

    def separate_ifs(n):
        out = []
        for i in range(1, n + 1):
            if i % 3 == 0 and i % 5 == 0:
                out.append("FizzBuzz")
            if i % 3 == 0:                      # `if`, not `elif`
                out.append("Fizz")
            if i % 5 == 0:
                out.append("Buzz")
            if i % 3 and i % 5:
                out.append(str(i))
        return out
    assert len(separate_ifs(15)) == 17 and len(Solution().fizzBuzz(15)) == 15
    print("note 1 confirmed: checking 3 first makes 15 'Fizz'; separate ifs give 17 entries, not 15")

    # Note 2: % 15 is the same test.
    assert all((i % 15 == 0) == (i % 3 == 0 and i % 5 == 0) for i in range(1, 10_001))
    print("note 2 confirmed: i % 15 == 0 matches 'divisible by 3 and 5' for every i up to 10,000")
