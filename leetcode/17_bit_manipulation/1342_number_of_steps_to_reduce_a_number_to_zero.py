"""
1342. Number of Steps to Reduce a Number to Zero  ·  Easy  ·  Bit Manipulation
https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/
(Not in the Blind 75. Extra practice.)

Count the steps to reach 0: halve the number if it's even, subtract 1 if it's
odd.
Constraints: 0 <= num <= 10^6.

Pattern:     simulation loop (and, underneath, binary digits)
Complexity:  O(log num) time, O(1) space
Solved:      2026-09-24

Key insight
    Halving shrinks a number fast: 10^6 needs about 20 halvings, not a million
    steps. That's why the loop is O(log num).

In binary, the steps are countable without looping
    Halving an even number = dropping its last binary digit (a 0).
    Subtracting 1 from an odd number = turning its last digit from 1 into 0.
    So every binary digit is dropped once, and every 1 costs one extra step
    to clear first. The final 1 needs no drop, hence the -1:

        steps = (number of binary digits) + (number of 1s) - 1     for num > 0

    14 is 1110: 4 digits + three 1s - 1 = 6. Matches the example.

Run the tests:  python3 leetcode/17_bit_manipulation/1342_number_of_steps_to_reduce_a_number_to_zero.py
"""


# ------------------------- my solution, as submitted -------------------------

# input : num: int
# output: number of steps to reach 0
# todo  : each step, if num is even divide it by 2, if odd subtract 1;
#         count how many steps until num is 0
# constraints: 0 <= num <= 10^6
#
# idea:
#   1. loop while num is not 0
#   2. even -> divide by 2, odd -> subtract 1
#   3. count 1 step each time
#   4. return the count

class Solution:
    def numberOfSteps(self, num: int) -> int:
        # step 1: declare the step counter
        steps = 0

        # step 2: keep reducing until num reaches 0
        while num != 0:
            # even: divide by 2
            if num % 2 == 0:
                num //= 2
            # odd: subtract 1
            else:
                num -= 1

            # count this step
            steps += 1

        # step 3: return the total steps
        return steps

# ------------------------------------------------------------------------------


def number_of_steps_bits(num: int) -> int:
    """No loop over the value: read the answer off the binary digits."""
    if num == 0:
        return 0
    return num.bit_length() + bin(num).count("1") - 1


# Review notes
#
# 1. Correct, and your complexity note is the important one: O(log num), not
#    O(num). Each halving removes a binary digit, so 10^6 takes about 20
#    halvings plus at most one subtraction each, around 40 steps.
#
# 2. `num = 0` returning 0 is right, and it's free: the loop condition is
#    false immediately. That's the whole "0 <= num" edge case handled.
#
# 3. `//` versus `/` is the detail to keep. `7 / 2` is 3.5 and `8 / 2` is 4.0,
#    a float, and floats drift once numbers get large. `//` keeps an int.
#    (cheatsheets/_easily_forgotten.md has the same warning.)
#
# 4. Two micro-simplifications, neither required:
#      - `while num:` means the same as `while num != 0` for an int.
#      - `num % 2` is the same test as `num % 2 == 0` inverted, and `num & 1`
#        is the bitwise version.
#
# 5. The binary formula above (number_of_steps_bits) gives the same answer
#    with no loop over the value at all. It's a good thing to mention after
#    your loop: it shows you saw what the operations do to the bits. The
#    tests check both agree for every num from 0 to 20,000 and on random
#    values up to 10^6.


# ----------------------------------- tests ------------------------------------

if __name__ == "__main__":
    import random

    versions = {"my solution": lambda n: Solution().numberOfSteps(n),
                "binary formula": number_of_steps_bits}

    cases = [
        ("example 1: 14 -> 7 -> 6 -> 3 -> 2 -> 1 -> 0", 14, 6),
        ("example 2: 8 -> 4 -> 2 -> 1 -> 0",            8,  4),
        ("example 3",                                   123, 12),
        ("zero (smallest allowed)",                     0,  0),
        ("one",                                         1,  1),
        ("two",                                         2,  2),
        ("a power of two",                              1024, 11),
        ("largest allowed",                             10**6, 26),
    ]
    for name, num, want in cases:
        for label, fn in versions.items():
            got = fn(num)
            assert got == want, f"{label}: {name} gave {got}, want {want}"
    print(f"all {len(cases)} cases pass ({', '.join(versions)})")

    for num in range(0, 20_001):
        assert Solution().numberOfSteps(num) == number_of_steps_bits(num), num
    rng = random.Random(0)
    for _ in range(2000):
        num = rng.randint(0, 10**6)
        assert Solution().numberOfSteps(num) == number_of_steps_bits(num), num
    print("0..20,000 exhaustively and 2,000 random values up to 10^6: the loop and "
          "the binary formula always agree")

    # Note 1: the largest allowed input still takes only a few dozen steps.
    assert Solution().numberOfSteps(10**6) == 26 == 20 + 7 - 1   # 20 binary digits, seven 1s
    print("note 1 confirmed: 10^6 needs 26 steps, not a million, because halving is O(log num)")

    # Note 3: / gives a float, // keeps an int.
    assert 8 / 2 == 4.0 and isinstance(8 / 2, float)
    assert 8 // 2 == 4 and isinstance(8 // 2, int)
    print("note 3 confirmed: 8 / 2 is 4.0 (float), 8 // 2 is 4 (int)")
