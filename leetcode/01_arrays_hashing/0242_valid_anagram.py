"""
242. Valid Anagram  ·  Easy  ·  Blind 75  ·  Arrays & Hashing
https://leetcode.com/problems/valid-anagram/

Given two strings s and t, return True if t is an anagram of s (the same
letters, the same number of times, in any order), otherwise False.
Constraint: s and t contain only lowercase English letters.
Follow-up: what if the inputs contain Unicode characters?

Pattern:     counting (frequency array)
Complexity:  O(n) time, O(1) space (the array is always 26 slots, however
             long the strings are)
Solved:      2026-09-14

Key insight
    Walk both strings together: +1 for each letter of s, -1 for each letter
    of t. If they're anagrams every letter cancels out, so all 26 counts end
    at zero. One array does the job of two separate counts.

Brute force (worth saying first in an interview)
    sorted(s) == sorted(t). Correct and one line, but O(n log n) time.
    Counting gets it down to O(n).

Run the tests:  python3 leetcode/01_arrays_hashing/0242_valid_anagram.py
"""
import unicodedata
from collections import Counter


# ------------------------- my solution, as submitted -------------------------

# input: s: str and t:str -- output: true 
# task: valid anagram, true if t is anagram of s; otherwise false
# caveat: s and t has lowercase 
# idea: count the frequency of those characters

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # check if the length of s and t are different? 
        if len(s) != len(t):
            # if different then false not anagram
            return False
        
        # declare array of 26
        count = [0] * 26

        # for loop for the length of s (t is equal length anyway)
        for i in range(len(s)):
            # get character from s and count +1 in the array
            count[ord(s[i]) - ord('a')] += 1
            # get the character from t and count -1 in the array
            count[ord(t[i]) - ord('a')] -= 1
        
        # loop through count
        for c in count:
            # if any of them is not 0
            if c != 0:
                # return false because not anagram
                return False
        # otherwise return true
        return True

# ------------------------------------------------------------------------------


# Review notes
#
# 1. The length check up front is a good habit. It's a free early exit, and it
#    makes "t is equal length anyway" true, which is what lets one loop walk
#    both strings safely.
#
# 2. `for i in range(len(s))` then `s[i]` and `t[i]` can be
#    `for a, b in zip(s, t)`: same thing, no indexes to get wrong.
#    The final loop can be `return all(c == 0 for c in count)`.
#
# 3. The follow-up: this solution only works because of the "lowercase
#    letters" rule, and outside it, it fails in two different ways.
#      - Uppercase gives a silently WRONG answer. ord('Z') - ord('a') is -7,
#        and Python lists accept negative indexes, so 'Z' lands in the slot
#        for 't'. isAnagram("Z", "t") returns True.
#      - Other characters crash. ord('é') - ord('a') is 136, past the end of
#        a 26-slot list, so it raises IndexError.
#    The silent wrong answer is the worse of the two.
#
# 4. Answer to the follow-up: count with a dict instead of a fixed array, so
#    any character can be a key. Counter(s) == Counter(t) does that in one
#    line. Space becomes O(k), where k is the number of distinct characters.
#    One extra detail interviewers like: the same visible character can be
#    stored two ways ('é' as one code point, or 'e' plus an accent mark), so
#    normalize both strings first (see is_anagram_unicode below).


def is_anagram_clean(s: str, t: str) -> bool:
    """Your approach, with note 2 applied. Still lowercase-only."""
    if len(s) != len(t):
        return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[ord(a) - ord('a')] += 1
        count[ord(b) - ord('a')] -= 1
    return all(c == 0 for c in count)


def is_anagram_unicode(s: str, t: str) -> bool:
    """The follow-up: works for any characters (note 4)."""
    s = unicodedata.normalize("NFC", s)
    t = unicodedata.normalize("NFC", t)
    return len(s) == len(t) and Counter(s) == Counter(t)


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random
    import string

    rng = random.Random(0)
    letters = list(string.ascii_lowercase)
    rng.shuffle(letters)
    big = ''.join(rng.choice(string.ascii_lowercase) for _ in range(50_000))
    big_shuffled = ''.join(rng.sample(big, len(big)))
    big_changed = big_shuffled[:-1] + ('a' if big_shuffled[-1] != 'a' else 'b')

    cases = [
        ("example 1",                      "anagram", "nagaram",  True),
        ("example 2",                      "rat",     "car",      False),
        ("different lengths",              "a",       "ab",       False),
        ("same letters, different counts", "aacc",    "ccac",     False),
        ("single letter",                  "a",       "a",        True),
        ("all 26 letters, shuffled",       string.ascii_lowercase, ''.join(letters), True),
        ("50,000 letters, shuffled",       big,       big_shuffled, True),
        ("50,000 letters, one changed",    big,       big_changed,  False),
    ]
    for name, s, t, want in cases:
        assert Solution().isAnagram(s, t) is want, f"my solution: {name}"
        assert is_anagram_clean(s, t) is want, f"clean version: {name}"
        assert is_anagram_unicode(s, t) is want, f"unicode version: {name}"
    print(f"all {len(cases)} cases pass (my solution, clean, and unicode versions)")

    # Note 3: pin down how the array version behaves outside the constraints,
    # so the review note stays true.
    assert Solution().isAnagram("Z", "t") is True        # silently wrong
    try:
        Solution().isAnagram("é", "e")
        raise AssertionError("expected IndexError for 'é'")
    except IndexError:
        pass
    print("note 3 confirmed: 'Z' vs 't' wrongly returns True, 'é' raises IndexError")

    # Note 4: the follow-up version handles what the array version can't.
    assert is_anagram_unicode("Z", "t") is False
    assert is_anagram_unicode("café", "éfac") is True
    assert is_anagram_unicode("日本", "本日") is True
    assert is_anagram_unicode("\u00e9", "e\u0301") is True   # "é" as one code point vs "e" + accent mark
    assert Counter("\u00e9") != Counter("e\u0301")           # without normalizing, they don't match
    print("note 4 confirmed: unicode version handles uppercase, accents, CJK, and both forms of 'é'")
