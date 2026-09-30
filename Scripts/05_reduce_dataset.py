# This is the script used to cut down the dataset into a usable, 25 mb size.
# The input to this file is sitdown_reviews_joined2.csv obtained from 04_merge_reviews_business.py and the output is sitdown_reviews.csv, the final cut dataset used for modeling. 

import pandas as pd
import os

input_file = "Data\Yelp-JSON\sitdown_reviews_joined2.csv"
output_file = "Data\Users\bryso\Downloads\Yelp-JSON\sitdown_reviews.csv"

rows = []
size = 0

for chunk in pd.read_csv(input_file, chunksize=8000):
    rows.append(chunk)
    size += chunk.memory_usage(deep=True).sum()

    if size >= 25 * 1024 * 1024:
        break
        
sample = (pd.concat(rows, ignore_index=True).sample(n=32000, random_state=42).reset_index(drop=True))
sample.to_csv(output_file, index=False)

print("Done!")
print("Saved to:", output_file)
print("File size:", round(os.path.getsize(output_file) / (1024 * 1024), 2), "MB")
print("Number of rows:", len(sample))
