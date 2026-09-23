# This is the script used to cut down the dataset into a usable, 25 mb size.
import pandas as pd
import os

input_file = r"C:\Users\bryso\Downloads\Yelp-JSON\sitdown_reviews_joined2.csv"
output_file = r"C:\Users\bryso\Downloads\Yelp-JSON\sitdown_reviews_25mb.csv"

rows = []
size = 0

for chunk in pd.read_csv(input_file, chunksize=8000):
    rows.append(chunk)
    size += chunk.memory_usage(deep=True).sum()

    if size >= 25 * 1024 * 1024:
        break
        
sample = pd.concat(rows, ignore_index=True)
sample.to_csv(output_file, index=False)

print("Done!")
print("Saved to:", output_file)
print("File size:", round(os.path.getsize(output_file) / (1024 * 1024), 2), "MB")
print("Number of rows:", len(sample))
