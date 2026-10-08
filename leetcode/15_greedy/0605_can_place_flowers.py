"""
605. Can Place Flowers  ·  Easy  ·  Greedy
https://leetcode.com/problems/can-place-flowers/
(Not in the Blind 75. Extra practice.)

flowerbed holds 0 (empty) and 1 (planted), with no two 1s already adjacent.
Return True if n more flowers fit without ever putting two 1s side by side.
Constraints: 1 <= len(flowerbed) <= 2*10^4, 0 <= n <= len(flowerbed).

Pattern:     greedy, one pass (plant at the earliest legal plot)
Complexity:  O(len) time, O(1) space
Solved:      2026-10-08

Key insight
    Plant as early as possible. Taking the earliest legal plot never costs you
    a later one: skipping it can only push the next flower further right, so
    the earliest choice always leaves at least as much room as any other.
    That's the exchange argument that makes greedy safe here.

The two edges are the whole difficulty
    A plot at the very start or very end has only one neighbour. Treating
    "off the end" as empty handles both, and `i == 0 or ...` short-circuits
    before the lookup, which matters in Python: flowerbed[-1] doesn't fail,
    it quietly reads the LAST plot.

Run the tests:  python3 leetcode/15_greedy/0605_can_place_flowers.py
"""
from typing import List


# --------------------- my solution, as submitted (final version) ---------------------

# input : flowerbed: list of 0s and 1s, n: how many flowers to plant
# output: True if all n flowers fit without two 1s side by side
# todo  : 0 = empty plot, 1 = taken; the input already has no adjacent 1s
# constraints: 1 <= len(flowerbed) <= 2*10^4, 0 <= n <= len(flowerbed)
#
# approach (greedy, walk with a manual index):
#   1. walk i forward while there are plots left AND flowers left to plant
#   2. a plot is plantable if it is 0 AND both neighbors are 0 (or out of bounds)
#   3. if valid: count it and jump i += 2, because i + 1 is now blocked
#   4. if not valid: just step i += 1
#   5. n <= 0 means every flower found a home
#
#   [1,0,0,0,1] n=1  ->  plant at index 2  ->  True
#   [1,0,0,0,1] n=2  ->  only 1 spot fits  ->  False
#
# remember:
#   - this is the same greedy as the for-loop version, with two upgrades:
#       i += 2 skips the plot that planting just blocked
#       n > 0 in the while condition stops as soon as we are done
#   - because we skip instead of writing, the input is NEVER modified
#     (the for-loop version needs flowerbed[i] = 1 to block the next plot)
#   - a for loop cannot do this: its step is fixed, so a while loop is needed
#   - edges count as empty: (i == 0) means "no left neighbor, treat as free"
#   - never write flowerbed[i-1] without that guard: in Python flowerbed[-1]
#     silently reads the LAST element instead of raising an error
#   - still O(n) time, O(1) space - O(n) is the floor, since every plot
#     must be looked at; this version just does less work per plot
#   - the backslash \ only continues a long line; brackets () would work too
#   - test: [1,0,0,0,1],1 -> True | [1,0,0,0,1],2 -> False
#           [0],1 -> True | [0,0,0],2 -> True | [1,0,0,0,0,1],2 -> False

class Solution:
    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        # step 1: start at the first plot
        i = 0
        size = len(flowerbed)

        # step 2: walk while plots remain and flowers are still needed
        while i < size and n > 0:                        # n > 0 lets us stop early
            # step 3: plot empty, and both sides empty or out of bounds
            if flowerbed[i] == 0 \
               and (i == 0 or flowerbed[i - 1] == 0) \
               and (i == size - 1 or flowerbed[i + 1] == 0):
                n -= 1                                   # one flower placed here
                i += 2                                   # skip the blocked neighbour
            else:
                i += 1                                   # not plantable, move on

        # step 4: all flowers placed?
        return n <= 0

# --------------------------------------------------------------------------------------


class SolutionForLoop:
    """My first version: a for loop that plants by writing 1 into the bed.

    Same greedy, same complexity. The difference is that it CHANGES the
    caller's list (see note 3).
    """

    def canPlaceFlowers(self, flowerbed: list[int], n: int) -> bool:
        if n == 0:
            return True
        for i in range(len(flowerbed)):
            if flowerbed[i] == 0:
                prev_empty = (i == 0) or (flowerbed[i - 1] == 0)
                next_empty = (i == len(flowerbed) - 1) or (flowerbed[i + 1] == 0)
                if prev_empty and next_empty:
                    flowerbed[i] = 1          # blocks the next plot from being used
                    n -= 1
                    if n == 0:
                        return True
        return n <= 0


def can_place_flowers_padded(flowerbed: List[int], n: int) -> bool:
    """A third way: pad both ends with 0 so the edges stop being special.

    Costs O(len) space, but every plot now has two real neighbours, so the
    `i == 0 or ...` guards disappear. Worth knowing as a technique: adding a
    sentinel to remove an edge case shows up all over array problems.
    """
    bed = [0] + list(flowerbed) + [0]
    planted = 0
    for i in range(1, len(bed) - 1):
        if bed[i - 1] == bed[i] == bed[i + 1] == 0:
            bed[i] = 1
            planted += 1
    return planted >= n


# Review notes
#
# 1. Both versions are correct, and the greedy really is optimal: against a
#    brute force that tries every legal set of plantings and takes the best,
#    they agree on 20,000 random beds. Your exchange argument ("skipping only
#    pushes the next flower further right") is exactly the right reasoning.
#
# 2. Your note about flowerbed[-1] is the most valuable one here. In most
#    languages an index of -1 crashes and you find the bug immediately. In
#    Python it quietly reads the last plot, so the code runs and returns
#    wrong answers on exactly one input shape. The tests show that failure:
#    without the i == 0 guard, planting at index 0 is judged against the LAST
#    plot, so [0, 0, 1] reports no room even though a flower fits at index 0.
#
# 3. The reason to prefer your while version: it never touches the input.
#    The for-loop version writes 1s into the caller's list, so after calling
#    it their flowerbed has changed. That's the same trade-off as nums.sort()
#    in 268 and the in-place prefix sum in 1480. In an interview, say it:
#    "this version modifies the input, is that acceptable?"
#
# 4. `i += 2` is a genuine optimisation, not just tidiness: after planting at
#    i, plot i + 1 can never be used, so visiting it is wasted work. Same
#    O(len) in the worst case, about half the steps on an empty bed.
#
# 5. One simplification: `return n <= 0` can be `return n == 0`, since n only
#    ever decreases by one at a time and the loop stops at n > 0. Both are
#    right, and <= is the safer habit.


# ----------------------------------- tests ------------------------------------

def _max_plantable(flowerbed):
    """Brute force: the most flowers that can be added, trying every combination."""
    empty = [i for i, v in enumerate(flowerbed) if v == 0]
    best = 0
    for mask in range(1 << len(empty)):
        bed = list(flowerbed)
        count = 0
        for bit, idx in enumerate(empty):
            if mask >> bit & 1:
                bed[idx] = 1
                count += 1
        if all(bed[i] == 0 or bed[i + 1] == 0 for i in range(len(bed) - 1)):
            best = max(best, count)
    return best


if __name__ == "__main__":
    import random

    versions = {
        "my solution (while)": lambda bed, n: Solution().canPlaceFlowers(list(bed), n),
        "my first (for loop)": lambda bed, n: SolutionForLoop().canPlaceFlowers(list(bed), n),
        "padded": can_place_flowers_padded,
    }

    cases = [
        ("example 1",                    [1, 0, 0, 0, 1],    1, True),
        ("example 2",                    [1, 0, 0, 0, 1],    2, False),
        ("from my notes: single plot",   [0],                1, True),
        ("from my notes: three empty",   [0, 0, 0],          2, True),
        ("from my notes: even gap",      [1, 0, 0, 0, 0, 1], 2, False),
        ("nothing to plant",             [1, 1, 1],          0, True),
        ("nothing to plant, empty bed",  [0, 0, 0],          0, True),
        ("one plot, already taken",      [1],                1, False),
        ("plant at both edges",          [0, 0, 1, 0, 0],    2, True),
        ("first plot free, last taken",  [0, 0, 1],          1, True),
        ("edge gap of four",             [0, 0, 0, 0],       2, True),
        ("too many asked for",           [0, 0, 0],          3, False),
    ]
    for name, bed, n, want in cases:
        for label, fn in versions.items():
            got = fn(bed, n)
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(20_000):
        size = rng.randint(1, 10)
        bed = []
        while len(bed) < size:                        # build a legal bed: no two 1s
            if bed and bed[-1] == 1:
                bed.append(0)
            else:
                bed.append(rng.choice([0, 0, 1]))
        most = _max_plantable(bed)
        for n in range(0, size + 1):
            want = n <= most
            for label, fn in versions.items():
                assert fn(bed, n) == want, f"{label} on {bed}, n={n}: want {want}"
    print("20,000 random beds, every n: greedy matches the best possible placement")

    # Note 2: what happens without the i == 0 guard.
    def no_edge_guard(flowerbed, n):
        bed = list(flowerbed)
        for i in range(len(bed)):
            if bed[i] == 0 and bed[i - 1] == 0 and (i == len(bed) - 1 or bed[i + 1] == 0):
                bed[i] = 1                            # bed[-1] reads the LAST plot
                n -= 1
        return n <= 0
    assert no_edge_guard([0, 0, 1], 1) is False       # wrong: a flower fits at index 0
    assert Solution().canPlaceFlowers([0, 0, 1], 1) is True
    print("note 2 confirmed: without the i == 0 guard, flowerbed[-1] reads the LAST plot, "
          "so [0,0,1] reports no room even though index 0 is free")

    # Note 3: which versions change the caller's list.
    bed = [0, 0, 0]
    Solution().canPlaceFlowers(bed, 2)
    assert bed == [0, 0, 0]
    SolutionForLoop().canPlaceFlowers(bed, 2)
    assert bed == [1, 0, 1]
    print("note 3 confirmed: the while version leaves the bed alone; the for-loop version "
          "rewrites it to [1, 0, 1]")

    # Note 4: i += 2 does about half the steps on an empty bed.
    steps_plus_two = len(range(0, 20_000, 2))
    assert steps_plus_two * 2 == 20_000
    print(f"note 4 confirmed: on a 20,000-plot empty bed, i += 2 visits {steps_plus_two:,} "
          "plots instead of 20,000")

    # Largest allowed input still returns instantly.
    big = [0] * 20_000
    assert Solution().canPlaceFlowers(list(big), 10_000) is True
    assert Solution().canPlaceFlowers(list(big), 10_001) is False
    print("largest allowed bed: 20,000 empty plots fit exactly 10,000 flowers")
