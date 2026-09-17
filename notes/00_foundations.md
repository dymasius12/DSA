# 00 — Foundations

Two things to install in your head before any problem: **how to count cost**,
and **which Python tool does what**.

---

## Part 1: Big-O, honestly

Big-O answers one question: *as the input grows, how does the work grow?*
We throw away constants and small terms, because at scale they don't matter.

`3n + 50` → **O(n)**. `n²/2` → **O(n²)**.

### The ladder (memorize this order)

| Notation | Name | n = 1,000,000 feels like | Typical source |
|----------|------|--------------------------|----------------|
| O(1) | constant | instant | dict lookup, arithmetic |
| O(log n) | logarithmic | instant | binary search, balanced tree |
| O(n) | linear | fast | one loop over the input |
| O(n log n) | linearithmic | fine | **sorting**, heap of n items |
| O(n²) | quadratic | too slow | nested loop over the input |
| O(2ⁿ) | exponential | hopeless past n≈25 | subsets, naive recursion |
| O(n!) | factorial | hopeless past n≈10 | permutations |

### Reading the constraints tells you the answer

Interviewers and LeetCode give you `n`'s max. That's a hint, not decoration:

| If n is up to... | You need at most | So probably |
|------------------|------------------|-------------|
| 10 | O(n!) | permutations / brute force |
| 20–25 | O(2ⁿ) | subsets, bitmask DP |
| 500 | O(n³) | 3 nested loops, some DP |
| 5,000 | O(n²) | nested loop, 2-D DP |
| 100,000 | O(n log n) | **sort it**, or heap |
| 1,000,000+ | O(n) or O(log n) | hash map, two pointers, binary search |

> Rule of thumb: a modern machine does ~10⁸ simple operations per second.
> If your `n` is 10⁵ and your idea is O(n²), that's 10¹⁰ ops. It will time out.
> **Know this before you start typing.**

### Space complexity

Same idea, for memory. The output usually doesn't count; the extra structures
you allocate do. A dict holding n keys is O(n) space. Recursion of depth n is
O(n) space too — the call stack is memory.

### The trade you'll make constantly

Almost every "clever" solution in Module 01 is the same move: **spend O(n)
memory to turn an O(n²) scan into an O(n) one.** Remember that sentence.

---

## Part 2: The Python toolkit

The four warm-ups in `problems/m00_foundations/` need only what's below. The
rest of the toolkit lives in the cheatsheets, so each thing is explained once:

| You need | It's in |
|---|---|
| sorting with `key=`, comprehensions, `deque`, `heapq`, `bisect`, `lru_cache` | [`cheatsheets/_python.md`](../cheatsheets/_python.md) |
| `len()`, type conversions, string and list methods, `sort` vs `sorted` | [`cheatsheets/_easily_forgotten.md`](../cheatsheets/_easily_forgotten.md) |
| what each operation costs | [`cheatsheets/00_complexity.md`](../cheatsheets/00_complexity.md) |

### `dict` and `set`: lookups in O(1)
```python
d = {}
d['x'] = 1         # O(1) on average
d.get('y', 0)      # no KeyError: returns 0 if 'y' is missing
'x' in d           # O(1)

s = set()
s.add(3)
3 in s             # O(1)
```
Use a set the moment you catch yourself writing `if x in some_list`. That list
check is O(n); the set check is O(1).

### `Counter` and `defaultdict`
```python
from collections import Counter, defaultdict

Counter("aabc")            # {'a': 2, 'b': 1, 'c': 1}: frequencies in one line
Counter(a) == Counter(b)   # "are these anagrams?" in one line

d = defaultdict(list)      # a missing key starts as []
d['k'].append(1)           # so this never raises KeyError
```

### The trap the last warm-up tests
```python
grid = [[0] * 3] * 3               # WRONG: three references to the SAME row
grid = [[0] * 3 for _ in range(3)] # right: a new row each time
```
With the wrong version, `grid[0][0] = 5` changes every row.

---

## What to do now

Open `problems/m00_foundations/warmups.py` and fill in the four warm-ups. They exist to
make sure the toolkit above is in your fingers, not just on the page.

Run: `./check 00`
