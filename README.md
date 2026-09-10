# DSA

My working repo for data structures, algorithms, and coding interviews. Python 3.

It's public because there's no reason for it not to be — if any of it is useful
to you, help yourself. But it's built for one person, and that shapes every
decision in here.

---

## The problem this repo exists to solve

I've learned this material before. More than once.

Then life gets busy, I stop for a few months, and when I come back it's gone —
not entirely, but enough that opening LeetCode feels like starting from zero.
And *that feeling* is the real problem, because it's what makes me not open it
at all. The knowledge decaying is annoying. Dreading the restart is what
actually costs me the years.

So this repo isn't a course, and it isn't a solutions dump. It's a **place to
come back to**. Everything here is designed around one question:

> When I return after six months away, what gets me productive in an hour
> instead of a month?

---

## How it's designed

The reason DSA knowledge evaporates is that most people store it as **thousands
of loose problems**. Loose facts decay fast. Patterns compress, and compressed
things reload fast.

So there are only ~16 patterns in here, and every module produces three
artifacts on purpose:

| Artifact | What it is | How fast it decays |
|----------|-----------|--------------------|
| `problems/` | stubs I fill in — the reps that build intuition | **fast** |
| `notes/` | the full explanation, for learning it the first time | slowly |
| `cheatsheets/` | the pattern compressed to one screen | **barely** |

When I come back, I reload from the cheatsheet — the smallest, most durable
artifact — and the rest decompresses behind it. That's the entire idea.

The other half is not having to decide where to start. `./review` scores every
topic by decay (how long since I touched it × how shaky I was) and just tells
me. Removing that decision is most of the battle.

---

## Layout

| Path | What it's for | When I read it |
|------|---------------|----------------|
| [`START_HERE.md`](START_HERE.md) | the re-entry ramp | after any gap |
| [`cheatsheets/_patterns.md`](cheatsheets/_patterns.md) | **every pattern: trigger + template** | reloading, or before an interview |
| `cheatsheets/NN_*.md` | one module, compressed to a screen | reloading |
| `notes/NN_*.md` | the full explanation | learning it the first time |
| `problems/mNN_*/` | stubs to fill in | doing the reps |
| `solutions/mNN_*/` | annotated references | **after** I've actually tried |
| [`PROGRESS.md`](PROGRESS.md) | status, confidence, session log | every session |

---

## The four commands

```bash
./check                 # run every test
./check 01              # run just module 01
./check 01 two_sum      # run one problem

./review                # what's decayed? what should I do today?
./log "what I did" 45   # record a session — even a 15-minute one
```

Tests are `pytest`. Every problem is a stub with a docstring spec; the tests
fail until it's implemented, including performance tests that reject an
O(n²) solution where O(n) was the point.

```bash
git clone https://github.com/dymasius12/DSA.git
cd DSA
pip install pytest
./review
```

---

## Roadmap

| # | Module | The pattern, in one line | Problems | Status |
|---|--------|--------------------------|----------|--------|
| 00 | Foundations | Big-O, and the Python toolkit you need | 4 | ✅ built |
| 01 | Arrays & Hashing | Trade memory for time with a dict or set | 8 | ✅ built |
| 02 | Two Pointers | Two indices walking a sorted array | 6 | planned |
| 03 | Sliding Window | A contiguous range that grows and shrinks | 7 | planned |
| 04 | Stack | Last in, first out — "match the previous thing" | 6 | planned |
| 05 | Binary Search | Halve the search space every step | 7 | planned |
| 06 | Linked List | Pointer surgery; fast and slow pointers | 8 | planned |
| 07 | Trees | Recursion on two children | 12 | planned |
| 08 | Tries | A tree keyed by characters | 3 | planned |
| 09 | Heap / Priority Queue | Always pull the smallest or largest next | 6 | planned |
| 10 | Backtracking | Try, recurse, undo | 8 | planned |
| 11 | Graphs | Grids and adjacency lists; BFS and DFS | 10 | planned |
| 12 | Advanced Graphs | Dijkstra, topological sort, union-find | 6 | planned |
| 13 | 1-D DP | Cache the answer to a smaller version | 10 | planned |
| 14 | 2-D DP | Cache over a grid of subproblems | 8 | planned |
| 15 | Greedy | Take the locally best choice — and prove it works | 6 | planned |
| 16 | Intervals | Sort by start, then merge or count | 5 | planned |
| 17 | Bit Manipulation | XOR, masks, and counting bits | 5 | planned |

Modules get built as I reach them, deliberately. A wall of 300 unfinished stubs
is exactly the thing that makes coming back feel heavy.

---

## How I work through a module

1. Read `notes/NN_*.md` — the pattern, when it applies, the template.
2. Fill in the stubs in `problems/mNN_*/`.
3. `./check NN` until it's green.
4. *Then* read `solutions/mNN_*/` and compare approaches.
5. Write the cheatsheet **in my own words**, then log it in `PROGRESS.md`.

### Pacing

One module a week. Notes on Monday, problems Tuesday through Friday.

**Saturday is review day**: re-solve three problems from *earlier* modules from
a blank file, no notes. This is the part everyone skips, and it's the part that
actually makes it stick.

### Rules I keep breaking and shouldn't

1. **Type the solution, never paste it.** Muscle memory is real.
2. **Say the complexity out loud before writing code.** Time and space.
3. **Never more than 25 minutes stuck.** Read the solution, understand it, close
   it, rewrite it from memory tomorrow. That's the method, not cheating.
4. **A solution I read is not a solution I know.** Re-solve it two days later.
5. If I can't explain the approach in two sentences, I don't understand it yet.

---

## If you're not me

You're welcome to any of it. A few honest notes:

- The **[pattern map](cheatsheets/_patterns.md)** is the part most likely to be
  useful to you standalone. It's a trigger → pattern table plus working
  templates for all 16 patterns, and it doesn't assume anything about the rest
  of the repo.
- The notes are written to teach, not to show off. If you're starting near zero,
  [`notes/00_foundations.md`](notes/00_foundations.md) assumes nothing.
- `PROGRESS.md` is my own tracker. Fork it and it becomes yours — but the
  confidence scores only work if you're honest, and honest is uncomfortable.
- Problem statements are paraphrased in the docstrings so the repo stands alone;
  the LC numbers are there if you want the original.

If something in here is wrong or badly explained, an issue is welcome.
