"""
2216. Minimum Deletions to Make Array Beautiful  ·  Medium  ·  Greedy
https://leetcode.com/problems/minimum-deletions-to-make-array-beautiful/
(Not in the Blind 75. Extra practice.)

An array is beautiful if its length is even and nums[i] != nums[i + 1] for
every even i: it splits into pairs, and each pair holds two DIFFERENT numbers.
An empty array is beautiful. Return the fewest deletions that make nums
beautiful.
Constraints: 1 <= len(nums) <= 10^5, 0 <= nums[i] <= 10^5.

Pattern:     greedy: pair each number with the first different number after it
Complexity:  mine O(n) time, O(n) space; the versions below are O(1) space
Solved:      2026-09-17

Key insight: turn it around
    Every number you keep ends up in a pair, so
        deletions = len(nums) - 2 * (number of pairs)
    Minimizing deletions is the same as MAXIMIZING the number of pairs.

Why the greedy choice is always safe (the part that makes this a Medium)
    Walk left to right with at most one number "waiting" for a partner.

    - x equals the waiting number: they can't pair, so one must go. Deleting x
      or deleting the waiting number leaves the exact same situation (the same
      value waiting), so deleting x loses nothing.

    - x is different: pair them now. Suppose a better solution skipped x and
      paired the waiting number with some later y instead. Swap y for x: the
      pair is still valid (x differs from it), and y is now free, so the
      swapped solution has at least as many pairs. Pairing with the EARLIEST
      valid partner leaves the most numbers available for future pairs.

    Neither choice can ever be beaten, so making them one at a time gives the
    maximum number of pairs, which means the minimum deletions.

Run the tests:  python3 leetcode/15_greedy/2216_minimum_deletions_to_make_array_beautiful.py
"""
from typing import List


# ------------------------- my solution, as submitted -------------------------

# input : nums: list of ints
# output: minimum number of elements to delete from nums
# todo  : make nums beautiful by deleting as few elements as possible
#
# beautiful means:
#   - len(nums) is even
#   - nums[i] != nums[i + 1] for every even i
#   - in plain words: the array splits into pairs, and each pair has two DIFFERENT numbers
#   - an empty array counts as beautiful
#
# constraints:
#   - 1 <= len(nums) <= 10^5
#   - 0 <= nums[i] <= 10^5
#
# ideas (dance partners):
#   1. build the beautiful array (kept) one number at a time
#   2. if kept has an EVEN length, nobody is waiting:
#        x starts a new pair, so always keep it
#   3. if kept has an ODD length, the last number is waiting for a partner:
#        x is different -> keep it (pair complete)
#        x is the same  -> skip it (deletions += 1)
#   4. at the end, if kept has an odd length, the last number has no partner:
#        delete it too (deletions += 1)
#
# remember:
#   - kept[-1] = the last number in kept (the one waiting)
#   - len(kept) % 2 == 1 means "someone is waiting alone"
#   - no need for len(nums): loop over values, check the length of kept instead
#   - complexity: O(n) time, O(n) space (for kept)
#   - test: [1,1,2,3,5] -> 1 | [1,1,2,2,3,3] -> 2 | [5] -> 1 | [2,2,2] -> 3

class Solution:
    def minDeletion(self, nums: List[int]) -> int:
        # step 1: set up
        # kept = the beautiful array we are building
        # deletions = how many numbers we skipped
        kept = []
        deletions = 0

        # step 2: take each number x, one at a time
        for x in nums:
            # check if someone is waiting for a partner
            # odd length (1, 3, 5...) means the last kept number has no partner yet
            waiting = len(kept) % 2 == 1

            # step 3: decide whether to keep or skip x
            # bad pair: someone is waiting AND x is the same number as them
            if waiting and kept[-1] == x:
                # skip x; the waiting number keeps waiting
                deletions += 1
            else:
                # good: x either starts a new pair or completes the waiting one
                kept.append(x)

        # step 4: fix the leftover
        # odd length means the last number never found a partner, so delete it
        if len(kept) % 2 == 1:
            deletions += 1

        # step 5: return the total number of deletions
        return deletions

# ------------------------------------------------------------------------------


# Review notes
#
# 1. Correct. It matches a brute force that tries EVERY possible set of
#    deletions (tests below), which is the real proof for a greedy solution.
#    The four examples in your notes are all right, including [2,2,2] -> 3.
#
# 2. The dance-partner framing is exactly the greedy argument, and your header
#    already states the O(n) space cost of `kept`. That's the one thing to
#    improve.
#
# 3. `kept` is never read except for two facts: whether its length is odd,
#    and its last value. So you don't need the list, only the waiting number.
#    See min_deletion_waiting below: same logic, O(1) space.
#
# 4. A trap when you make that change: use `waiting is None`, NOT
#    `not waiting`. 0 is a valid value here (0 <= nums[i]), and `not 0` is
#    True, so a waiting 0 would be treated as "nobody waiting".
#    [0, 0] should need 2 deletions; the `not waiting` version returns 1.
#    (The tests confirm this.)


def min_deletion_waiting(nums: List[int]) -> int:
    """Your idea with note 3 applied: keep only the waiting number. O(1) space."""
    deletions = 0
    waiting = None                      # the number waiting for a partner, or None
    for x in nums:
        if waiting is None:             # nobody waiting: x starts a pair
            waiting = x
        elif waiting == x:              # same number: can't pair, skip x
            deletions += 1
        else:                           # different: pair complete
            waiting = None
    if waiting is not None:             # leftover with no partner
        deletions += 1
    return deletions


def min_deletion_index(nums: List[int]) -> int:
    """The common editorial version: no list and no waiting variable.

    After `deletions` removals, nums[i] has shifted left to position
    i - deletions. It starts a pair when that position is even; if it equals
    the next number, delete it.
    """
    deletions = 0
    for i in range(len(nums) - 1):
        if (i - deletions) % 2 == 0 and nums[i] == nums[i + 1]:
            deletions += 1
    if (len(nums) - deletions) % 2 == 1:
        deletions += 1
    return deletions


# ----------------------------------- tests ------------------------------------

def _brute_force(nums):
    """Try every subset of positions to keep; smallest deletions wins."""
    n = len(nums)
    best = n                             # deleting everything is always valid
    for mask in range(1 << n):
        kept = [nums[i] for i in range(n) if mask >> i & 1]
        if len(kept) % 2 == 0 and all(kept[i] != kept[i + 1] for i in range(0, len(kept), 2)):
            best = min(best, n - len(kept))
    return best


if __name__ == "__main__":
    import random

    versions = {
        "my solution": lambda nums: Solution().minDeletion(nums),
        "waiting (O(1))": min_deletion_waiting,
        "index shift (O(1))": min_deletion_index,
    }

    cases = [
        ("example 1",                       [1, 1, 2, 3, 5],          1),
        ("example 2",                       [1, 1, 2, 2, 3, 3],       2),
        ("one element",                     [5],                      1),
        ("all the same, odd",               [2, 2, 2],                3),
        ("all the same, even",              [2, 2, 2, 2],             4),
        ("already beautiful",               [1, 2, 3, 4],             0),
        ("pairs equal across the boundary", [1, 2, 2, 3],             0),
        ("zeros",                           [0, 0],                   2),
        ("zero waiting, then a partner",    [0, 0, 1],                1),
    ]
    for name, nums, want in cases:
        for label, fn in versions.items():
            got = fn(list(nums))
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    trials = 3000
    for _ in range(trials):
        nums = [rng.randint(0, 2) for _ in range(rng.randint(1, 12))]   # small range -> many repeats
        want = _brute_force(nums)
        for label, fn in versions.items():
            assert fn(list(nums)) == want, f"{label} disagrees with brute force on {nums}"
    print(f"{trials} random arrays (up to 12 long): all versions match the brute force")

    big = [rng.randint(0, 3) for _ in range(100_000)]
    assert len({fn(list(big)) for fn in versions.values()}) == 1
    print("100,000 elements (largest allowed): all versions agree")

    # Note 4: the `not waiting` trap with value 0.
    def buggy(nums):
        deletions, waiting = 0, None
        for x in nums:
            if not waiting:          # BUG: treats a waiting 0 as nobody waiting
                waiting = x
            elif waiting == x:
                deletions += 1
            else:
                waiting = None
        return deletions + (waiting is not None)
    assert buggy([0, 0]) == 1 and min_deletion_waiting([0, 0]) == 2
    print("note 4 confirmed: `not waiting` gives 1 for [0, 0]; `waiting is None` gives the correct 2")
