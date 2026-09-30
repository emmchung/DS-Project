# This is the initial restaurant extraction script. It performs the following actions to get to the cut dataset of 32000 rows from the original Yelp Open Dataset. 
# 1. Loads the Yelp business and review JSON files.
# 2. Identifies businesses categorized as restaurants.
# 3. Extracts their business IDs and restaurant information.
# 4. Processes the large review dataset in chunks of 100,000 reviews.
# 5. Retains reviews associated with restaurant business IDs.
# 6. Saves the resulting restaurant data and review chunks as CSV files bundled into one file named Yelp-JSON.


import tarfile
import os

tar_path = "Data\Yelp-Json.tar"
extract_to = "Data\Yelp-JSON"

os.makedirs(extract_to, exist_ok=True)

with tarfile.open(tar_path, "r") as tar:
    tar.extractall(path=extract_to)

print("Extracted to:", extract_to)

# This is the initial restaurant extraction script. It is the first step in creating the smaller Yelp dataset used for our analysis.
#
# The overall extraction process is intended to:
# 1. Load the Yelp business and review JSON files.
# 2. Identify businesses categorized as restaurants.
# 3. Extract the business IDs and restaurant information.
# 4. Process the large review dataset in chunks of 100,000 reviews.
# 5. Keep only reviews associated with restaurant business IDs.
# 6. Save the resulting restaurant data and review chunks as CSV files.
#
# The goal is to reduce the original Yelp Open Dataset to a more manageable dataset of approximately 32,000 restaurant reviews for our analysis.


# Import tarfile so that we can work with the .tar archive containing  the original Yelp JSON dataset.
import tarfile

# Import os so that we can create the folder where the extracted files will be stored.
import os


# Path to the original compressed Yelp dataset.
# The dataset is stored as a .tar archive inside the Data folder.
tar_path = "Data\Yelp-Json.tar"

# Folder where the contents of the Yelp .tar archive will be extracted.
extract_to = "Data\Yelp-JSON"


# Create the output folder if it does not already exist.
# exist_ok=True prevents an error if the folder has already been created.
os.makedirs(extract_to, exist_ok=True)


# Open the Yelp .tar archive in read mode ("r").
# The "with" statement automatically closes the archive after extraction is complete.
with tarfile.open(tar_path, "r") as tar:
    
    # Extract all files contained in the archive into the specified folder.
    tar.extractall(path=extract_to)


# Print the location of the extracted files so we can confirm where the Yelp dataset was saved.
print("Extracted to:", extract_to)
