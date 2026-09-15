"""
121. Best Time to Buy and Sell Stock  ·  Easy  ·  Blind 75  ·  Sliding Window
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

prices[i] is a stock's price on day i. Buy on one day and sell on a LATER day.
Return the maximum profit, or 0 if no trade makes money.
Constraints: 1 <= len(prices) <= 10^5, 0 <= prices[i] <= 10^4.

Pattern:     running minimum, which is a sliding window with the left edge
             at the cheapest day so far
Complexity:  O(n) time, O(1) space (once the slice is removed, see note 1)
Solved:      2026-09-15

Key insight
    The best sale on any given day is "today's price minus the cheapest price
    before today". So you never need to look back over the earlier days: one
    variable remembers the cheapest price seen so far, and one pass is enough.

Sliding window view (why NeetCode files it under Sliding Window)
    left = buy day, right = sell day. Move right forward every step. When
    right finds a price lower than left's, move left to right, because
    buying there is better for every future sale. min_price is simply the
    price at `left`.

Brute force (worth saying first in an interview)
    Try every buy/sell pair: O(n^2). With n up to 10^5 that's about 5 * 10^9
    pairs, far too slow. The constraint is telling you to find O(n).

Run the tests:  python3 leetcode/03_sliding_window/0121_best_time_to_buy_and_sell_stock.py
"""
from typing import List


# ------------------------- my solution, as submitted -------------------------

# input: prices[int], where prices[i] is the stock price on the ith day
# output: the maximum profit from one transaction, or 0 if no profit is possible
# todo: buy the stock on one day and sell it on a later day for the highest possible profit
# ideas: go through the array and keep track of the lowest price seen so far
#        for each price, calculate the profit we would make if we sold on that day
#        we do not need to save the indices because iterating from left to right ensures
#        that the buying day always comes before the selling day
# in short: start with the first price as min_price, then update max_profit and min_price
#           as we iterate through the remaining prices
# Time:  O(n) — visit each price once
# Space: O(1) — only use a few variables

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Treat the first day's price as our cheapest buying price so far
        min_price = prices[0]

        # Start at 0 because we can choose not to make an unprofitable trade
        max_profit = 0

        # Begin on the second day since the first day is our starting buy price
        for current_price in prices[1:]:

            # If we sell today, this is how much profit we would make
            current_profit = current_price - min_price

            # Keep this profit only if it is better than our previous best
            max_profit = max(max_profit, current_profit)

            # If today's price is cheaper, use it as the buy price for future days
            min_price = min(min_price, current_price)

        # Return the best profit found, or 0 if every price went down
        return max_profit

# ------------------------------------------------------------------------------


# Review notes
#
# 1. The space is O(n), not O(1). `prices[1:]` is a slice, and slices COPY:
#    it builds a new list of n - 1 items before the loop starts. For 10^5
#    prices that's roughly 800 KB of extra memory (measured in the tests
#    below). The fix is to loop over `prices` itself. Day 0 then gives a
#    profit of 0 and a min_price that doesn't change, so the answer is the
#    same, with no copy. (cheatsheets/_python.md: "Slices copy".)
#
# 2. Your comments are excellent. The header states input, output, the idea,
#    why indices aren't needed, and the time/space before any code. That's
#    exactly what to say out loud in an interview. Only the space line was off.
#
# 3. Update order: you compute today's profit BEFORE lowering min_price, which
#    matches "buy before sell". Doing it the other way round also works: if
#    today becomes the new minimum, today's profit is 0, which never beats
#    max_profit. The tests check both orders give the same answers.
#
# 4. `prices[0]` relies on the constraint that there's at least one price.
#    On an empty list it raises IndexError. That's fine here, but in an
#    interview it's worth asking "can prices be empty?" before assuming.


def max_profit_clean(prices: List[int]) -> int:
    """Same algorithm, note 1 applied: no slice, so O(1) extra space."""
    min_price = prices[0]
    max_profit = 0
    for price in prices:
        max_profit = max(max_profit, price - min_price)
        min_price = min(min_price, price)
    return max_profit


def max_profit_two_pointers(prices: List[int]) -> int:
    """The sliding-window version: left = buy day, right = sell day."""
    left = 0
    best = 0
    for right in range(1, len(prices)):
        if prices[right] < prices[left]:
            left = right                      # cheaper buy day found
        else:
            best = max(best, prices[right] - prices[left])
    return best


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random
    import tracemalloc

    def brute_force(prices):
        return max([0] + [prices[j] - prices[i]
                          for i in range(len(prices))
                          for j in range(i + 1, len(prices))])

    def min_first(prices):   # note 3: lower min_price BEFORE computing profit
        min_price, best = prices[0], 0
        for p in prices:
            min_price = min(min_price, p)
            best = max(best, p - min_price)
        return best

    solutions = {
        "my solution": lambda p: Solution().maxProfit(p),
        "clean": max_profit_clean,
        "two pointers": max_profit_two_pointers,
        "min-first order": min_first,
    }

    cases = [
        ("example 1",                            [7, 1, 5, 3, 6, 4], 5),
        ("example 2 (only goes down)",           [7, 6, 4, 3, 1],    0),
        ("one price",                            [5],                0),
        ("two prices, up",                       [1, 5],             4),
        ("two prices, down",                     [5, 1],             0),
        ("all the same",                         [3, 3, 3],          0),
        ("cheapest day comes after the best trade", [3, 8, 1, 2],    5),
        ("cheapest day is the last day",         [4, 9, 2, 6, 0],    5),
        ("price extremes",                       [0, 10_000],        10_000),
    ]
    for name, prices, want in cases:
        for label, fn in solutions.items():
            assert fn(prices) == want, f"{label}: {name} gave {fn(prices)}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(solutions)})")

    rng = random.Random(0)
    for _ in range(500):
        prices = [rng.randint(0, 50) for _ in range(rng.randint(1, 40))]
        want = brute_force(prices)
        for label, fn in solutions.items():
            assert fn(prices) == want, f"{label} disagrees with brute force on {prices}"
    print("500 random lists: all versions match the brute force")

    big = [rng.randint(0, 10_000) for _ in range(100_000)]
    assert len({fn(big) for fn in solutions.values()}) == 1
    print("100,000 prices: all versions agree")

    # Note 1: measure the extra memory of the slice.
    def peak_bytes(fn, prices):
        tracemalloc.start()
        fn(prices)
        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
        return peak
    ramp = list(range(100_000))
    with_slice = peak_bytes(Solution().maxProfit, ramp)
    no_slice = peak_bytes(max_profit_clean, ramp)
    assert with_slice > 500_000 and no_slice < 10_000, (with_slice, no_slice)
    print(f"note 1 confirmed: prices[1:] used {with_slice / 1000:.0f} KB extra, "
          f"looping over prices used {no_slice / 1000:.1f} KB")

    # Note 4: the empty-list behaviour the note describes.
    try:
        Solution().maxProfit([])
        raise AssertionError("expected IndexError on an empty list")
    except IndexError:
        print("note 4 confirmed: an empty list raises IndexError")
