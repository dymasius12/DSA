"""
1071. Greatest Common Divisor of Strings  ·  Easy  ·  Math & Geometry
https://leetcode.com/problems/greatest-common-divisor-of-strings/
(Not in the Blind 75. Extra practice.)

"t divides s" means s is t repeated some whole number of times. Return the
longest string that divides BOTH str1 and str2, or "" if there isn't one.
Constraints: 1 <= len(str1), len(str2) <= 1000, uppercase letters.

Pattern:     string periodicity + gcd of the lengths
Complexity:  O(n + m) time and space (the two glued strings)
Solved:      2026-10-06

Key insight
    If both strings are built from the same block, then gluing them in either
    order gives the same text: both are just that block repeated (a + b) times.
    So str1 + str2 == str2 + str1 decides, in one line, whether any answer
    exists.

    Once it does, the answer's LENGTH must divide both lengths, and the
    longest such length is gcd(len1, len2). The first gcd characters are the
    answer, with nothing left to check.

Why the test is trustworthy
    One direction is easy: same block in both, so both gluings match.
    The other direction (if the gluings match, a common block must exist) is
    the interesting one, and it's a known result about periodic strings
    (Fine and Wilf's theorem). Worth saying in an interview that you know the
    check is sound, even if you don't prove it at the whiteboard.

Run the tests:  python3 leetcode/18_math_geometry/1071_greatest_common_divisor_of_strings.py
"""
from math import gcd


# ------------------------- my solution, as submitted -------------------------

# 1071. Greatest Common Divisor of Strings (Easy)
#
# input : str1, str2 strings (uppercase letters)
# output: the largest string x such that x repeated fills BOTH str1 and str2
# todo  : "t divides s" means s = t + t + ... + t; return "" if no such x exists
# constraints: 1 <= len(str1), len(str2) <= 1000
#
# ideas:
#   1. if any x divides both, then str1 + str2 must equal str2 + str1
#      (same blocks, so the order of gluing cannot matter)
#      if they differ -> no answer -> return ""
#   2. x must repeat to fill both, so len(x) divides both lengths
#      the largest such length is gcd(len1, len2)
#   3. return the first gcd characters of str1
#
#   "ABCABC" + "ABC" = "ABCABCABC"  (same both ways) -> gcd(6,3)=3 -> "ABC"
#   "LEET"   + "CODE" = "LEETCODE"
#   "CODE"   + "LEET" = "CODELEET"  (different)      -> ""
#
# remember:
#   - ONE check kills every "no answer" case: str1 + str2 != str2 + str1
#   - this is what catches "AAAAAB" vs "AAA": "AAA" looks valid until the final B
#   - the LENGTH must be the gcd, not one of the lengths:
#     "ABABAB" vs "ABAB" -> gcd(6,4)=2 -> "AB", not "ABAB"
#   - str1[:k] or str2[:k] both work: after step 1 they share the same first k chars
#   - after step 1 passes, no verifying is needed; the prefix is guaranteed
#   - complexity: O(n + m) time, O(n + m) space (for the glued strings)
#   - test: "ABCABC","ABC" -> "ABC" | "ABABAB","ABAB" -> "AB"
#           "LEET","CODE" -> "" | "AAAAAB","AAA" -> ""

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        # step 1: check whether a common block can exist at all
        if str1 + str2 != str2 + str1:                   # glue both ways and compare
            return ""                                    # orders differ -> no answer

        # step 2: find the length of the answer
        length_of_gcd_string = gcd(len(str1), len(str2))  # largest length dividing both

        # step 3: cut that many characters off the front
        return str1[:length_of_gcd_string]                # str2[:k] gives the same

# ------------------------------------------------------------------------------


def gcd_of_strings_checked(str1: str, str2: str) -> str:
    """The version that trusts nothing: build the candidate, then verify it.

    Slower and longer, but it needs no theorem. Worth writing first if you
    can't remember whether the glue test is sound.
    """
    k = gcd(len(str1), len(str2))
    candidate = str1[:k]
    if candidate * (len(str1) // k) == str1 and candidate * (len(str2) // k) == str2:
        return candidate
    return ""


# Review notes
#
# 1. Correct, and this is the intended solution. Against a brute force that
#    tries every possible block length, it agrees on 20,000 random pairs.
#
# 2. The glue test is the whole trick, and your "AAAAAB vs AAA" note is the
#    best example of why it's needed: "AAA" divides neither string, but a
#    naive prefix check looks fine until the final B. Here,
#    "AAAAAB" + "AAA" is "AAAAABAAA" while "AAA" + "AAAAAB" is "AAAAAAAAB",
#    so it's rejected immediately.
#
# 3. Your note that the length must be the gcd (not either length) is the
#    other thing people get wrong. "ABABAB" and "ABAB" share "ABAB" as a
#    prefix, but "ABAB" doesn't divide "ABABAB" (6 isn't a multiple of 4).
#    gcd(6, 4) = 2 gives "AB", which divides both.
#
# 4. "no verifying is needed" is true, and it's worth knowing WHY you can
#    skip it: that's Fine and Wilf's theorem doing the work. If you'd rather
#    not lean on a theorem you can't prove on the spot, gcd_of_strings_checked
#    above builds the candidate and verifies it, which is just as fast here.
#
# 5. Space is O(n + m) because str1 + str2 builds a whole new string. You can
#    avoid that by verifying instead of gluing (the function above), which is
#    O(1) extra. Not worth it at n <= 1000, but it's the honest trade-off.


# ----------------------------------- tests ------------------------------------

def _brute_force(str1, str2):
    """Try every block length from longest to shortest."""
    for k in range(min(len(str1), len(str2)), 0, -1):
        block = str1[:k]
        if len(str1) % k == 0 and len(str2) % k == 0 \
                and block * (len(str1) // k) == str1 \
                and block * (len(str2) // k) == str2:
            return block
    return ""


if __name__ == "__main__":
    import random

    versions = {
        "my solution": lambda a, b: Solution().gcdOfStrings(a, b),
        "verify instead": gcd_of_strings_checked,
        "brute force": _brute_force,
    }

    cases = [
        ("example 1",                      "ABCABC",  "ABC",   "ABC"),
        ("example 2",                      "ABABAB",  "ABAB",  "AB"),
        ("example 3, nothing in common",   "LEET",    "CODE",  ""),
        ("from my notes: the trailing B",  "AAAAAB",  "AAA",   ""),
        ("identical strings",              "ABC",     "ABC",   "ABC"),
        ("one letter each, same",          "A",       "A",     "A"),
        ("one letter each, different",     "A",       "B",     ""),
        ("whole of the shorter divides",   "ABABAB",  "AB",    "AB"),
        ("same letters, wrong order",      "ABAB",    "BABA",  ""),
        ("coprime lengths, no answer",     "ABCABC",  "ABCA",  ""),
        # gcd(1000, 500) = 500, so the answer is the whole shorter string
        ("longest allowed",                "AB" * 500, "AB" * 250, "AB" * 250),
        ("longest allowed, gcd smaller",   "AB" * 500, "AB" * 333, "AB"),
    ]
    for name, a, b, want in cases:
        for label, fn in versions.items():
            got = fn(a, b)
            assert got == want, f"{label}: {name} gave {got!r}, want {want!r}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    rng = random.Random(0)
    for _ in range(20_000):
        # A small alphabet and short blocks, so real answers come up often.
        if rng.random() < 0.5:
            block = "".join(rng.choice("AB") for _ in range(rng.randint(1, 3)))
            a = block * rng.randint(1, 5)
            b = block * rng.randint(1, 5)
        else:
            a = "".join(rng.choice("AB") for _ in range(rng.randint(1, 8)))
            b = "".join(rng.choice("AB") for _ in range(rng.randint(1, 8)))
        want = _brute_force(a, b)
        for label in ("my solution", "verify instead"):
            assert versions[label](a, b) == want, f"{label} on {a!r}, {b!r}: want {want!r}"
    print("20,000 random pairs: the glue test matches a full search for the longest block")

    # Note 2: why the glue test catches "AAAAAB" vs "AAA".
    assert "AAAAAB" + "AAA" == "AAAAABAAA"
    assert "AAA" + "AAAAAB" == "AAAAAAAAB"
    print('note 2 confirmed: "AAAAAB"+"AAA" and "AAA"+"AAAAAB" differ, so it returns "" at once')

    # Note 3: the answer's length is the gcd, not either length.
    assert gcd(6, 4) == 2 and Solution().gcdOfStrings("ABABAB", "ABAB") == "AB"
    assert "ABAB" * (6 // 4 if 6 % 4 == 0 else 0) != "ABABAB"
    print('note 3 confirmed: "ABAB" can\'t divide "ABABAB" (6 % 4 != 0), so the answer is "AB"')
