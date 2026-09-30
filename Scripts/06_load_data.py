# This file is used to load the sitdown_reviews.csv file into VS code. 
import pandas as pd

# Define the location of the final sit-down restaurant review dataset.
file_path = "Data/sitdown_reviews.csv"

# Read the CSV file into a pandas DataFrame.
df = pd.read_csv(file_path)

# Print the total number of rows in the dataset.
print("Rows:", len(df))

# Print the names of all columns in the dataset.
print("Columns:", list(df.columns))

# Display the first five rows of the dataset to verify that the data was loaded correctly.
print(df.head())
