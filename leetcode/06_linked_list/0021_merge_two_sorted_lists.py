"""
21. Merge Two Sorted Lists  ·  Easy  ·  Blind 75  ·  Linked List
https://leetcode.com/problems/merge-two-sorted-lists/

Given the heads of two sorted linked lists, merge them into one sorted list by
splicing together the existing nodes, and return its head.
Constraints: 0 to 50 nodes in each list, -100 <= Node.val <= 100, both sorted
in non-decreasing order.

Pattern:     dummy head + tail pointer (the standard way to build a linked list)
Complexity:  O(n + m) time, O(1) space (nodes are relinked, never copied)
Solved:      2026-09-17

Key insight
    Always compare only the two FRONT nodes. Both lists are sorted, so the
    smaller front is the smallest node left anywhere. Attach it, advance that
    list, repeat. When one list runs out, the rest of the other is already
    sorted, so attach it whole in one step.

    The dummy node removes the special case of "the merged list is still
    empty, so where does the first node go?" Every node, including the first,
    is attached the same way: tail.next = node.

Run the tests:  python3 leetcode/06_linked_list/0021_merge_two_sorted_lists.py
"""
# Lets `ListNode | None` in the hints below run on Python 3.9 (see note 5).
from __future__ import annotations


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ------------------------- my solution, as submitted -------------------------

# input : heads of two sorted linked lists
# output: head of the merged sorted linked list
# todo  : merge two sorted linked lists into one list by relinking the existing nodes
#
# constraints:
#   - number of nodes in both lists: 0 to 50 (either list can be empty)
#   - -100 <= Node.val <= 100
#   - both lists sorted in non-decreasing order
#
# ideas:
#   1. make a dummy node as a fake head, and a tail pointer starting at dummy
#   2. while both lists still have nodes:
#        compare the two front nodes, attach the smaller one to tail.next,
#        move that list forward one node, then move tail forward
#   3. one list is now empty: attach whatever is left of the other (already sorted)
#   4. return dummy.next (the real head, skipping the fake one)
#
# remember:
#   - dummy = bookmark at the start (never moves); tail = pen at the end (keeps moving)
#   - tail = dummy makes two names for the SAME node, not a copy
#   - `a or b` returns a if a is not empty, otherwise b
#   - complexity: O(n + m) time, O(1) space
#   - test: [1,2,4] + [1,3,4] -> [1,1,2,3,4,4] | [] + [] -> [] | [] + [0] -> [0]

class Solution:
    def mergeTwoLists(self, list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
        # step 1: dummy node (fake head) + tail pointer
        dummy = ListNode()
        tail = dummy

        # step 2: loop while both lists have nodes
        while list1 and list2:
            if list1.val <= list2.val:      # compare the two front nodes
                tail.next = list1           # attach the smaller node
                list1 = list1.next          # move that list forward
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next                # move tail forward

        # step 3: attach the leftover list (at least one is None now)
        tail.next = list1 or list2

        # step 4: return the real head, skipping the fake one
        return dummy.next

# ------------------------------------------------------------------------------


# Review notes
#
# 1. Correct, and the textbook solution. It really is O(1) space: the only new
#    node is the dummy. Every other node in the result is an original node,
#    relinked (the tests check this by identity).
#
# 2. Your "remember" notes are the strongest part.
#      - "dummy = bookmark, tail = pen" is exactly right: dummy never moves, so
#        dummy.next still points at the real head once tail has moved on.
#      - "tail = dummy makes two names for the SAME node" is the key idea
#        behind step 1. The first `tail.next = ...` changes dummy.next too,
#        because they're one node.
#
# 3. `<=` rather than `<` is a nice touch. On a tie it takes list1's node
#    first, so equal values keep their original order (a "stable" merge).
#    The problem doesn't require it, but merge sort relies on exactly this.
#
# 4. On `a or b`: precisely, `or` returns a if a is TRUTHY, otherwise b. A
#    ListNode is always truthy (it doesn't define __bool__ or __len__) and
#    None is falsy, so here it means "whichever list isn't exhausted". The
#    same line is also correct when both are None: it attaches None.
#
# 5. `ListNode | None` in a type hint needs Python 3.10+. LeetCode is newer,
#    so it's fine there, but on Python 3.9 the class fails to even define:
#    "TypeError: unsupported operand type(s) for |". This file adds
#    `from __future__ import annotations` at the top so your code runs locally
#    unchanged. On 3.9 without that import, write `Optional[ListNode]`.
#
# 6. Alternative worth knowing: the recursive version is shorter,
#        if not list1 or not list2: return list1 or list2
#        if list1.val <= list2.val:
#            list1.next = merge(list1.next, list2); return list1
#        list2.next = merge(list1, list2.next); return list2
#    but it uses O(n + m) stack space, one frame per node. Your iterative
#    version is the better interview answer.


def merge_recursive(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    """Note 6: shorter, but O(n + m) space on the call stack."""
    if not list1 or not list2:
        return list1 or list2
    if list1.val <= list2.val:
        list1.next = merge_recursive(list1.next, list2)
        return list1
    list2.next = merge_recursive(list1, list2.next)
    return list2


# ----------------------------------- tests ------------------------------------

def _build(vals, tag=None):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
        head.tag = tag                 # remember which list a node came from
    return head


def _to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def _nodes(head):
    out = []
    while head:
        out.append(head)
        head = head.next
    return out


if __name__ == "__main__":
    import random

    versions = {
        "my solution": lambda a, b: Solution().mergeTwoLists(a, b),
        "recursive": merge_recursive,
    }

    cases = [
        ("example 1",                  [1, 2, 4],    [1, 3, 4],     [1, 1, 2, 3, 4, 4]),
        ("example 2, both empty",      [],           [],            []),
        ("example 3, first empty",     [],           [0],           [0]),
        ("second empty",               [5],          [],            [5]),
        ("all of list1 comes first",   [1, 2, 3],    [7, 8, 9],     [1, 2, 3, 7, 8, 9]),
        ("all of list2 comes first",   [7, 8, 9],    [1, 2, 3],     [1, 2, 3, 7, 8, 9]),
        ("different lengths",          [2],          [1, 3, 5, 7],  [1, 2, 3, 5, 7]),
        ("all equal values",           [4, 4],       [4, 4, 4],     [4, 4, 4, 4, 4]),
        ("value extremes",             [-100, 100],  [-100, 0],     [-100, -100, 0, 100]),
    ]
    for name, a, b, want in cases:
        for label, fn in versions.items():
            got = _to_list(fn(_build(a), _build(b)))
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(500):
        a = sorted(rng.randint(-100, 100) for _ in range(rng.randint(0, 50)))
        b = sorted(rng.randint(-100, 100) for _ in range(rng.randint(0, 50)))
        for label, fn in versions.items():
            assert _to_list(fn(_build(a), _build(b))) == sorted(a + b), f"{label}: {a} + {b}"
    print("500 random pairs of up to 50 nodes: both versions match sorted(a + b)")

    # Note 1: splicing, not copying. The result holds exactly the original nodes.
    l1, l2 = _build([1, 3, 5]), _build([2, 4, 6])
    originals = {id(n) for n in _nodes(l1) + _nodes(l2)}
    merged = Solution().mergeTwoLists(l1, l2)
    assert {id(n) for n in _nodes(merged)} == originals
    print("note 1 confirmed: every node in the result is an original node, no copies")

    # Note 3: <= makes it stable. On ties, list1's nodes come first.
    merged = Solution().mergeTwoLists(_build([1, 2, 2], tag="list1"),
                                      _build([2, 2, 3], tag="list2"))
    twos = [n.tag for n in _nodes(merged) if n.val == 2]
    assert twos == ["list1", "list1", "list2", "list2"], twos
    print("note 3 confirmed: on equal values, list1's nodes stay ahead of list2's")

    # Note 4: `a or b` when both are exhausted attaches None, which is correct.
    assert (None or None) is None
    node = ListNode(0)
    assert (node or None) is node and (None or node) is node
    print("note 4 confirmed: `or` picks the non-None list, and gives None when both are None")
