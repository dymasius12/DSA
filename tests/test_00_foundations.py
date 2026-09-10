import pytest
from problems.m00_foundations.warmups import (
    char_frequency, has_duplicate, group_by_first_letter, make_grid,
)


class TestCharFrequency:
    def test_basic(self):
        assert char_frequency("aabc") == {'a': 2, 'b': 1, 'c': 1}

    def test_empty(self):
        assert char_frequency("") == {}

    def test_single(self):
        assert char_frequency("z") == {'z': 1}

    def test_spaces_and_case_are_distinct(self):
        assert char_frequency("a A") == {'a': 1, ' ': 1, 'A': 1}


class TestHasDuplicate:
    def test_has_one(self):
        assert has_duplicate([1, 2, 3, 1]) is True

    def test_none(self):
        assert has_duplicate([1, 2, 3]) is False

    def test_empty(self):
        assert has_duplicate([]) is False

    def test_all_same(self):
        assert has_duplicate([7, 7]) is True

    def test_large_input_must_not_be_quadratic(self):
        # 200k distinct values. An O(n^2) solution will not finish.
        assert has_duplicate(list(range(200_000))) is False


class TestGroupByFirstLetter:
    def test_basic(self):
        assert group_by_first_letter(["apple", "ant", "bee"]) == {
            'a': ["apple", "ant"], 'b': ["bee"],
        }

    def test_empty(self):
        assert group_by_first_letter([]) == {}

    def test_order_preserved_within_group(self):
        assert group_by_first_letter(["cat", "cow", "car"])['c'] == ["cat", "cow", "car"]


class TestMakeGrid:
    def test_shape_and_fill(self):
        assert make_grid(2, 3) == [[0, 0, 0], [0, 0, 0]]

    def test_custom_fill(self):
        assert make_grid(1, 2, 9) == [[9, 9]]

    def test_rows_are_independent(self):
        # This is the whole point of the exercise.
        g = make_grid(3, 3)
        g[0][0] = 5
        assert g[1][0] == 0, "rows share the same list — use a comprehension"
        assert g[2][0] == 0

    def test_zero_rows(self):
        assert make_grid(0, 5) == []
