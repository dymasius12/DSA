"""
268. Missing Number  ·  Easy  ·  Blind 75  ·  Bit Manipulation
https://leetcode.com/problems/missing-number/

nums holds n distinct numbers taken from the range [0, n]. Exactly one number
from that range is absent. Return it.
Constraints: n == len(nums), 1 <= n <= 10^4, 0 <= nums[i] <= n, all distinct.

Pattern:     "array of 0..n with one missing" -> sum formula, XOR, or
             index-as-value. Sorting works but isn't the intended answer.
Complexity:  mine O(n log n); the sum and XOR versions are O(n) / O(1)
Solved:      2026-09-16

Key insight
    The range [0, n] holds n + 1 numbers, but the array has only n slots, so
    exactly one is left out.

    n is len(nums), NEVER max(nums). The largest value can itself be the
    missing one: [0, 1] has max 1, but n is 2 and 2 is the answer.

Three ways to do it
    1. Sort, then the first index where value != index is the answer (mine).
    2. Sum: 0..n adds up to n(n+1)/2, so subtract the actual sum.
    3. XOR: a ^ a == 0, so XOR every index with every value and the pairs
       cancel, leaving the missing number.

Run the tests:  python3 leetcode/17_bit_manipulation/0268_missing_number.py
"""
from typing import List


# ------------------------- my solution, as submitted -------------------------

# input: nums: list[int], n distinct ints from [0, n] -- output: int
# todo: return the one number in [0, n] missing from nums
# careful: n == len(nums), 1 <= n <= 10^4, 0 <= nums[i] <= n
# idea: n = len(nums) is the top of the RANGE (not always max(nums)).
#       Sort, then the first index where value != index is the missing number.
#       If no mismatch, the missing number is n.

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        # the idea is we sort the array first
        nums.sort()
        # find n from the size of nums
        n = len(nums)
        # traverse the sorted array and see if the number is not the index
        # because after being sorted, the index should reflect the number
        for i, x in enumerate(nums):
            # if index is not equal the element then return that number because it is missing
            if x != i:
                # return that number, the index, not the element
                return i
        # but if the missing number is at the last index and last element, return n
        return n

# ------------------------------------------------------------------------------


def missing_number_sum(nums: List[int]) -> int:
    """Gauss sum, the optimal answer. O(n) time, O(1) space.

    0 + 1 + ... + n equals n(n + 1) / 2. Subtract what's actually there and
    the difference is the missing number. No special cases at all.
    Trace: [3, 0, 1] -> expected 6, actual 4, answer 2.
    """
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


def missing_number_xor(nums: List[int]) -> int:
    """XOR. O(n) time, O(1) space, and the reason this sits in Bit Manipulation.

    a ^ a == 0 and a ^ 0 == a. XOR-ing every index 0..n with every value makes
    each present number cancel with its own index, leaving only the number
    that has no partner. Start at n, because indices only reach n - 1.
    Trace: [0, 1] -> res starts at 2; 0^0 and 1^1 cancel; answer 2.
    """
    res = len(nums)
    for i, x in enumerate(nums):
        res ^= i ^ x
    return res


# Review notes
#
# 1. Your solution is correct, and the reasoning behind it is the part that
#    matters: n comes from len(nums), not max(nums). That's the trap in this
#    problem and you named it before writing code.
#
# 2. Checking value against index also catches a missing 0 for free: [1, 2]
#    sorts to [1, 2], index 0 holds 1, so it returns 0 immediately. And the
#    `return n` at the end is genuinely needed, not defensive padding: when
#    nothing is missing inside the array, the answer is n itself.
#
# 3. Two things to say out loud about sorting:
#      - O(n log n) is slower than needed. The sum and XOR versions are O(n),
#        and an interviewer will usually push you toward one of them.
#      - `nums.sort()` MUTATES the caller's list. If the caller still needs
#        the original order, that's a bug. `sorted(nums)` copies instead,
#        which costs O(n) space. The tests below confirm the mutation.
#
# 4. Your note that XOR "avoids overflow risk in Java/C++" is right, and worth
#    saying in an interview. n(n+1)/2 with large n can overflow a 32-bit int
#    in those languages. Python integers grow as needed, so the sum version is
#    safe here, but the interviewer may not be thinking in Python.
#
# 5. Python note from your write-up, confirmed: `for i in len(nums)` raises
#    TypeError, because an int isn't iterable. Use `range(len(nums))` for
#    indices, or `enumerate(nums)` when you want both index and value.


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random

    def brute_force(nums):
        return (set(range(len(nums) + 1)) - set(nums)).pop()

    versions = {
        "my solution (sort)": lambda nums: Solution().missingNumber(list(nums)),
        "sum": missing_number_sum,
        "xor": missing_number_xor,
    }

    cases = [
        ("example 1, missing in the middle", [3, 0, 1],                        2),
        ("example 2, missing n (the end)",   [0, 1],                           2),
        ("example 3",                        [9, 6, 4, 2, 3, 5, 7, 0, 1],      8),
        ("missing 0 (the start)",            [1, 2],                           0),
        ("one element, 0 present",           [0],                              1),
        ("one element, 1 present",           [1],                              0),
        ("already sorted, missing last",     [0, 1, 2, 3],                     4),
    ]
    for name, nums, want in cases:
        for label, fn in versions.items():
            got = fn(list(nums))
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(500):
        n = rng.randint(1, 60)
        missing = rng.randint(0, n)
        nums = [x for x in range(n + 1) if x != missing]
        rng.shuffle(nums)
        for label, fn in versions.items():
            got = fn(list(nums))
            assert got == missing == brute_force(list(nums)), f"{label} failed on {nums}"
    print("500 random arrays: all three versions match the brute force")

    n = 10_000                      # the largest input the constraints allow
    big = [x for x in range(n + 1) if x != 7_777]
    rng.shuffle(big)
    assert {fn(list(big)) for fn in versions.values()} == {7_777}
    print(f"n = {n} (largest allowed): all three agree")

    # Note 1: the max(nums) trap.
    nums = [0, 1]
    assert max(nums) == 1 and len(nums) == 2 and missing_number_sum(nums) == 2
    print("note 1 confirmed: [0, 1] has max 1 but the answer is 2, so n must be len(nums)")

    # Note 3: nums.sort() changes the caller's list; sorted() doesn't.
    original = [3, 0, 1]
    Solution().missingNumber(original)
    assert original == [0, 1, 3], original
    untouched = [3, 0, 1]
    missing_number_xor(untouched)
    assert untouched == [3, 0, 1]
    print("note 3 confirmed: the sort version reordered the caller's list, XOR left it alone")

    # Note 5: `for i in len(nums)` is a TypeError.
    try:
        for _i in len([1, 2]):
            pass
        raise AssertionError("expected TypeError")
    except TypeError:
        print("note 5 confirmed: `for i in len(nums)` raises TypeError")
