import pytest

from load_scores import load_scores


def test_load_scores_keeps_valid_rows_and_records_invalid_rows(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text(
		"이름,점수\n"
		"  Alice  , 0 \n"
		"Bob,100\n"
		"\n"
		"Charlie,50\n"
		"한 열만\n"
		",80\n"
		"Dave,\n"
		"Eve,점수\n"
		"Frank,-1\n"
		"Grace,101\n"
		"Ivy,70,extra\n",
		encoding="utf-8-sig",
		newline="",
	)

	kept, skipped = load_scores(path)

	assert kept == [("Alice", 0), ("Bob", 100), ("Charlie", 50)]
	assert skipped == [
		(6, "한 열만", "열 개수가 2가 아님"),
		(7, ",80", "이름이 비어 있음"),
		(8, "Dave,", "점수가 비어 있음"),
		(9, "Eve,점수", "점수가 정수가 아님"),
		(10, "Frank,-1", "점수가 0~100 밖"),
		(11, "Grace,101", "점수가 0~100 밖"),
		(12, "Ivy,70,extra", "열 개수가 2가 아님"),
	]


def test_load_scores_header_only_returns_empty_lists(tmp_path):
	path = tmp_path / "scores.csv"
	path.write_text("이름,점수\n", encoding="utf-8")

	assert load_scores(path) == ([], [])


def test_load_scores_missing_file_raises_file_not_found_error(tmp_path):
	path = tmp_path / "missing.csv"

	with pytest.raises(FileNotFoundError):
		load_scores(path)
