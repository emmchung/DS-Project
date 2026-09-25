# This file is used to load the file into VS code
import pandas as pd

file_path = "Data/sitdown_reviews_25mb.csv"

df = pd.read_csv(file_path)

print("Rows:", len(df))
print("Columns:", list(df.columns))
print(df.head())
