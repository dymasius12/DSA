# DSA — Coding Interview Track

Python 3 · pattern-based · built to be **come-back-able**.

> **Been away a while? → [START_HERE.md](START_HERE.md).** Don't scroll this
> roadmap and feel behind. That file has a 90-minute path back to functional.

## The core idea

LeetCode is not 3000 problems. It is roughly **16 patterns**. Once you can
recognize which pattern a problem belongs to within 60 seconds, the coding part
is mechanical. This repo is organized by pattern, not by difficulty.

Your job in each module:
1. Read `notes/NN_topic.md` — the pattern, when it applies, the template.
2. Fill in the stubs in `problems/NN_topic/`.
3. Run `./check NN` until green.
4. Only then read `solutions/NN_topic/` and compare.
5. Log it in `PROGRESS.md`.

## The four commands

```bash
./check              # run every test
./check 01           # run just module 01
./check 01 two_sum   # run one problem

./review             # what has decayed? what should I do today?
./log "what I did" 45   # record a session (do this even for 15 minutes)
```

`./review` is the one that keeps this repo alive. When you come back after a
gap, it tells you where to start so you don't have to decide.

## Layout

| Path | What it's for | When you read it |
|------|---------------|------------------|
| `START_HERE.md` | the re-entry ramp | after any gap |
| `cheatsheets/_patterns.md` | **every pattern, trigger + template** | reloading, or pre-interview |
| `cheatsheets/NN_*.md` | one module, compressed to a screen | reloading |
| `notes/NN_*.md` | the full explanation | learning it the first time |
| `problems/mNN_*/` | stubs you fill in | doing the reps |
| `solutions/mNN_*/` | annotated references | **after** you've tried |
| `PROGRESS.md` | status, confidence, session log | every session |

## Roadmap

| # | Module | Pattern in one line | Problems |
|---|--------|---------------------|----------|
| 00 | Foundations | Big-O and the Python toolkit you need | 4 |
| 01 | Arrays & Hashing | Trade memory for time with a dict/set | 8 |
| 02 | Two Pointers | Two indices walking a sorted array | 6 |
| 03 | Sliding Window | A contiguous range that grows and shrinks | 7 |
| 04 | Stack | Last-in-first-out; "match the previous thing" | 6 |
| 05 | Binary Search | Halve the search space each step | 7 |
| 06 | Linked List | Pointer surgery; fast/slow pointers | 8 |
| 07 | Trees | Recursion on two children | 12 |
| 08 | Tries | A tree keyed by characters | 3 |
| 09 | Heap / Priority Queue | Always pull the smallest/largest next | 6 |
| 10 | Backtracking | Try, recurse, undo | 8 |
| 11 | Graphs | Grids and adjacency lists; BFS/DFS | 10 |
| 12 | Advanced Graphs | Dijkstra, topological sort, union-find | 6 |
| 13 | 1-D DP | Cache the answer to a smaller version | 10 |
| 14 | 2-D DP | Cache over a grid of subproblems | 8 |
| 15 | Greedy | Take the locally best choice, prove it works | 6 |
| 16 | Intervals | Sort by start, then merge/count | 5 |
| 17 | Bit Manipulation | XOR, masks, and counting bits | 5 |

## Pacing (no deadline = do it right)

- **1 module per week.** Read notes Monday, grind problems Tue–Fri.
- **Saturday is review day**: redo 3 problems from *previous* modules from
  scratch, no notes. This is the part everyone skips and it is the part that
  actually makes it stick.
- Never spend more than **25 minutes stuck** on a problem. Read the solution,
  understand it, close it, then rewrite it from memory the next day.

## Rules that matter

1. **Type the solution, never paste it.** Muscle memory is real.
2. **Say the complexity out loud** before you write code. Time and space.
3. **A solution you read is not a solution you know.** Re-solve it 2 days later.
4. If you can't explain the approach in two sentences, you don't understand it yet.
