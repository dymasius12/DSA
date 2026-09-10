import random
import pytest
from problems.m01_arrays_hashing.arrays_hashing import (
    contains_duplicate, is_anagram, two_sum, group_anagrams,
    top_k_frequent, product_except_self, longest_consecutive, is_valid_sudoku,
    encode, decode,
)


def norm_groups(groups):
    """Group order and within-group order don't matter."""
    return sorted(sorted(g) for g in groups)


class TestContainsDuplicate:
    def test_has(self):
        assert contains_duplicate([1, 2, 3, 1]) is True

    def test_not(self):
        assert contains_duplicate([1, 2, 3, 4]) is False

    def test_empty(self):
        assert contains_duplicate([]) is False

    def test_negatives(self):
        assert contains_duplicate([-1, -1]) is True

    def test_perf(self):
        assert contains_duplicate(list(range(200_000))) is False


class TestIsAnagram:
    def test_true(self):
        assert is_anagram("anagram", "nagaram") is True

    def test_false(self):
        assert is_anagram("rat", "car") is False

    def test_different_lengths(self):
        assert is_anagram("a", "ab") is False

    def test_both_empty(self):
        assert is_anagram("", "") is True

    def test_same_letters_different_counts(self):
        assert is_anagram("aacc", "ccac") is False


class TestTwoSum:
    def test_basic(self):
        assert two_sum([2, 7, 11, 15], 9) == [0, 1]

    def test_not_adjacent(self):
        assert two_sum([3, 2, 4], 6) == [1, 2]

    def test_same_value_twice(self):
        # The classic bug: an element pairing with itself.
        assert two_sum([3, 3], 6) == [0, 1]

    def test_negatives(self):
        assert two_sum([-3, 4, 3, 90], 0) == [0, 2]

    def test_perf(self):
        n = 100_000
        nums = list(range(n))
        assert two_sum(nums, (n - 1) + (n - 2)) == [n - 2, n - 1]


class TestGroupAnagrams:
    def test_basic(self):
        got = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        assert norm_groups(got) == norm_groups(
            [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]])

    def test_empty_list(self):
        assert group_anagrams([]) == []

    def test_empty_string(self):
        assert norm_groups(group_anagrams([""])) == [[""]]

    def test_no_anagrams(self):
        got = group_anagrams(["a", "b"])
        assert norm_groups(got) == [["a"], ["b"]]


class TestTopKFrequent:
    def test_basic(self):
        assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]

    def test_k_is_one(self):
        assert top_k_frequent([1], 1) == [1]

    def test_all_distinct(self):
        got = top_k_frequent([5, 6, 7], 3)
        assert sorted(got) == [5, 6, 7]

    def test_k_equals_distinct_count(self):
        assert sorted(top_k_frequent([1, 1, 2], 2)) == [1, 2]

    def test_perf(self):
        nums = [i % 500 for i in range(200_000)]
        assert len(top_k_frequent(nums, 10)) == 10


class TestProductExceptSelf:
    def test_basic(self):
        assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]

    def test_with_one_zero(self):
        assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]

    def test_with_two_zeros(self):
        assert product_except_self([0, 0, 2]) == [0, 0, 0]

    def test_two_elements(self):
        assert product_except_self([2, 3]) == [3, 2]

    def test_negatives(self):
        assert product_except_self([-1, -2, -3]) == [6, 3, 2]


class TestLongestConsecutive:
    def test_basic(self):
        assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4

    def test_empty(self):
        assert longest_consecutive([]) == 0

    def test_duplicates(self):
        assert longest_consecutive([1, 2, 0, 1]) == 3

    def test_single(self):
        assert longest_consecutive([7]) == 1

    def test_negatives_spanning_zero(self):
        assert longest_consecutive([-2, -1, 0, 1]) == 4

    def test_perf_must_be_linear(self):
        # One run of 100k. A solution missing the `n-1 not in set` guard
        # degrades to O(n^2) here and will hang.
        nums = list(range(100_000))
        random.Random(0).shuffle(nums)
        assert longest_consecutive(nums) == 100_000


class TestEncodeDecode:
    """The only contract that matters: decode(encode(x)) == x, for ANY x."""

    @pytest.mark.parametrize("strs", [
        ["neet", "code", "love", "you"],
        [],
        [""],
        ["", ""],
        ["a"],
        ["a#b"],                    # the delimiter appears INSIDE a string
        ["#", "##", "###"],
        ["12#34"],                  # looks like a length prefix
        ["3#abc"],                  # looks like an entire encoded string
        ["hello world", " ", "\n"],
        ["x" * 500, "y"],           # multi-digit length
    ])
    def test_roundtrip(self, strs):
        assert decode(encode(strs)) == strs

    def test_encode_returns_a_string(self):
        assert isinstance(encode(["a", "b"]), str)

    def test_decode_empty(self):
        assert decode("") == []


def make_board(rows):
    return [list(r) for r in rows]


VALID = make_board([
    "53..7....", "6..195...", ".98....6.",
    "8...6...3", "4..8.3..1", "7...2...6",
    ".6....28.", "...419..5", "....8..79",
])


class TestValidSudoku:
    def test_valid(self):
        assert is_valid_sudoku([row[:] for row in VALID]) is True

    def test_empty_board(self):
        assert is_valid_sudoku([['.'] * 9 for _ in range(9)]) is True

    def test_duplicate_in_row(self):
        b = [['.'] * 9 for _ in range(9)]
        b[0][0] = '5'
        b[0][8] = '5'
        assert is_valid_sudoku(b) is False

    def test_duplicate_in_column(self):
        b = [['.'] * 9 for _ in range(9)]
        b[0][3] = '9'
        b[7][3] = '9'
        assert is_valid_sudoku(b) is False

    def test_duplicate_in_box_only(self):
        # Different row, different column, same 3x3 box.
        b = [['.'] * 9 for _ in range(9)]
        b[3][3] = '1'
        b[4][4] = '1'
        assert is_valid_sudoku(b) is False
