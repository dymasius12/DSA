# Python Shortcuts

The idioms worth having in muscle memory for interviews. Organized by *what you
want to do*, because that's how you'll search for them under pressure.

Nothing clever for its own sake — every line here is something an interviewer
would read as fluent, not as a trick.

> Verified on Python 3.9. Anything newer is flagged.

---

## Sorting — where most of the wins are

```python
sorted(a)                          # new list;  a.sort() sorts in place
sorted(a, reverse=True)            # descending
sorted(words, key=len)             # by length
sorted(words, key=str.lower)       # case-insensitive
sorted(pairs, key=lambda p: p[1])  # by second element

# Multiple keys: tuple. Earlier elements win ties.
sorted(people, key=lambda p: (p.age, p.name))

# Mixed directions: negate the numeric one.
sorted(items, key=lambda x: (-x.score, x.name))   # score DESC, name ASC

# Sort a dict by value
sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
```

**The rule to remember:** `key=` describes *what to compare*, and a **tuple key
sorts by each field in order**. That one sentence covers ~90% of sorting
questions. Python's sort is stable, so equal elements keep their original order.

---

## min / max — the underused `key`

```python
max(nums)
max(words, key=len)                # longest word
min(points, key=lambda p: p[0]**2 + p[1]**2)   # closest to origin
max(counts, key=counts.get)        # dict key with the largest value
max(nums, default=0)               # no crash on an empty list
```

`min`/`max` take the same `key=` as `sorted`. If you're writing a loop with a
`best = float('-inf')` accumulator, check whether `max(..., key=...)` does it.

---

## Comprehensions

```python
[x * 2 for x in nums]                      # map
[x for x in nums if x > 0]                 # filter
[x * 2 for x in nums if x > 0]             # both
{x: x**2 for x in nums}                    # dict
{x for x in nums}                          # set
[c for word in words for c in word]        # flatten (loops in for-order)
[[0] * cols for _ in range(rows)]          # 2-D grid  ← never [[0]*c]*r
```

Read a nested one **left to right, like nested for-loops** — that's the whole
mental model. `x if cond else y` goes *before* the `for`; a plain filter goes
*after*.

```python
[x if x > 0 else 0 for x in nums]          # ternary: BEFORE the for
[x for x in nums if x > 0]                 # filter: AFTER the for
```

---

## Unpacking

```python
a, b = b, a                    # swap, no temp
first, *rest = [1, 2, 3, 4]    # first=1,  rest=[2,3,4]
*init, last = [1, 2, 3, 4]     # init=[1,2,3],  last=4
a, (b, c) = 1, (2, 3)          # nested

for i, x in enumerate(nums): ...          # index + value
for i, x in enumerate(nums, 1): ...       # 1-indexed
for x, y in zip(a, b): ...                # two lists in lockstep
for x, y, z in zip(a, b, c): ...          # any number

dict(zip(keys, values))        # two lists -> dict
rows = list(zip(*grid))        # TRANSPOSE a 2-D list
```

`zip(*grid)` transposing a matrix is worth memorizing — it shows up constantly
in grid problems (rotate, check columns, diagonals).

---

## Strings

```python
s[::-1]                        # reverse
''.join(chars)                 # list of chars -> string  (NEVER += in a loop)
s.split()                      # on any whitespace, drops empties
s.split(',')                   # on a specific character
'-'.join(['a', 'b'])           # 'a-b'

s.strip() / .lstrip() / .rstrip()
s.lower() / .upper()
s.isalpha() / .isdigit() / .isalnum()      # useful for "valid palindrome"
s.count('a')
s.replace('a', 'b')
s.startswith('ab') / .endswith('ab')

ord('a')        # 97   char -> int
chr(97)         # 'a'  int -> char
ord(c) - ord('a')    # 'a'->0 ... 'z'->25   the alphabet-index trick
```

**Strings are immutable.** `s += c` in a loop is O(n²) because it rebuilds the
whole string each time. Build a `list`, then `''.join(...)` once.

---

## Counting & grouping

```python
from collections import Counter, defaultdict

Counter("aabc")                # Counter({'a': 2, 'b': 1, 'c': 1})
Counter(nums).most_common(2)   # [(val, count), ...] top 2
Counter(a) == Counter(b)       # anagram check, one line
Counter(a) - Counter(b)        # multiset difference (drops non-positives)

d = defaultdict(list);  d[k].append(v)     # no KeyError, no setup
d = defaultdict(int);   d[k] += 1          # counting without Counter
d = defaultdict(set);   d[k].add(v)

counts.get(k, 0)               # safe read with a default
counts[k] = counts.get(k, 0) + 1           # count without any import
d.setdefault(k, []).append(v)              # group without any import
```

`Counter` is a `dict`, so everything a dict does works on it.

---

## Truthiness — the quiet one that saves the most lines

```python
if not nums:        ...        # empty list/str/dict/set, 0, None -> falsy
if nums:            ...
x = val or default             # default when val is falsy
acc = acc or []                # the safe mutable-default fix

any(x > 0 for x in nums)       # "is there at least one..."
all(x > 0 for x in nums)       # "are they all..."
sum(1 for x in nums if x > 0)  # count matches without building a list
```

`any`/`all` **short-circuit** — they stop at the first decisive element, so
they're a real early exit, not just shorter code.

---

## Numbers

```python
float('inf'), float('-inf')    # bigger/smaller than everything
INF = float('inf')             # give it a name at the top

divmod(17, 5)                  # (3, 2)  quotient and remainder at once
17 // 5,  17 % 5               # 3, 2
abs(-3)
round(2.567, 2)
sum(nums) / len(nums)          # mean

10 ** 9 + 7                    # the usual modulus
1_000_000                      # underscores are legal in literals
```

**The negative-division trap:**
```python
-7 // 2      # -4  — floors toward NEGATIVE infinity
int(-7 / 2)  # -3  — truncates toward zero
-7 % 2       #  1  — Python's % is always non-negative for a positive divisor
```
This bites in binary search on negatives and in hashing. `-1 % n` giving `n-1`
is a *feature* — it makes circular-array indexing free.

---

## Iteration

```python
range(5)                       # 0..4
range(2, 10)                   # 2..9
range(10, 0, -1)               # 10 down to 1
range(len(a) - 1, -1, -1)      # last index down to 0  ← the backwards loop

reversed(a)                    # iterator, no copy
for x in reversed(a): ...
for i in reversed(range(n)): ...          # clearer than range(n-1,-1,-1)

for _ in range(k): ...         # repeat k times, index unused
zip(a, a[1:])                  # consecutive pairs — good for "is sorted"
```

```python
# "is this sorted?" in one line
all(a[i] <= a[i+1] for i in range(len(a) - 1))
all(x <= y for x, y in zip(a, a[1:]))     # same thing, no indices
```

---

## Slicing

```python
a[2:5]        # index 2,3,4
a[:3]         # first three
a[-3:]        # last three
a[::2]        # every other
a[::-1]       # reversed copy
a[:]          # shallow COPY — this is why backtracking does res.append(path[:])
```

Slices **copy**, so `a[1:]` inside a loop is O(n) each time. Fine for clarity,
a real cost in a hot loop.

---

## Structures worth reaching for

```python
from collections import deque
q = deque([1, 2, 3])
q.append(4); q.popleft()       # both O(1)  ← your BFS queue
q.appendleft(0); q.pop()
# list.pop(0) is O(n). This is the single most common accidental slowdown.

import heapq
h = []
heapq.heappush(h, 5)           # O(log n)
heapq.heappop(h)               # O(log n), returns the SMALLEST
h[0]                           # peek, O(1)
heapq.heapify(a)               # O(n), in place
heapq.nlargest(3, nums)        # top 3 without managing a heap
heapq.nsmallest(3, nums)
heapq.heappush(h, -x)          # negate to fake a MAX-heap
heapq.heappush(h, (priority, item))       # tuples sort by first element
```

```python
import bisect
bisect.bisect_left(a, x)       # leftmost index where x could be inserted
bisect.bisect_right(a, x)      # rightmost such index
bisect.insort(a, x)            # insert, keeping sorted
```
`bisect_left` on a sorted list is a correct binary search you don't have to
write. Know it — then still be able to write the loop by hand, because that's
often what's actually being asked.

---

## Sets

```python
a & b     # intersection      a | b     # union
a - b     # difference        a ^ b     # symmetric difference
a <= b    # is a a subset of b
set(list1) & set(list2)        # common elements, O(n)
```

---

## Memoization — free DP

```python
from functools import lru_cache

@lru_cache(None)               # None = unlimited cache
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)
```
Write the plain recursion first, confirm it's right, *then* add the decorator.
Exponential becomes linear on one line. Arguments must be hashable — so pass
tuples, not lists. (3.9+ also has `@cache`, the same thing without the `None`.)

---

## Worth knowing exists

```python
from itertools import permutations, combinations, product, accumulate

list(permutations([1,2,3]))        # all orderings
list(combinations([1,2,3], 2))     # all 2-picks, order-independent
list(product([0,1], repeat=3))     # cartesian product / binary strings
list(accumulate([1,2,3,4]))        # [1, 3, 6, 10]  running sum = prefix sums
```

Use them to **check your answer** while practising. In an interview,
`combinations` when asked to write backtracking is usually dodging the question
— but `accumulate` for prefix sums is fair game.

---

## The five that save the most typing

If you only keep five:

```python
1.  sorted(x, key=lambda i: (a, b))    # tuple key = multi-level sort
2.  Counter(x)                         # frequency map, free
3.  defaultdict(list)                  # grouping without KeyError checks
4.  ''.join(list_of_chars)             # never build strings with +=
5.  a[:]  /  [[0]*c for _ in range(r)] # copy, and a grid that isn't aliased
```

---

## Related

- [`_easily_forgotten.md`](_easily_forgotten.md): the plain basics (`len()`,
  `str()`, conversions) for when the blank is simpler than an idiom
- [`00_complexity.md`](00_complexity.md) — what each of these costs
- [`_patterns.md`](_patterns.md) — the algorithm templates that use them
- [`../notes/00_foundations.md`](../notes/00_foundations.md) — the longer
  explanation, with the gotchas spelled out

[← back to the repo](../README.md)
