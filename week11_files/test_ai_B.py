import pytest

from load_scores import load_scores


def test_keeps_valid_scores_and_duplicate_names(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text("name,score\nAlice,0\nBob,100\nAlice,75\n", encoding="utf-8")

	assert load_scores(path) == (
		[("Alice", 0), ("Bob", 100), ("Alice", 75)],
		[],
	)


def test_header_only_returns_empty_lists(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text("name,score\n", encoding="utf-8")

	assert load_scores(path) == ([], [])


def test_skips_invalid_rows_with_line_number_original_and_reason(tmp_path):
	path = tmp_path / "scores.csv"
	rows = [
		"one-column",
		"too,many,columns",
		"missing-score,",
		"not-an-integer,abc",
		"below-range,-1",
		"above-range,101",
		",50",
	]
	path.write_text("name,score\n" + "\n".join(rows) + "\n", encoding="utf-8")

	kept, skipped = load_scores(path)

	assert kept == []
	assert [(number, original) for number, original, _ in skipped] == [
		(number, row) for number, row in enumerate(rows, start=2)
	]
	assert all(isinstance(reason, str) and reason for _, _, reason in skipped)


def test_blank_lines_are_ignored(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text("name,score\n\nAlice,42\n\n", encoding="utf-8")

	assert load_scores(path) == ([("Alice", 42)], [])


def test_missing_file_raises_file_not_found_error(tmp_path):
	with pytest.raises(FileNotFoundError):
		load_scores(tmp_path / "missing.csv")
