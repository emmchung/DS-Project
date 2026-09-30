# This is the initial restaurant extraction script. It performs the following actions to get to the cut dataset of 32000 rows from the original Yelp Open Dataset. 
# 1. Loads the Yelp business and review JSON files.
# 2. Identifies businesses categorized as restaurants.
# 3. Extracts their business IDs and restaurant information.
# 4. Processes the large review dataset in chunks of 100,000 reviews.
# 5. Retains reviews associated with restaurant business IDs.
# 6. Saves the resulting restaurant data and review chunks as CSV files in Yelp-JSON file.


import tarfile
import os

tar_path = r"C:\Users\bryso\Downloads\Yelp-Json.tar"
extract_to = r"C:\Users\bryso\Downloads\Yelp-JSON"

os.makedirs(extract_to, exist_ok=True)

with tarfile.open(tar_path, "r") as tar:
    tar.extractall(path=extract_to)

print("Extracted to:", extract_to)
