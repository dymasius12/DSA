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

You need fluency with these six things. Not familiarity — fluency.

### `list` — the workhorse
```python
a = [3, 1, 2]
a.append(4)        # O(1)   add to end
a.pop()            # O(1)   remove from end
a.pop(0)           # O(n)   remove from front — AVOID, use deque
a.sort()           # O(n log n) in place
b = sorted(a)      # O(n log n) new list
a[::-1]            # reversed copy
a[1:3]             # slice — O(k), it COPIES
len(a)             # O(1)
```

### `dict` — the single most useful structure in interviews
```python
d = {}
d['x'] = 1         # O(1) average
d.get('y', 0)      # O(1), no KeyError — returns 0 if missing
'x' in d           # O(1)
for k, v in d.items(): ...
```

### `set` — membership in O(1)
```python
s = set()
s.add(3); 3 in s; s.remove(3)
set(a) & set(b)    # intersection
```
Use a set the moment you catch yourself writing `if x in some_list`.
That list check is O(n); the set check is O(1).

### `collections` — the three you'll actually use
```python
from collections import Counter, defaultdict, deque

Counter("aabc")            # {'a': 2, 'b': 1, 'c': 1}  — frequency in one line
Counter(a) == Counter(b)   # "are these anagrams?" in one line

d = defaultdict(list)      # missing key auto-creates []
d['k'].append(1)           # no KeyError

q = deque([1, 2, 3])
q.append(4); q.popleft()   # BOTH O(1) — this is your BFS queue
```

### `heapq` — a min-heap (Module 09)
```python
import heapq
h = []
heapq.heappush(h, 5)   # O(log n)
heapq.heappop(h)       # O(log n), returns SMALLEST
h[0]                   # peek smallest, O(1)
heapq.heappush(h, -x)  # negate to fake a MAX-heap
```

### Idioms that save you time under pressure
```python
for i, x in enumerate(a):        ...   # index AND value
for x, y in zip(a, b):           ...   # walk two lists together
res = [x*2 for x in a if x > 0]        # comprehension
INF = float('inf')                     # a value bigger than everything
a, b = b, a                            # swap, no temp variable
'-'.join(['a','b'])                    # 'a-b'
d.setdefault(k, []).append(v)          # defaultdict without importing
```

### Gotchas that will bite you
```python
grid = [[0]*3]*3       # WRONG — three references to the SAME row
grid = [[0]*3 for _ in range(3)]   # right

def f(acc=[]):         # WRONG — default list is shared across calls
def f(acc=None):       # right; then `acc = acc or []`

-7 // 2   # -4, not -3. Python floors toward negative infinity.
int(-7/2) # -3, truncates toward zero.
```

---

## What to do now

Open `problems/00_foundations/` and fill in the four warm-ups. They exist to
make sure the toolkit above is in your fingers, not just on the page.

Run: `./check 00`
