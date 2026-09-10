# 01 — Arrays & Hashing · reload sheet

**The one idea:** spend O(n) memory to kill an O(n²) scan.
**The one question:** *what am I looking up, and what's the key?*

## The four shapes
```python
seen = set()                      # 1. membership: "have I seen this?"
count = Counter(nums)             # 2. frequency:  "how many of each?"
seen = {}; seen[val] = i          # 3. locate:     "where did I see it?"
groups = defaultdict(list)        # 4. group:      "what belongs together?"
groups[computed_key].append(x)
```
Stuck? Walk all four. One fits ~90% of the time.

## Keys must be hashable
`str` `int` `tuple` `frozenset` ✅ · `list` `dict` `set` ❌
Need to key on a collection → `tuple(sorted(x))`.

## Snippets worth remembering
```python
# two_sum: check BEFORE inserting, or [3,3] matches itself
if target - n in seen: return [seen[target - n], i]
seen[n] = i

# anagram key
tuple(sorted(word))

# top-k without sorting: bucket by frequency, walk from the top
buckets = [[] for _ in range(len(nums) + 1)]
for val, freq in Counter(nums).items(): buckets[freq].append(val)

# prefix/suffix: two passes replace a nested loop
prefix = 1
for i in range(n): res[i] = prefix; prefix *= nums[i]
suffix = 1
for i in range(n-1, -1, -1): res[i] *= suffix; suffix *= nums[i]

# longest run: ONLY start from a run's first element
if n - 1 in num_set: continue     # <- without this it's O(n^2)

# 3x3 box index
box = (r // 3, c // 3)
```

## Complexities to say out loud
| | time | space |
|---|---|---|
| contains_duplicate | O(n) | O(n) |
| is_anagram | O(n) | **O(1)** — 26 letters, doesn't grow with n |
| two_sum | O(n) | O(n) |
| group_anagrams | O(n·k log k) | O(n·k) |
| top_k_frequent | O(n) bucket sort | O(n) |
| product_except_self | O(n) | **O(1)** extra — output doesn't count |
| longest_consecutive | O(n) | O(n) |
| is_valid_sudoku | O(1) — fixed 9×9 | O(1) |

## If you only remember one thing
`x in a_list` is O(n). `x in a_set` is O(1).
That single swap is the whole module.
