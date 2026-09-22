"""
1480. Running Sum of 1d Array  ·  Easy  ·  Arrays & Hashing
https://leetcode.com/problems/running-sum-of-1d-array/
(Not in the Blind 75. Extra practice.)

Return a list where position i holds nums[0] + nums[1] + ... + nums[i].
Constraints: 1 <= len(nums) <= 1000, -10^6 <= nums[i] <= 10^6.

Pattern:     prefix sum (each total = the previous total + this number)
Complexity:  O(n) time, O(1) extra space besides the output list
Solved:      2026-09-22

Key insight
    Each running sum contains the previous one. Keep a single total and add
    one number at a time, instead of adding everything up again from the start.

Why this problem matters
    The list it builds is a PREFIX SUM, and prefix sums answer "what's the sum
    of nums[i..j]?" in O(1): prefix[j] - prefix[i - 1]. That's the tool behind
    harder problems like 303 (Range Sum Query) and 560 (Subarray Sum Equals K).

Run the tests:  python3 leetcode/01_arrays_hashing/1480_running_sum_of_1d_array.py
"""
from itertools import accumulate
from typing import List


# ------------------------- my solution, as submitted -------------------------

# 1480. Running Sum of 1d Array (Easy)
#
# input : nums: list of ints
# output: list where each spot = sum of all numbers up to that spot
# todo  : runningSum[i] = nums[0] + nums[1] + ... + nums[i]
# constraints: 1 <= len(nums) <= 1000, -10^6 <= nums[i] <= 10^6
#
# idea (prefix sum):
#   each running sum = previous running sum + current number
#   so keep one total, add each number to it, and save the total
#
#   nums:     1   2   3   4
#   total:    1   3   6   10
#                 ↑
#             1 + 2 = 3
#
# remember:
#   - total starts at 0, so the first number needs no special case
#   - never re-add from the start each time (that's O(n^2))
#   - complexity: O(n) time, O(n) space for the result
#   - test: [1,2,3,4] -> [1,3,6,10] | [1,1,1,1,1] -> [1,2,3,4,5] | [3,1,2,10,1] -> [3,4,6,16,17]

class Solution:
    def runningSum(self, nums: list[int]) -> list[int]:
        # step 1: set up
        # runningSum = the answer list we fill in
        # total = the running sum so far (0 before the first number)
        runningSum = []
        total = 0

        # step 2: go through each number
        for val in nums:
            # add the current number to the running sum so far
            total += val
            # save this running sum as the next answer
            runningSum.append(total)

        # step 3: return the answer list
        return runningSum

# ------------------------------------------------------------------------------


# Review notes
#
# 1. Correct, and optimal: every number is added exactly once. Starting total
#    at 0 so the first number needs no special case is a good habit. The same
#    trick (a starting value that changes nothing) shows up everywhere.
#
# 2. Space: the output list is O(n), but the output usually isn't counted
#    (cheatsheets/00_complexity.md). Beyond it you use one variable, so this is
#    "O(1) extra space", which is the phrase an interviewer expects.
#
# 3. Style: Python names variables in snake_case (running_sum, or result).
#    Here `runningSum` also matches the method's name. It works, because the
#    method is self.runningSum and the variable is local, but a reader has to
#    stop and check.
#
# 4. Two shorter versions, both below:
#      - list(accumulate(nums)) from itertools does exactly this in one line.
#        Mention it, but expect to be asked to write the loop.
#      - In place: nums[i] += nums[i - 1] for i from 1. No extra list at all,
#        but it CHANGES the caller's list (the same trade-off as nums.sort()
#        in problem 268). Ask whether that's allowed first.
#
# 5. Overflow isn't an issue here, and the constraints are why: at most 1000
#    numbers of size 10^6 add up to at most 10^9, which fits in a 32-bit int
#    (limit about 2.1 * 10^9). Python's ints never overflow anyway, but in
#    Java or C++ that bound is what makes a plain int safe.


def running_sum_accumulate(nums: List[int]) -> List[int]:
    """Note 4: the standard-library one-liner."""
    return list(accumulate(nums))


def running_sum_in_place(nums: List[int]) -> List[int]:
    """Note 4: no extra list, but it overwrites the input."""
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]
    return nums


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random

    versions = {
        "my solution": lambda nums: Solution().runningSum(list(nums)),
        "accumulate": lambda nums: running_sum_accumulate(list(nums)),
        "in place": lambda nums: running_sum_in_place(list(nums)),
    }

    cases = [
        ("example 1",           [1, 2, 3, 4],           [1, 3, 6, 10]),
        ("example 2",           [1, 1, 1, 1, 1],        [1, 2, 3, 4, 5]),
        ("example 3",           [3, 1, 2, 10, 1],       [3, 4, 6, 16, 17]),
        ("one number",          [7],                    [7]),
        ("negatives",           [-1, -2, 3],            [-1, -3, 0]),
        ("zeros",               [0, 0, 0],              [0, 0, 0]),
        ("extremes",            [10**6, -10**6, 10**6], [10**6, 0, 10**6]),
    ]
    for name, nums, want in cases:
        for label, fn in versions.items():
            got = fn(nums)
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(1000):
        nums = [rng.randint(-10**6, 10**6) for _ in range(rng.randint(1, 60))]
        want = [sum(nums[:i + 1]) for i in range(len(nums))]     # the O(n^2) way
        for label, fn in versions.items():
            assert fn(nums) == want, f"{label} on {nums}"
    print("1000 random arrays: all versions match re-adding from the start each time")

    # Note 4: the in-place version changes the caller's list; yours doesn't.
    original = [1, 2, 3]
    Solution().runningSum(original)
    assert original == [1, 2, 3]
    running_sum_in_place(original)
    assert original == [1, 3, 6]
    print("note 4 confirmed: your version leaves the input alone, the in-place one overwrites it")

    # Note 5: the largest possible running sum fits in a 32-bit int.
    worst = Solution().runningSum([10**6] * 1000)[-1]
    assert worst == 10**9 < 2**31 - 1
    print(f"note 5 confirmed: the largest possible total is {worst:,}, under the 32-bit limit {2**31 - 1:,}")

    # Why it matters: range sums in O(1) from the prefix sums.
    nums = [3, 1, 2, 10, 1]
    prefix = Solution().runningSum(nums)
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            fast = prefix[j] - (prefix[i - 1] if i else 0)
            assert fast == sum(nums[i:j + 1])
    print("prefix sums confirmed: every range sum nums[i..j] equals prefix[j] - prefix[i-1]")
