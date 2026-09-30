# This is the script used to cut down the dataset into a usable, 25 mb size.
# The input to this file is sitdown_reviews_joined2.csv obtained from 04_merge_reviews_business.py and the output is sitdown_reviews.csv, the final cut dataset used for modeling. 

import pandas as pd
import os

# Define the location of the full joined sit-down restaurant review dataset.
input_file = "Data\Yelp-JSON\sitdown_reviews_joined2.csv"

# Define the location where the final smaller dataset will be saved.
output_file = "Data\Users\bryso\Downloads\Yelp-JSON\sitdown_reviews.csv"

# Create an empty list to store the chunks of data that will be used for the final sample.
rows = []

# Initialize a variable to keep track of the approximate amount of data loaded into memory.
size = 0

# Read the large joined dataset in chunks of 8,000 rows at a time to avoid loading the entire file into memory.
for chunk in pd.read_csv(input_file, chunksize=8000):

    # Add the current chunk to the list of data that will be combined into the final sample.
    rows.append(chunk)

    # Calculate the memory usage of the current chunk and add it to the running total.
    size += chunk.memory_usage(deep=True).sum()

    # Stop reading additional chunks once the accumulated data reaches approximately 25 MB.
    if size >= 25 * 1024 * 1024:
        break
        
# Combine the collected chunks into one DataFrame, randomly select 32,000 reviews, and reset the row index.
# random_state=42 ensures that the same 32,000 reviews are selected each time the script is run.
sample = (pd.concat(rows, ignore_index=True).sample(n=32000, random_state=42).reset_index(drop=True))

# Save the final 32,000-row sample as a CSV file without including the DataFrame index.
sample.to_csv(output_file, index=False)

# Confirm that the dataset creation process is complete.
print("Done!")

# Print the location where the final dataset was saved.
print("Saved to:", output_file)

# Calculate and print the final CSV file size in megabytes.
print("File size:", round(os.path.getsize(output_file) / (1024 * 1024), 2), "MB")

# Print the total number of rows in the final dataset.
print("Number of rows:", len(sample))
