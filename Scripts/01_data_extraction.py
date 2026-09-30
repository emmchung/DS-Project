# This is the initial restaurant extraction script. It is the first step in creating the smaller Yelp dataset used for our analysis.
# obtained from "" into a usable file for preprocessing --> merging --> modeling. 
#
# NOTE: This script is to be used ONLY if obtaining the dataset from the "https://business.yelp.com/data/resources/open-dataset/" website, 
# instead of using the established "sitdown_reviews.csv" found in the Data folder of this repository. 


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
