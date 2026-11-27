import pandas as pd


def 정제(df):
	df = df.copy()

	df = df.dropna(subset=["점수"])
	print(len(df))

	df = df.drop_duplicates()
	print(len(df))

	df["반"] = df["반"].str.strip()
	df["과목"] = df["과목"].str.strip()
	print(len(df))

	df["점수"] = pd.to_numeric(df["점수"], errors="coerce")
	valid = df["점수"].between(0, 100) & (df["점수"] % 1 == 0)
	df = df.loc[valid].copy()
	df["점수"] = df["점수"].astype(int)
	print(len(df))

	return df

df = pd.read_csv("scores_2026.csv")
print(sorted(정제(df)["반"].unique())) 
print(sorted(정제(df)["과목"].unique()))