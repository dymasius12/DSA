# 01 — Arrays & Hashing

## The one idea

> **Spend O(n) memory to avoid an O(n²) scan.**

Almost every problem in this module is the same move. You have a brute force
that, for each element, *searches the rest of the array* for something. That
search is the O(n) inner loop. A hash map makes that search O(1).

So the question you ask, every time, is:
**"What am I looking up, and what should the key be?"**

Get the key right and the problem is over. Most of the difficulty in this module
is choosing the key — not writing the loop.

---

## Why a dict is O(1)

A dict computes `hash(key)` — a number — and uses it to jump straight to a slot
in memory. No scanning. The cost doesn't grow with size. That's it. That's the
whole superpower, and it's why `x in some_set` beats `x in some_list` so badly
at scale.

Requirement: keys must be **hashable** (immutable). So:
- `str`, `int`, `tuple`, `frozenset` → valid keys ✅
- `list`, `dict`, `set` → **not** valid keys ❌

This matters more than it sounds. When you need to key on a group of things —
"all words that are anagrams of each other" — you must convert to something
hashable first, usually a `tuple` or a sorted `str`. That conversion *is* the
insight in `group_anagrams`.

---

## The four shapes

Nearly every hashing problem is one of these:

### 1. Set for membership — "have I seen this?"
```python
seen = set()
for x in nums:
    if x in seen: return True
    seen.add(x)
```
→ `contains_duplicate`, `longest_consecutive`

### 2. Counter for frequency — "how many of each?"
```python
from collections import Counter
count = Counter(nums)          # {value: how many times}
```
→ `valid_anagram`, `top_k_frequent`

### 3. Map value → index — "where did I see it?"
```python
seen = {}                      # value -> index
for i, x in enumerate(nums):
    if target - x in seen:     # look for the COMPLEMENT
        return [seen[target - x], i]
    seen[x] = i
```
→ `two_sum`. Note the order: check *before* inserting, or `[3,3]` breaks.

### 4. Map a computed key → group — "what belongs together?"
```python
from collections import defaultdict
groups = defaultdict(list)
for w in words:
    key = tuple(sorted(w))     # or a 26-length count tuple
    groups[key].append(w)
```
→ `group_anagrams`, `valid_sudoku`

**When you're stuck on a hashing problem, walk these four.** One of them fits
about 90% of the time.

---

## The prefix/suffix trick

`product_except_self` introduces a pattern you'll reuse for the rest of your
life (prefix sums, running maxima, range queries):

> For each index, you need something about *everything to the left* and
> *everything to the right*. Precompute both in two passes instead of
> recomputing per index.

Pass 1 left→right accumulating; pass 2 right→left accumulating. Two O(n) passes
replace an O(n²) nested loop. Whenever you see "for each i, look at all j < i",
reach for this.

---

## Complexity you should be able to state instantly

| Problem | Time | Space |
|---|---|---|
| contains_duplicate | O(n) | O(n) |
| valid_anagram | O(n) | O(1) — at most 26 keys |
| two_sum | O(n) | O(n) |
| group_anagrams | O(n · k log k) | O(n·k) — k = word length |
| top_k_frequent | O(n) with bucket sort | O(n) |
| product_except_self | O(n) | O(1) extra (output doesn't count) |
| longest_consecutive | O(n) | O(n) |
| valid_sudoku | O(1) — the board is always 9×9 | O(1) |

`valid_anagram` being O(1) space surprises people. The alphabet is fixed at 26,
so the dict never grows with n. Say that out loud in an interview; it's the kind
of detail that reads as *actually understanding it*.

---

## The trap in longest_consecutive

The naive fix is "sort it" — that's O(n log n) and the problem demands O(n).
The real trick: only start counting a run from a number that is the **start** of
its run, i.e. `n - 1 not in num_set`. Without that check, you re-walk the same
sequence from every member and it degrades to O(n²).

That check is the entire problem. Everything else is a while loop.

---

Now go do them: `./check 01`
