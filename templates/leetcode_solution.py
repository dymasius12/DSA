"""
NNN. Problem Title  ·  Easy  ·  Blind 75  ·  Module Name
https://leetcode.com/problems/problem-slug/

The problem in one or two sentences, in your own words.
Constraints: the ones that matter (input sizes, value ranges, guarantees).

Pattern:     one short line, e.g. "sliding window" (./sync shows this in the index)
Complexity:  O(?) time, O(?) space
Solved:      YYYY-MM-DD

Key insight
    The one idea that makes the problem easy once you see it.

Brute force (worth saying first in an interview)
    The obvious approach, its complexity, and why it's too slow.

Run the tests:  python3 leetcode/NN_module/NNNN_problem_name.py
"""
# Save as leetcode/<module folder>/NNNN_problem_name.py (see tools/catalog.py
# for folder names), fill it in, run the file, then run ./sync.
from typing import List, Optional


# ------------------------- my solution, as submitted -------------------------

# input : what you're given
# output: what you return
# todo  : the task in plain words
#
# constraints:
#   - the limits, and what they rule in or out
#
# ideas:
#   1. step by step, before writing any code
#
# remember:
#   - the trick, the trap, the Python detail you'd forget
#   - complexity: O(?) time, O(?) space
#   - test: example -> answer | edge case -> answer

class Solution:
    def methodName(self, nums: List[int]) -> int:
        raise NotImplementedError

# ------------------------------------------------------------------------------


# Review notes
#
# 1. Is it correct, and what proves it? (edge cases, a brute-force comparison)
# 2. What's good about it, specifically?
# 3. What could be better, and why? Back each claim with a test below.


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    # Test three shapes: the normal case, the smallest or empty case, and the
    # edge case named in the problem's examples.
    cases = [
        # (name, input, expected)
        ("example 1", [1, 2, 3], 0),
        ("smallest input", [1], 0),
    ]
    for name, nums, want in cases:
        got = Solution().methodName(nums)
        assert got == want, f"{name}: got {got}, want {want}"
    print(f"all {len(cases)} cases pass")
