import pytest

from ai_A import load_scores


def test_load_scores_keeps_valid_rows_and_ignores_header_and_blank_lines(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"name,score\n Alice , 85 \n\nBob,0\nCarol,100\n",
		encoding="utf-8-sig",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Alice", 85), ("Bob", 0), ("Carol", 100)]
	assert skipped == []


def test_load_scores_records_invalid_rows_with_line_number_original_and_reason(tmp_path):
	path = tmp_path / "invalid.csv"
	path.write_text(
		"name,score\n"
		"OnlyOneColumn\n"
		",75\n"
		"NoScore,\n"
		"NotAnInt,abc\n"
		"Fraction,1.5\n"
		"TooLow,-1\n"
		"TooHigh,101\n"
		"Too,Many,Columns\n",
		encoding="utf-8",
	)

	kept, skipped = load_scores(path)

	assert kept == []
	assert skipped == [
		(2, "OnlyOneColumn", "열 개수가 2가 아님"),
		(3, ",75", "이름이 비어 있음"),
		(4, "NoScore,", "점수가 비어 있음"),
		(5, "NotAnInt,abc", "점수가 정수가 아님"),
		(6, "Fraction,1.5", "점수가 정수가 아님"),
		(7, "TooLow,-1", "점수가 0~100 밖"),
		(8, "TooHigh,101", "점수가 0~100 밖"),
		(9, "Too,Many,Columns", "열 개수가 2가 아님"),
	]


def test_load_scores_missing_file_raises_file_not_found_error(tmp_path):
	with pytest.raises(FileNotFoundError):
		load_scores(tmp_path / "missing.csv")