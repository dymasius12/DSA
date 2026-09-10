# The Pattern Map

The most important file in this repo, and the one most likely to be useful on
its own. Every interview pattern, what triggers it, and a working template.

LeetCode isn't three thousand problems — it's about sixteen patterns wearing
three thousand costumes. Once you can name the pattern within a minute of
reading a problem, the coding part is mechanical. That recognition is the whole
skill, and this page is it compressed.

Read the table as: *when a problem says this → reach for that.*

---

## Short on time? These eight first

The highest-frequency set — they cover a large share of real interview
questions, and each has a template below:

`Sliding Window` · `Subsets/Backtracking` · `Modified Binary Search` ·
`Top K (heap)` · `Tree DFS` · `Tree BFS` · `Topological Sort` · `Two Pointers`

Worth knowing what that set *leaves out*, though: **hashing** (module 01, which
is more common than any of them) and **dynamic programming** (13–14, which is
where interviews get hard). The eight are the fastest way to become competent.
They are not the whole job.

---

## Trigger → Pattern

| The problem says... | Reach for | Module |
|---|---|---|
| "have I seen this before?", "count of", "does X exist" | **hash map / set** | 01 |
| input is **sorted**, find a pair/triplet | **two pointers** | 02 |
| "longest/shortest **contiguous** subarray or substring" | **sliding window** | 03 |
| "matching", "nearest previous greater", "valid parentheses" | **stack** | 04 |
| "level order", "depth of", "shortest path" in a tree | **BFS with a queue** | 07 |
| sorted input, or "minimize the maximum" | **binary search** | 05 |
| "middle of list", "does it cycle", "reverse the list" | **fast/slow pointers** | 06 |
| anything with a tree | **DFS recursion**, or BFS for levels | 07 |
| prefix matching, autocomplete, word lists | **trie** | 08 |
| "top K", "K largest/smallest", "median as it streams" | **heap** | 09 |
| "all combinations/permutations/subsets", n ≤ 20 | **backtracking** | 10 |
| grid, islands, "connected", "shortest steps" | **BFS/DFS** | 11 |
| weighted shortest path / dependency order / grouping | **Dijkstra / topo sort / union-find** | 12 |
| "how many ways", "min/max cost to reach" | **DP** | 13–14 |
| "can I take the best option each step?" | **greedy** (prove it!) | 15 |
| list of `[start, end]` | **sort by start, then sweep** | 16 |
| "without extra space", "single number", powers of 2 | **bit manipulation** | 17 |

---

## Templates

### Sliding window (variable size)
```python
left = 0
window = {}                       # or a running sum / counter
best = 0
for right, ch in enumerate(s):
    window[ch] = window.get(ch, 0) + 1
    while <window is invalid>:    # shrink from the left until valid again
        window[s[left]] -= 1
        if window[s[left]] == 0:
            del window[s[left]]
        left += 1
    best = max(best, right - left + 1)
return best
```

### Two pointers (sorted array)
```python
l, r = 0, len(a) - 1
while l < r:
    cur = a[l] + a[r]
    if cur == target: return [l, r]
    elif cur < target: l += 1     # need bigger
    else: r -= 1                  # need smaller
```

### Binary search
```python
lo, hi = 0, len(a) - 1
while lo <= hi:                   # <= , and hi is INCLUSIVE
    mid = (lo + hi) // 2
    if a[mid] == target: return mid
    elif a[mid] < target: lo = mid + 1
    else: hi = mid - 1
return -1
```
### Modified binary search (rotated sorted array)
```python
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid
    if nums[lo] <= nums[mid]:                 # LEFT half is sorted
        if nums[lo] <= target < nums[mid]: hi = mid - 1
        else:                              lo = mid + 1
    else:                                     # RIGHT half is sorted
        if nums[mid] < target <= nums[hi]: lo = mid + 1
        else:                              hi = mid - 1
return -1
```
The insight: after a rotation **at least one half is still sorted**. Work out
which, then ask whether the target lies inside that sorted half. If yes, go
there; if no, go the other way.

### Binary search on the answer
When the ask is "minimize the maximum" or "find the smallest X that works",
binary search the **answer range**, not the array. Write a `feasible()` helper.
```python
def feasible(x) -> bool: ...          # can we do it with x?

lo, hi = <smallest possible>, <largest possible>
while lo < hi:                        # note: <  and hi = mid (not mid - 1)
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid        # works — try smaller
    else:             lo = mid + 1    # doesn't — must go bigger
return lo
```

### BFS (shortest path in an unweighted graph / grid)
```python
from collections import deque
q = deque([start])
seen = {start}
steps = 0
while q:
    for _ in range(len(q)):       # this inner loop = ONE level
        node = q.popleft()
        if node == goal: return steps
        for nxt in neighbors(node):
            if nxt not in seen:
                seen.add(nxt)     # mark on ENQUEUE, not on dequeue
                q.append(nxt)
    steps += 1
return -1
```

### DFS on a grid
```python
def dfs(r, c):
    if r < 0 or c < 0 or r >= rows or c >= cols: return
    if grid[r][c] != '1': return          # wall, or already visited
    grid[r][c] = '0'                      # mark visited
    for dr, dc in ((1,0), (-1,0), (0,1), (0,-1)):
        dfs(r + dr, c + dc)
```

### Top K elements (heap of size k)
```python
import heapq
h = []
for n in nums:
    heapq.heappush(h, n)
    if len(h) > k:
        heapq.heappop(h)       # evict the smallest -> h keeps the k LARGEST
return h
```
Counter-intuitive but the point: for the k **largest**, use a **min**-heap of
size k, so the weakest survivor is always the one on top and cheapest to evict.
Flip it (or negate) for the k smallest. O(n log k), better than sorting when
k << n.

```python
# Weighted by something else? Push a tuple — it sorts by the first element.
heapq.heappush(h, (freq, value))

# And if you don't need to stream it:
heapq.nlargest(k, nums)                   # done, no heap management
```

### Backtracking
```python
def backtrack(start, path):
    if <path is a complete answer>:
        res.append(path[:])       # COPY — path keeps mutating
        return
    for i in range(start, len(nums)):
        path.append(nums[i])      # choose
        backtrack(i + 1, path)    # explore
        path.pop()                # UNDO — this is the whole pattern
```

### Tree DFS
```python
def dfs(node):
    if not node: return <base case>
    left = dfs(node.left)
    right = dfs(node.right)
    return <combine left, right, node.val>
```

### Tree BFS (level order)
```python
from collections import deque
if not root: return []
res, q = [], deque([root])
while q:
    level = []
    for _ in range(len(q)):        # snapshot the size FIRST — that's the level
        node = q.popleft()
        level.append(node.val)
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    res.append(level)
return res
```
`for _ in range(len(q))` is the whole trick: capture the length *before* the
loop, so you process exactly one level even as you append the next one.
Reach for BFS over DFS whenever the question mentions **levels, depth, or the
shortest path**.

### Topological sort (Kahn's algorithm)
```python
from collections import deque, defaultdict
adj = defaultdict(list)
indeg = [0] * n
for node, dependency in edges:        # dependency must come BEFORE node
    adj[dependency].append(node)
    indeg[node] += 1

q = deque([i for i in range(n) if indeg[i] == 0])   # nothing blocks these
order = []
while q:
    node = q.popleft()
    order.append(node)
    for nxt in adj[node]:
        indeg[nxt] -= 1               # one prerequisite satisfied
        if indeg[nxt] == 0:           # all satisfied -> now available
            q.append(nxt)
return order if len(order) == n else []   # short == there was a CYCLE
```
Repeatedly take whatever has no unmet prerequisites. **The length check at the
end is the cycle detection** — if you couldn't place every node, something was
circular. Course schedules, build order, task dependencies.

### DP (1-D, bottom-up)
```python
dp = [0] * (n + 1)
dp[0] = <base case>
for i in range(1, n + 1):
    dp[i] = <recurrence over dp[i-1], dp[i-2], ...>
return dp[n]
```
*Top-down alternative:* write the recursion, then add `@lru_cache(None)`.
Do that first if the recurrence is hard to see.

---

## The 4 questions, every single problem

Ask these before typing. They collapse most problems in under a minute.

1. **What am I actually being asked to return?** (a count, an index, the thing itself)
2. **What does `n` max out at?** → tells you the required complexity → tells you the pattern
3. **Is the input sorted?** (or can I sort it for O(n log n)?)
4. **What's the brute force, and what specific work is it repeating?**
   Every optimization is "stop repeating *that*."
