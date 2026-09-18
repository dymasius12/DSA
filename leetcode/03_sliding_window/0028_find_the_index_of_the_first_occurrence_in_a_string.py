"""
28. Find the Index of the First Occurrence in a String  ·  Easy  ·  Sliding Window
https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
(Not in the Blind 75. Extra practice.)

Return the index where needle first appears in haystack, or -1 if it never does.
Constraints: 1 <= len(haystack), len(needle) <= 10^4, lowercase letters only.
needle can be LONGER than haystack.

Pattern:     fixed-size sliding window (compare each window with needle)
Complexity:  O(h * n) time, O(n) space (the slice, see note 2); KMP is O(h + n)
Solved:      2026-09-18

Key insight
    Every possible match starts somewhere in 0 .. h - n. Check each start in
    order and the first hit is the answer. The window never changes size, so
    it's the simplest kind of sliding window.

Worst case
    haystack = "aaaa...ab", needle = "aa...ab": nearly every window matches
    almost all the way before failing, so each check costs about n. That's
    where O(h * n) comes from, and it's why KMP exists.

Run the tests:  python3 leetcode/03_sliding_window/0028_find_the_index_of_the_first_occurrence_in_a_string.py
"""


# ------------------------- my solution, as submitted -------------------------

# 28. Find the Index of the First Occurrence in a String (Easy)
#
# input : haystack string, needle string -- output: int index
# todo  : find the index of the first occurrence of needle in haystack, else -1
# constraints: 1 <= len(haystack), len(needle) <= 10^4, lowercase letters only
#
# idea: sliding window
#   1. find h = len(haystack) and n = len(needle)
#   2. take a window of n characters starting at index i
#   3. if the window equals needle, return i
#      if not, slide the window one step right
#   4. the last window starts at h - n; if none matched, return -1
#
# remember:
#   - haystack[i:i + n] cuts out n characters starting at i (end is excluded)
#   - range(h - n + 1) includes the last valid start (h - n)
#   - bigger length first: h - n, never n - h (negative range = loop never runs)
#   - two strings compare directly with ==
#   - complexity: O(h * n) time, O(1) space (KMP does O(h + n) if asked)
#   - test: "sadbutsad","sad" -> 0 | "sadbutsad","but" -> 3 | "leetcode","leeto" -> -1 | "abc","abc" -> 0

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        # step 1: find the length of haystack and needle
        h = len(haystack)
        n = len(needle)

        # step 2: try every window start
        # +1 because range excludes the last number, and h - n is a valid start
        for i in range(h - n + 1):
            # step 3: the window is the n characters starting at i
            # i:i + n takes characters i up to i + n - 1 (the end is excluded)
            if haystack[i:i + n] == needle:
                return i

        # step 4: no window matched
        return -1

# ------------------------------------------------------------------------------


# Review notes
#
# 1. Correct, and the loop bound is exactly right. range(h - n + 1) covers the
#    last valid start, h - n. It also handles a needle LONGER than haystack
#    for free: h - n + 1 is then 0 or negative, the loop never runs, and you
#    return -1. The constraints allow that case, so it's worth knowing why
#    your code already handles it.
#
# 2. The space is O(n), not O(1). haystack[i:i + n] builds a NEW string of n
#    characters on every step (slices copy, the same lesson as problem 121).
#    Each copy is freed before the next one, so the peak is one window, O(n).
#
#    But DON'T "fix" it by comparing character by character
#    (str_str_no_slice below). That really is O(1) space, and in the worst-
#    case test it's hundreds of times SLOWER: about 2.5 s against 3 ms when
#    measured. The slice copy and == run in C; the character loop runs in
#    Python. Big-O counts them the same, and the constant factor doesn't.
#    Your version is the better answer. Just state its space as O(n).
#
# 3. `bigger length first: h - n` is a good note to keep. Written the other
#    way, range(n - h + 1) would search the wrong starts and give wrong
#    answers, silently.
#
# 4. In an interview, mention haystack.find(needle) exists (it returns -1 on
#    a miss, where haystack.index(needle) raises ValueError), then ask whether
#    you're allowed to use it. Usually the point is to write the loop.
#
# 5. Your KMP note is the right follow-up. KMP never re-reads a haystack
#    character: when a match fails, a precomputed table (lps) says how much of
#    the needle already matches, so the search resumes from there instead of
#    starting over. That makes it O(h + n). See str_str_kmp below.


def str_str_no_slice(haystack: str, needle: str) -> int:
    """Note 2: O(1) extra space, but far slower in Python. Only if asked."""
    h, n = len(haystack), len(needle)
    for i in range(h - n + 1):
        j = 0
        while j < n and haystack[i + j] == needle[j]:
            j += 1
        if j == n:
            return i
    return -1


def str_str_kmp(haystack: str, needle: str) -> int:
    """Note 5: Knuth-Morris-Pratt. O(h + n) time, O(n) space for the table."""
    n = len(needle)
    # lps[k] = length of the longest proper prefix of needle[:k+1] that is
    # also a suffix of it. "How much still matches if the next char fails."
    lps = [0] * n
    length = 0
    for k in range(1, n):
        while length and needle[k] != needle[length]:
            length = lps[length - 1]
        if needle[k] == needle[length]:
            length += 1
        lps[k] = length

    j = 0                                  # characters of needle matched so far
    for i, c in enumerate(haystack):
        while j and c != needle[j]:
            j = lps[j - 1]                 # fall back, don't restart
        if c == needle[j]:
            j += 1
            if j == n:
                return i - n + 1
    return -1


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random
    import time
    import tracemalloc

    versions = {
        "my solution": lambda h, n: Solution().strStr(h, n),
        "no slice": str_str_no_slice,
        "KMP": str_str_kmp,
    }

    cases = [
        ("example 1",                   "sadbutsad",   "sad",   0),
        ("example 2",                   "leetcode",    "leeto", -1),
        ("from my notes: middle",       "sadbutsad",   "but",   3),
        ("from my notes: whole string", "abc",         "abc",   0),
        ("needle at the very end",      "hello",       "llo",   2),
        ("needle longer than haystack", "a",           "aaa",   -1),
        ("single characters, match",    "a",           "a",     0),
        ("single characters, miss",     "a",           "b",     -1),
        ("overlapping candidates",      "aaa",         "aa",    0),
        ("KMP's classic case",          "mississippi", "issip", 4),
        ("near-miss prefix",            "aabaaab",     "aaab",  3),
    ]
    for name, hay, ndl, want in cases:
        for label, fn in versions.items():
            got = fn(hay, ndl)
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(3000):
        hay = "".join(rng.choice("ab") for _ in range(rng.randint(1, 30)))
        ndl = "".join(rng.choice("ab") for _ in range(rng.randint(1, 6)))
        want = hay.find(ndl)
        for label, fn in versions.items():
            assert fn(hay, ndl) == want, f"{label} vs str.find on {hay!r}, {ndl!r}"
    print("3000 random pairs: all versions match Python's str.find")

    # Worst case at the largest allowed size: every window almost matches.
    hay = "a" * 9_999 + "b"
    ndl = "a" * 4_999 + "b"
    for label, fn in versions.items():
        t = time.perf_counter()
        got = fn(hay, ndl)
        ms = (time.perf_counter() - t) * 1000
        assert got == 5_000, (label, got)
        print(f"  worst case, {label:<12} {ms:8.1f} ms")

    # Note 2: measure the extra memory of the slice.
    def peak(fn, *args):
        tracemalloc.start()
        fn(*args)
        p = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        return p
    hay, ndl = "a" * 10_000, "a" * 4_999 + "b"          # never matches
    with_slice = peak(Solution().strStr, hay, ndl)
    no_slice = peak(str_str_no_slice, hay, ndl)
    assert with_slice >= 4_999 > no_slice, (with_slice, no_slice)
    print(f"note 2 confirmed: the slice version peaked at {with_slice / 1000:.1f} KB "
          f"(one {len(ndl)}-character window), the no-slice version at {no_slice / 1000:.1f} KB")

    # Note 1: needle longer than haystack -> the range is empty.
    assert list(range(len("a") - len("aaa") + 1)) == []
    print("note 1 confirmed: a longer needle gives an empty range, so -1")

    # Note 4: find vs index on a miss.
    assert "abc".find("z") == -1
    try:
        "abc".index("z")
        raise AssertionError("expected ValueError")
    except ValueError:
        print("note 4 confirmed: find returns -1 on a miss, index raises ValueError")
