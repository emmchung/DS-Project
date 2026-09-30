# This is a script to preprocess the data file obtained from [Reference 3: https://business.yelp.com/data/resources/open-dataset/] Yelp open dataset: review.json and business.json.
# The input to this script is the bundled Yelp-JSON file obtained from running 01_data_extraction.py. The output of this file is restaurants.csv which is used in the following script 03_preprocessing_2.py

import pandas as pd
import os


# Define the file paths for the Yelp business and review JSON files.
business= "Data\Yelp-JSON\yelp_academic_dataset_business.json"
reviews = "Data\Yelp-JSON\yelp_academic_dataset_review.json"

# Define the folder where the processed restaurant data and review files will be saved.
output = "Data\Yelp-JSON\processed"


# Create the output folder if it does not already exist. exist_ok=True prevents an error if the folder already exists.
os.makedirs(output,exist_ok=True)


# Read the Yelp business JSON file into a pandas DataFrame.
# lines=True indicates that each line of the JSON file represents a separate JSON object (one business).
business = pd.read_json(business,lines=True)


# Print the total number of businesses in the original business dataset.
print("Number of businesses:",len(business))


# Indicate that the script is beginning the process of identifying which businesses are restaurants.
print("Identifying restaurants")


# Filter the business dataset to keep only businesses whose category information contains the word "Restaurants."
# fillna("") replaces missing category values with an empty string so that missing values do not cause an error during the text search.
# str.contains() searches the categories column for "Restaurants."
# case=False means the search is not sensitive to capitalization.
# .copy() creates a separate DataFrame containing the restaurant records.

restaurants = business[
    business["categories"]
    .fillna("")
    .str.contains("Restaurants", case=False)
].copy()


# Print the total number of businesses identified as restaurants.
print("Number of restaurants:", len(restaurants))


# Keep only the business information needed for the restaurant dataset: business ID, name, city, state, star rating, and categories.
restaurants = restaurants[["business_id", "name", "city", "state", "stars", "categories"]]


# Save the restaurant information as a CSV file in the processed folder.
# index=False prevents pandas from adding the DataFrame index as an additional column in the CSV file.
restaurants.to_csv(os.path.join(output, "restaurants.csv"),index=False)


# Confirm that the restaurant information has been saved.
print("Restaurant information saved.")


# Create a set containing the unique business IDs for all identified restaurants.
# This set will be used to efficiently identify restaurant reviews in the much larger review dataset.
restaurant_ids = set(restaurants["business_id"])


# Read the review JSON file in chunks of 100,000 reviews at a time.
# Processing the file in chunks prevents the entire large review dataset from needing to be loaded into memory at once.
review_chunks = pd.read_json(reviews,lines=True,chunksize=100000)


# Initialize counters to keep track of the number of chunks processed, total reviews processed, and total restaurant reviews identified.
chunk_number = 0
total_reviews_processed = 0
total_restaurant_reviews = 0


# Process each 100,000-review chunk from the review dataset.
for reviews in review_chunks:

    # Add the number of reviews in the current chunk to the running total of reviews processed.
    total_reviews_processed += len(reviews)


    # Filter the current review chunk to keep only reviews whose business_id belongs to one of the identified restaurants.
    restaurant_reviews = reviews[reviews["business_id"].isin(restaurant_ids)].copy()


    # Add the number of restaurant reviews found in this chunk to the running total of restaurant reviews.
    total_restaurant_reviews += len(restaurant_reviews)


    # Only create and save a file if the current chunk contains at least one restaurant review.
    if len(restaurant_reviews) > 0:

        # Create a unique file path for the current restaurant review chunk.
        # The chunk number is included in the filename so that each chunk can be saved as a separate CSV file.
        output_path = os.path.join(output, f"reviews_chunk_{chunk_number}.csv")


        # Save the restaurant reviews from the current chunk as a CSV file.
        # index=False prevents pandas from adding the DataFrame index as an extra column.
        restaurant_reviews.to_csv(output_path,index=False)


        # Print the number of restaurant reviews saved from the current chunk.
        print(f"Saved {len(restaurant_reviews):,} restaurant reviews.")


    # Print the running total number of reviews processed so far.
    print(f"Total reviews processed: "f"{total_reviews_processed:,}")


    # Increase the chunk counter by one before moving to the next group of reviews.
    chunk_number += 1


# After all review chunks have been processed, print the total number of review chunks that were examined.
print(f"Total chunks: {chunk_number:,}")

# Print the total number of reviews processed across all chunks.
print(f"Total reviews processed: {total_reviews_processed:,}")

# Print the total number of reviews that were associated with identified restaurant businesses.
print(f"Total restaurant reviews: {total_restaurant_reviews:,}")


# Print the location where the processed restaurant information and review files were saved.
print(f"Files saved to:")
print(output)

    restaurant_reviews = reviews[reviews["business_id"].isin(restaurant_ids)].copy()

    total_restaurant_reviews += len(restaurant_reviews)

    if len(restaurant_reviews) > 0:

        output_path = os.path.join(output, f"reviews_chunk_{chunk_number}.csv")

        restaurant_reviews.to_csv(output_path,index=False)

        print(f"Saved {len(restaurant_reviews):,} restaurant reviews.")

    print(f"Total reviews processed: "f"{total_reviews_processed:,}")

    chunk_number += 1

print(f"Total chunks: {chunk_number:,}")
print(f"Total reviews processed: {total_reviews_processed:,}")
print(f"Total restaurant reviews: {total_restaurant_reviews:,}")

print(f"Files saved to:")
print(output)
