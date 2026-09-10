# The Pattern Map

**The most important file in this repo.** If you only reload one thing, this.

Read it as: *when I see this in a problem → reach for this.*

---

## Trigger → Pattern

| The problem says... | Reach for | Module |
|---|---|---|
| "have I seen this before?", "count of", "does X exist" | **hash map / set** | 01 |
| input is **sorted**, find a pair/triplet | **two pointers** | 02 |
| "longest/shortest **contiguous** subarray or substring" | **sliding window** | 03 |
| "matching", "nearest previous greater", "valid parentheses" | **stack** | 04 |
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
*Binary search on the answer:* when asked to "minimize the maximum", binary
search over the **answer range**, and write a `feasible(x) -> bool` helper.

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
