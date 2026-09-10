"""Module 01 — Arrays & Hashing.

Read notes/01_arrays_hashing.md first.

For each function: state the time and space complexity OUT LOUD before you
write code. Then write it. Then run ./check 01

If you're stuck for 25 minutes, read the solution, close it, and rewrite it
from memory tomorrow. That is not cheating — that is the method.
"""
from collections import Counter, defaultdict


def contains_duplicate(nums: list) -> bool:
    """LC 217. True if any value appears at least twice.

    [1,2,3,1] -> True      [1,2,3,4] -> False

    Shape 1 from the notes: a set for membership.
    Target: O(n) time, O(n) space.
    """
    pass


def is_anagram(s: str, t: str) -> bool:
    """LC 242. True if t is a rearrangement of s.

    ("anagram", "nagaram") -> True     ("rat", "car") -> False

    Two ways: sort both (O(n log n)), or count both (O(n)). Do the counting one.
    Check the lengths first — it's a free early exit.
    Target: O(n) time, O(1) space (alphabet is bounded).
    """
    pass


def two_sum(nums: list, target: int) -> list:
    """LC 1. Return indices of the two numbers adding to target.

    ([2,7,11,15], 9) -> [0, 1]
    Exactly one solution exists. You may not use the same element twice.
    Return the indices in ascending order.

    Shape 3: map value -> index, and look for the COMPLEMENT (target - x).
    Order matters: check the map BEFORE inserting the current number,
    or [3,3] with target 6 will match itself.
    Target: O(n) time, O(n) space.
    """
    pass


def group_anagrams(strs: list) -> list:
    """LC 49. Group words that are anagrams of each other.

    ["eat","tea","tan","ate","nat","bat"]
        -> [["eat","tea","ate"], ["tan","nat"], ["bat"]]

    Order of the groups doesn't matter, and order within a group doesn't matter
    (the test sorts before comparing).

    Shape 4: compute a key that is IDENTICAL for anagrams, then group on it.
    A list can't be a dict key. What hashable thing is the same for "eat" and
    "tea"?
    Target: O(n * k log k) time, k = max word length.
    """
    pass


def top_k_frequent(nums: list, k: int) -> list:
    """LC 347. The k most frequent elements, in any order.

    ([1,1,1,2,2,3], 2) -> [1, 2]

    Easy version: Counter + sort by count. That's O(n log n).
    Better: bucket sort. A value's frequency can be at most len(nums), so make
    buckets[freq] = [values with that frequency] and walk it from the end.
    That's O(n). Try for the O(n) version.
    """
    pass


def product_except_self(nums: list) -> list:
    """LC 238. res[i] = product of every element EXCEPT nums[i]. No division.

    [1,2,3,4] -> [24,12,8,6]

    The prefix/suffix trick from the notes.
    Pass 1 (left->right): res[i] = product of everything to the LEFT of i.
    Pass 2 (right->left): multiply in the product of everything to the RIGHT,
                          carried in a single running variable.
    Target: O(n) time, O(1) extra space (the output array doesn't count).
    """
    pass


def longest_consecutive(nums: list) -> int:
    """LC 128. Length of the longest run of consecutive integers.

    [100,4,200,1,3,2] -> 4        (the run 1,2,3,4)
    [] -> 0

    Sorting is O(n log n) and the problem wants O(n). Put everything in a set,
    then only START counting from a number whose predecessor is absent.
    Without that guard you re-walk the same run from every member -> O(n^2).
    Target: O(n) time, O(n) space.
    """
    pass


def encode(strs: list) -> str:
    """LC 271. Encode a list of strings into ONE string.

    encode(["neet", "code"]) -> some string that decode() can reverse

    The catch: any separator you pick could appear inside a string. ["a#b"]
    must survive. So a plain "#".join() is wrong.

    The fix is length-prefixing: write each string as <length>#<string>.
    "neet" -> "4#neet". Now the reader knows exactly how many characters to
    take and never has to guess where a string ends.

    Target: O(n) time over the total characters.
    """
    pass


def decode(s: str) -> list:
    """LC 271. Reverse `encode`. decode(encode(x)) must equal x for any x.

    Walk with a pointer: read digits until '#', that's the length; take that
    many characters; jump past them; repeat.

    decode("") -> []
    """
    pass


def is_valid_sudoku(board: list) -> bool:
    """LC 36. Is the 9x9 board valid SO FAR? (Empty cells are '.')

    Valid means: no repeated digit in any row, column, or 3x3 box.
    You do NOT need to check solvability, only current conflicts.

    Shape 1 + shape 4: three defaultdict(set)s — by row, by column, by box.
    The box index is the trick: (r // 3, c // 3).
    Target: O(1) — the board size is fixed at 81 cells.
    """
    pass
