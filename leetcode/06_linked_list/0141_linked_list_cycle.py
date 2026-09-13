"""
141. Linked List Cycle  ·  Easy  ·  Blind 75  ·  Linked List
https://leetcode.com/problems/linked-list-cycle/

Given the head of a singly linked list, return True if some node can be
reached again by following `next` pointers (a cycle), otherwise False.
Follow-up: can you do it in O(1) memory?

Pattern:     fast & slow pointers (Floyd's tortoise and hare)
Complexity:  O(n) time, O(1) space, so it meets the follow-up
Solved:      2026-09-13

Key insight
    Once both pointers are inside the cycle, fast gains exactly one node on
    slow every step. The gap shrinks 3, 2, 1, 0, so fast can never jump over
    slow: they must meet. With no cycle, fast simply reaches the end (None).

Brute force (worth saying first in an interview)
    Keep a set of visited nodes; seeing one again means a cycle.
    O(n) time but O(n) space. Floyd's gets rid of that set.

Run the tests:  python3 leetcode/06_linked_list/0141_linked_list_cycle.py
"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


# ------------------------- my solution, as submitted -------------------------

# input: linked list -- output: true or false
# to do: find if a linked list has cycle
# clue: use hare and tortoise, two pointers. 

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # declare the hare and tortoise slow and fast pointers 
        slow = head
        fast = head

        # loop through the linked list
        while fast and fast.next: 
            slow = slow.next # tortoise moves 1 step
            fast = fast.next.next # hare moves 2 step

            # if the slow pointers = fast pointers 
            if slow == fast:
                # there is a cycle return true
                return True

        # else return false. 
        # this should be outside while cycle 
        # because it is a conclusion at the end. otherwise wrong.
        else:
            return False

# ------------------------------------------------------------------------------


# Review notes
#
# 1. `while ... else:` is a real Python feature, and it's what this code uses.
#    The `else` belongs to the `while`: it runs when the loop condition turns
#    false without a `break`. That's the same moment code after the loop would
#    run, so the answer is identical. A plain `return False` after the loop is
#    clearer, though. Many readers will think while-else is an if-else that
#    got mis-indented.
#
# 2. `slow is fast` says "the same node" more precisely than `slow == fast`.
#    ListNode doesn't define __eq__, so `==` falls back to comparing identity
#    and works here, but `is` doesn't rely on that.
#
# 3. `while fast and fast.next` is exactly the right condition, because
#    `fast.next.next` needs both to exist. Checking only `fast` crashes on
#    odd-length lists: fast lands on the last node, and last.next.next fails.


def has_cycle_clean(head: Optional[ListNode]) -> bool:
    """The same algorithm, with notes 1 and 2 applied."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# ----------------------------------- tests ------------------------------------

def _build(vals, pos):
    """LeetCode's input format: values, plus the index the tail links back to."""
    nodes = [ListNode(v) for v in vals]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if pos != -1 and nodes:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


if __name__ == "__main__":
    cases = [
        ("example 1",                  [3, 2, 0, -4],        1,     True),
        ("example 2",                  [1, 2],               0,     True),
        ("example 3",                  [1],                 -1,     False),
        ("empty list",                 [],                  -1,     False),
        ("one node pointing to itself", [1],                 0,     True),
        ("two nodes, no cycle",        [1, 2],              -1,     False),
        ("odd length, no cycle",       [1, 2, 3],           -1,     False),
        ("tail points to itself",      [1, 2, 3, 4],         3,     True),
        ("repeated values, no cycle",  [7, 7, 7, 7],        -1,     False),
        ("10,000 nodes, cycle",        list(range(10_000)),  9_999, True),
        ("10,000 nodes, no cycle",     list(range(10_000)), -1,     False),
    ]
    for name, vals, pos, want in cases:
        assert Solution().hasCycle(_build(vals, pos)) is want, f"my solution: {name}"
        assert has_cycle_clean(_build(vals, pos)) is want, f"clean version: {name}"
    print(f"all {len(cases)} cases pass (my solution and the clean version)")
