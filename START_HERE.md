# Start here

For coming back after a break, whether it's been two weeks or two years.

---

**You came back. That was the hard part.**

Don't scroll the roadmap and feel behind. Opening the repo, seeing everything
you haven't done, and closing the tab is the habit this page exists to break.
Pick the situation below that matches today, and do only that.

---

## "It's been a while and I've forgotten everything"

You haven't. Recognising something comes back far faster than learning it did.
This is a reload, not a restart:

1. **Read the map (about 20 minutes).**
   [`cheatsheets/_patterns.md`](cheatsheets/_patterns.md) has every pattern, its
   trigger, and its template. [`cheatsheets/00_complexity.md`](cheatsheets/00_complexity.md)
   is Big-O on one page.
2. **Run `./review`.** It ranks topics by how much they've faded. Trust it over
   your gut, which overrates the topics you enjoyed.
3. **Re-solve one problem you've already solved.** Open a file in
   [`leetcode/`](leetcode/), read **only the header**, and solve it on LeetCode
   or in a blank file. Then compare with the rest of the file. The point isn't
   progress: it's proving the knowledge is still there.
4. **Then carry on** where [`PROGRESS.md`](PROGRESS.md) left off.

About ninety minutes, and you're working again.

## "I only have 15 minutes"

Read one cheatsheet, then `./log "read the sliding window cheatsheet" 15`.

That counts. Waiting for a free afternoon that never comes is how six months go
by, and a 15-minute session is never wasted here.

## "I'm back and want to make progress"

[`ROADMAP.md`](ROADMAP.md) shows each module's progress and what to do next.
[`PROBLEMS.md`](PROBLEMS.md) shows which Blind 75 problems are left.

## "I have an interview soon"

1. [`cheatsheets/_patterns.md`](cheatsheets/_patterns.md)
2. Re-solve the files in [`leetcode/`](leetcode/) from their headers alone.
3. Re-solve the ★ starred problems in [`PROGRESS.md`](PROGRESS.md).

Skip everything else. This isn't the week to learn a new pattern.

## "My setup doesn't work any more"

```bash
python3 -m pip install -r requirements.txt
./check all
```

If `./check all` passes, everything is fine. It checks every reference
solution, every write-up, and that the indexes are up to date.

---

## Why a reload works

DSA knowledge fades when it's stored as thousands of separate problems.
Patterns compress, and compressed things reload fast. That's why each topic is
kept at three depths: problems (fade fast), notes (fade slowly), and
cheatsheets (barely fade). You reload from the cheatsheet, and the rest follows.

It's also why each module's cheatsheet should be written **in your own
words**. Compressing it yourself is what makes it stick, and later you'll
trust your own phrasing more than anyone else's.

**The gap was never the problem. Believing the gap meant starting over was.**

[← back to the repo](README.md)
