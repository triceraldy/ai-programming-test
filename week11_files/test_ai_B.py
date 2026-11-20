import pytest

from ai_B import load_scores


def test_load_scores_keeps_valid_rows_and_duplicate_names(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"name,score\n"
		"Alice,0\n"
		"Bob,100\n"
		"Alice,75\n",
		encoding="utf-8",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Alice", 0), ("Bob", 100), ("Alice", 75)]
	assert skipped == []


def test_load_scores_skips_invalid_rows_and_ignores_blank_lines(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"name,score\n"
		"Valid,50\n"
		"\n"
		"Too,Many,Columns\n"
		"OnlyOneColumn\n"
		"BlankScore,\n"
		"NotInteger,abc\n"
		"TooLow,-1\n"
		"TooHigh,101\n"
		",80\n",
		encoding="utf-8",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Valid", 50)]
	assert [line_number for line_number, _, _ in skipped] == [4, 5, 6, 7, 8, 9, 10]
	assert [line.strip() for _, line, _ in skipped] == [
		"Too,Many,Columns",
		"OnlyOneColumn",
		"BlankScore,",
		"NotInteger,abc",
		"TooLow,-1",
		"TooHigh,101",
		",80",
	]
	assert all(reason for _, _, reason in skipped)


def test_load_scores_header_only_returns_empty_lists(tmp_path):
	path = tmp_path / "header_only.csv"
	path.write_text("name,score\n", encoding="utf-8")

	assert load_scores(path) == ([], [])


def test_load_scores_missing_file_raises_file_not_found_error(tmp_path):
	path = tmp_path / "missing.csv"

	with pytest.raises(FileNotFoundError):
		load_scores(path)
