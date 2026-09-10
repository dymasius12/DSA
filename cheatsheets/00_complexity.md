# Complexity — 2-minute reload

Everything about Big-O that actually comes up in an interview, and nothing that
doesn't. Companion to [`notes/00_foundations.md`](../notes/00_foundations.md),
which explains the *why*.

## The ladder
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)

## Constraints tell you the answer
| n up to | max complexity | probably |
|---|---|---|
| 10 | O(n!) | permutations |
| 20 | O(2ⁿ) | subsets / bitmask |
| 500 | O(n³) | triple loop, DP |
| 5,000 | O(n²) | nested loop, 2-D DP |
| 100,000 | O(n log n) | **sort**, heap |
| 1,000,000+ | O(n) | hash map, two pointers |

~10⁸ operations per second. n=10⁵ with an O(n²) idea = 10¹⁰ ops = timeout.

## Python costs people get wrong
| Operation | Cost |
|---|---|
| `list.pop(0)` | **O(n)** — use `deque.popleft()`, O(1) |
| `x in list` | **O(n)** — use a set, O(1) |
| `a[1:5]` slice | O(k), it **copies** |
| `list.insert(0, x)` | O(n) |
| `dict[k]`, `set.add` | O(1) average |
| `heappush/heappop` | O(log n) |
| `sorted()` | O(n log n), O(n) space |
| string `+=` in a loop | O(n²) — build a list, `''.join()` at the end |

## Space
Recursion depth n = O(n) space. The call stack is memory.
Output usually doesn't count toward space complexity.

## The trade
> Spend O(n) memory to turn an O(n²) scan into O(n).
> That one sentence is most of Module 01.
