import pandas as pd
df = pd.read_csv("scores_2026.csv")

print(df.shape) # (114, 5)
print(df["점수"].isna().sum()) # 6 ← 빈 칸이 몇 개인가
print(df.duplicated().sum()) # 4 ← 완전히 같은 행이 몇 개인가
print(df["반"].unique()) # ['2반' '1반' '1반 '] ← 세 개?
print(df["과목"].unique()) # ['수학' '프로그래밍' '영어' '프로그래밍 ']
print(df["점수"].describe()) 