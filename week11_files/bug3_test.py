import pytest

from bug3_logic import count_pass, find_max


@pytest.mark.parametrize(
	("scores", "expected"),
	[
		([70, 85, 60, 95], 95),  # Maximum is the final item.
		([10, 30, 20], 30),
		([7], 7),
		([-8, -3, -5], -3),
	],
)
def test_find_max(scores, expected):
	assert find_max(scores) == expected


def test_find_max_empty_scores_raises_index_error():
	with pytest.raises(IndexError):
		find_max([])


@pytest.mark.parametrize(
	("scores", "cutoff", "expected"),
	[
		([70, 85, 60, 95], 60, 3),  # A score equal to the cutoff does not pass.
		([60, 61, 59], 60, 1),
		([1, 2, 3], 3, 0),
		([], 60, 0),
	],
)
def test_count_pass_with_cutoff(scores, cutoff, expected):
	assert count_pass(scores, cutoff) == expected


def test_count_pass_uses_default_cutoff():
	assert count_pass([59, 60, 61]) == 1
