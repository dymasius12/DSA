"""Module 00 reference solutions. Read these AFTER you've tried."""
from collections import Counter, defaultdict


def char_frequency(s: str) -> dict:
    # The manual version — this is what Counter does for you.
    #   freq = {}
    #   for c in s:
    #       freq[c] = freq.get(c, 0) + 1
    #   return freq
    # O(n) time, O(k) space.
    return dict(Counter(s))


def has_duplicate(nums: list) -> bool:
    # A set of everything seen so far. The moment we see a repeat, stop.
    # Early-exit matters: on [1,1,...huge...] this returns after 2 steps.
    # The one-liner `return len(set(nums)) != len(nums)` also works but always
    # scans the whole list.
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False


def group_by_first_letter(words: list) -> dict:
    # defaultdict(list) means d[key] auto-creates [] on first touch.
    groups = defaultdict(list)
    for w in words:
        groups[w[0]].append(w)
    return dict(groups)


def make_grid(rows: int, cols: int, fill: int = 0) -> list:
    # Each iteration builds a FRESH [fill]*cols list.
    # [[fill]*cols]*rows would alias one row `rows` times.
    return [[fill] * cols for _ in range(rows)]
