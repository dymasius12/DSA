"""
104. Maximum Depth of Binary Tree  ·  Easy  ·  Blind 75  ·  Trees
https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree, return its maximum depth: the number of nodes
on the longest path from the root down to a leaf.
Constraints: 0 to 10^4 nodes, -100 <= Node.val <= 100.

Pattern:     tree DFS (recursion: 1 + max of the two children)
Complexity:  O(n) time, O(h) space for the call stack (h = height, up to n)
Solved:      2026-09-21

Key insight
    A tree's depth is defined in terms of smaller trees: 1 for this node, plus
    the deeper of its two subtrees. An empty subtree has depth 0. Write that
    sentence as code and the recursion is done.

LeetCode's input format
    [3,9,20,null,null,15,7] is the tree listed level by level, with null
    marking a missing child. Your function receives the root TreeNode, not
    the list. The tests below build trees from that format.

Run the tests:  python3 leetcode/07_trees/0104_maximum_depth_of_binary_tree.py
"""
# Lets `TreeNode | None` in the hint below run on Python 3.9.
from __future__ import annotations

from collections import deque


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ------------------------- my solution, as submitted -------------------------

# input : root of a binary tree (TreeNode, not an array) -- output: int max depth
# todo  : find the number of nodes on the longest path from root to a leaf
# constraints: 0 to 10^4 nodes, -100 <= Node.val <= 100
# idea (recursion):
#   1. empty spot (None) has depth 0
#   2. a real node's depth = 1 + the bigger depth of its two children
#   3. ask the left child, ask the right child, take the max, add 1
#   note: node count can't give the depth (2^x only works for full trees);
#         the shape matters, so we must walk down both sides

class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        # Step 1: Base case, where there is no root
        if root is None:
            return 0

        # Step 2: ask each child how deep it is
        left = self.maxDepth(root.left)
        right = self.maxDepth(root.right)

        # Step 3: this node counts as 1, plus taller side 
        return 1 + max(left,right)

# ------------------------------------------------------------------------------


# Review notes
#
# 1. Correct, and it's the standard answer. Your base case `root is None ->
#    0` also covers the empty tree the constraints allow (0 nodes), so there
#    is no separate special case.
#
# 2. Your note that node count can't give the depth is exactly right. Three
#    nodes can be depth 2 (a root with two children) or depth 3 (a chain).
#    Only the shape decides, which is why both sides have to be visited.
#
# 3. The space is O(h), where h is the height, not O(1): each recursive call
#    waits on the call stack until its children return. For a balanced tree
#    h is about log n. For a tree that's one long chain, h = n.
#
# 4. That chain is a real risk in Python. With 10^4 nodes in a line, the
#    recursion goes 10^4 calls deep, and Python's default limit is about
#    1,000: it raises RecursionError (the tests confirm this). An online judge
#    may run with a higher limit, but plain Python won't, and it's a good
#    follow-up question in an interview. Two answers:
#      - Iterate instead (max_depth_bfs and max_depth_stack below). Same O(n)
#        time, and no recursion limit.
#      - sys.setrecursionlimit(...) works, but it treats the symptom: very
#        deep recursion can still crash the interpreter itself.
#
# 5. BFS gives the depth for free: process the tree one level at a time and
#    count the levels. That's the "Tree BFS" template in
#    cheatsheets/_patterns.md.


def max_depth_bfs(root: TreeNode | None) -> int:
    """Note 5: count the levels, one at a time. No recursion."""
    if root is None:
        return 0
    depth = 0
    queue = deque([root])
    while queue:
        depth += 1
        for _ in range(len(queue)):          # exactly one level
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth


def max_depth_stack(root: TreeNode | None) -> int:
    """Note 4: the same DFS as yours, with an explicit stack of (node, depth)."""
    best = 0
    stack = [(root, 1)] if root else []
    while stack:
        node, depth = stack.pop()
        best = max(best, depth)
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
    return best


# ----------------------------------- tests ------------------------------------

def _build(values):
    """Build a tree from LeetCode's level-order list, e.g. [3,9,20,None,None,15,7]."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        for side in ("left", "right"):
            if i < len(values) and values[i] is not None:
                child = TreeNode(values[i])
                setattr(node, side, child)
                queue.append(child)
            i += 1
    return root


def _chain(n):
    """n nodes, each the right child of the one before: height n."""
    root = None
    for v in range(n):
        root = TreeNode(v, right=root)
    return root


if __name__ == "__main__":
    import random
    import sys

    versions = {
        "my solution": lambda root: Solution().maxDepth(root),
        "BFS": max_depth_bfs,
        "stack": max_depth_stack,
    }

    cases = [
        ("example 1",                    [3, 9, 20, None, None, 15, 7],     3),
        ("example 2",                    [1, None, 2],                      2),
        ("empty tree",                   [],                                0),
        ("one node",                     [0],                               1),
        ("only left children",           [1, 2, None, 3, None, 4],          4),
        ("full tree of 3 levels",        [1, 2, 3, 4, 5, 6, 7],             3),
        ("deepest leaf on the left",     [1, 2, 3, 4, None, None, None, 5], 4),
        ("negative values",              [-100, -1, 100],                   2),
    ]
    for name, values, want in cases:
        for label, fn in versions.items():
            got = fn(_build(values))
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    # Random trees: every version agrees with a brute force over all paths.
    def all_path_lengths(node, depth=1):
        if node is None:
            return []
        if not node.left and not node.right:
            return [depth]
        return all_path_lengths(node.left, depth + 1) + all_path_lengths(node.right, depth + 1)

    rng = random.Random(0)
    for _ in range(1000):
        values = [rng.randint(-100, 100) if rng.random() < 0.75 else None
                  for _ in range(rng.randint(0, 40))]
        root = _build(values)
        want = max(all_path_lengths(root), default=0)
        for label, fn in versions.items():
            assert fn(root) == want, f"{label} on {values}"
    print("1000 random trees: all versions match the longest root-to-leaf path")

    # Note 2: the same node count, different depths.
    assert Solution().maxDepth(_build([1, 2, 3])) == 2
    assert Solution().maxDepth(_build([1, 2, None, 3])) == 3
    print("note 2 confirmed: 3 nodes can be depth 2 or depth 3, so count alone can't tell")

    # Note 4: a chain of 10^4 nodes, the largest the constraints allow.
    chain = _chain(10_000)
    assert max_depth_bfs(chain) == max_depth_stack(chain) == 10_000
    try:
        Solution().maxDepth(chain)
        raise AssertionError("expected RecursionError at the default limit")
    except RecursionError:
        pass
    print(f"note 4 confirmed: a 10,000-node chain makes the recursive version raise "
          f"RecursionError (limit {sys.getrecursionlimit()}); BFS and stack return 10000")
