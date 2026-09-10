"""Module 01 reference solutions. Read AFTER you've genuinely tried."""
from collections import Counter, defaultdict


def contains_duplicate(nums: list) -> bool:
    # Early-exit beats `len(set(nums)) != len(nums)` on inputs that repeat early.
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False


def is_anagram(s: str, t: str) -> bool:
    # Length check is a free O(1) rejection.
    # Counter equality compares the two frequency maps. O(n) time.
    # O(1) space: at most 26 keys regardless of how long the strings are.
    if len(s) != len(t):
        return False
    return Counter(s) == Counter(t)


def two_sum(nums: list, target: int) -> list:
    # seen: value -> the index we saw it at.
    # We ask "did I already pass the number that completes this pair?"
    # Checking before inserting is what stops an element pairing with itself.
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []


def group_anagrams(strs: list) -> list:
    # sorted("eat") and sorted("tea") both give ['a','e','t'].
    # A list isn't hashable, so tuple() it to use as a key.
    # O(n * k log k) because we sort each of the n words of length k.
    #
    # The O(n * k) alternative avoids sorting entirely: key on a 26-length
    # tuple of letter counts.
    #     key = [0] * 26
    #     for c in w: key[ord(c) - ord('a')] += 1
    #     groups[tuple(key)].append(w)
    groups = defaultdict(list)
    for w in strs:
        groups[tuple(sorted(w))].append(w)
    return list(groups.values())


def top_k_frequent(nums: list, k: int) -> list:
    # Bucket sort. A frequency can never exceed len(nums), so index buckets
    # BY frequency. Then walk from the highest bucket down.
    # O(n) — no sorting, no heap.
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)

    res = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            res.append(value)
            if len(res) == k:
                return res
    return res


def product_except_self(nums: list) -> list:
    # Two passes, no division.
    n = len(nums)
    res = [1] * n

    # Pass 1: res[i] = product of everything strictly LEFT of i.
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]

    # Pass 2: fold in the product of everything strictly RIGHT of i.
    # `suffix` is a single variable — that's how we stay at O(1) extra space.
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]

    return res


def longest_consecutive(nums: list) -> int:
    # The guard `n - 1 not in num_set` is the entire problem.
    # It means each run is walked exactly once across the whole loop,
    # so the total work is O(n) even though there's a nested while.
    num_set = set(nums)
    best = 0
    for n in num_set:
        if n - 1 in num_set:
            continue          # not the start of a run — skip it
        length = 1
        while n + length in num_set:
            length += 1
        best = max(best, length)
    return best


def is_valid_sudoku(board: list) -> bool:
    # Three independent "have I seen this digit here" checks.
    # (r // 3, c // 3) maps a cell to one of the nine 3x3 boxes.
    rows = defaultdict(set)
    cols = defaultdict(set)
    boxes = defaultdict(set)

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue
            box = (r // 3, c // 3)
            if val in rows[r] or val in cols[c] or val in boxes[box]:
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[box].add(val)
    return True
