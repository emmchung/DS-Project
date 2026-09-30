# This is a script used to merge the two data sets together after using the preprocessing scripts.  
# the input to this file is yelp_academic_review.json and obtained form the yelp open data set and restaurants_sitdown_only.csv obtained from the 03_preprocessing_2.py. 
 
 
import json 
import pandas as pd 
 
# Define the file paths for the Yelp review data, filtered sit-down restaurant data, and output file.
reviews = "Data\Yelp-JSON\yelp_academic_review.json" 
businesses = "Data\Yelp-JSON\restaurants_sitdown_only.csv" 
output = "Data\Yelp-JSON\sitdown_reviews_joined2.csv" 
 
# Open the review JSON file and read the first review to identify the columns contained in the review data.
with open(reviews, "r", encoding="utf-8") as f: 
    first_review = json.loads(f.readline()) 
 
# Print the column names contained in the review data.
print("All Review Columns:") 
 
# Print each review column with a numbered label to make the structure of the review data easier to inspect.
for i, column in enumerate(first_review.keys(), start=1): 
    print(f"{i}. {column}") 
 
# Print the total number of columns in the review data.
print("Number of columns:", len(first_review)) 
 
# Read the filtered sit-down restaurant CSV file into a pandas DataFrame.
businesses = pd.read_csv(businesses) 
 
# Print the column names contained in the restaurant data.
print("Business columns:") 
print(businesses.columns.tolist()) 
 
# Print the first few rows of the restaurant data to verify that it was loaded correctly.
print("First few businesses:") 
print(businesses.head()) 
 
# Select the restaurant information needed to add to each review and rename the restaurant star rating column to distinguish it from the review star rating.
restaurants = (businesses[ 
    ["business_id","name", "city", "state", "stars"] 
].rename(columns={"stars": "restaurant_stars"})) 
 
# Print the first few rows of the selected restaurant information.
print("Restaurant Data:") 
print(restaurants.head()) 
 
# Convert business IDs to strings and remove any leading or trailing spaces to ensure they can be matched consistently with review business IDs.
restaurants["business_id"] = ( 
    restaurants["business_id"] 
    .astype(str) 
    .str.strip() 
) 
 
# Count the number of duplicate business IDs in the restaurant dataset.
duplicate_count = restaurants["business_id"].duplicated().sum() 
 
# Print the number of duplicate business IDs found.
print("Duplicate business IDs:", duplicate_count) 
 
# If duplicate business IDs exist, identify and inspect the duplicated IDs.
if duplicate_count > 0: 
 
    # Find all rows containing a business ID that appears more than once and extract the duplicated IDs.
    duplicate_ids = restaurants.loc[ 
        restaurants["business_id"].duplicated(keep=False), 
        "business_id"] 
 
    # Print the number of unique business IDs that appear more than once.
    print("Number of unique duplicate IDs:",duplicate_ids.nunique()) 
 
# Remove duplicate business IDs while keeping the first occurrence of each business.
restaurants = restaurants.drop_duplicates( 
    subset="business_id", 
    keep="first") 
 
 
# Convert the restaurant DataFrame into a dictionary where each business ID is used as the key.
# This allows restaurant information to be quickly matched to reviews using the business ID.
restaurant_info = ( 
    restaurants 
    .set_index("business_id") 
    .to_dict("index")) 
 
 
# Open the review JSON file for reading and create the output CSV file for writing the joined data.
with open(reviews, "r", encoding="utf-8") as infile, \ 
     open(output, "w", encoding="utf-8", newline="") as outfile: 
 
    # Track whether the current row is the first row so the CSV header is only written once.
    first_row = True 

    # Initialize a counter for the number of reviews successfully matched with restaurant information.
    joined = 0 

    # Initialize a counter for the total number of reviews processed.
    processed = 0 
 
    # Process the review JSON file one line at a time rather than loading the entire file into memory.
    for line in infile: 
 
        # Convert the current JSON line into a Python dictionary containing the review information.
        review = json.loads(line) 
 
        # Increase the total number of processed reviews by one.
        processed += 1 
 
        # Extract the business ID from the current review, convert it to a string, and remove extra spaces.
        business_id = str( 
            review["business_id"] 
        ).strip() 
 
        # Check whether the review's business ID belongs to one of the filtered sit-down restaurants.
        if business_id in restaurant_info: 
 
            # Add the corresponding restaurant information to the review dictionary.
            review.update( 
                restaurant_info[business_id] 
            ) 
 
            # Convert the updated review dictionary into a one-row pandas DataFrame so it can be written to the CSV file.
            row = pd.DataFrame([review]) 
 
            # Write the review and restaurant information to the output CSV file.
            # The header is only included for the first joined review.
            row.to_csv( 
                outfile, 
                index=False, 
                header=first_row 
            ) 
 
            # Set first_row to False so subsequent rows do not repeat the CSV header.
            first_row = False 
 
            # Increase the count of reviews successfully matched with a sit-down restaurant.
            joined += 1 
 
        # Print progress every 100,000 reviews processed.
        if processed % 100000 == 0: 
 
            print( 
                f"Processed: {processed:,} | " 
                f"Joined: {joined:,}") 
 
 
# Print the total number of reviews processed from the original review dataset.
print(f"Reviews processed: {processed:,}") 

# Print the total number of reviews successfully matched with sit-down restaurant information.
print(f"Reviews joined:    {joined:,}") 
 
# Print the location of the final joined dataset.
print("Output file:") 
print(output)
