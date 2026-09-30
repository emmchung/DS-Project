# This script is a secondary preprocessing script used to filter the data into only sit down restaurant types.
# The input of this file is restaurants.csv obtained from 02_preprocessing.py. The output is restaurants_sitdown_only.csv, which contains only reviews from the open data set that pertain to sitdown restaurants. 

import pandas as pd


# Define the location of the restaurant dataset created in the previous preprocessing script.
path = "Data\Yelp-JSON\restaurants.csv"

# Define the location and filename for the filtered sit-down restaurant dataset.
output = "Data\Yelp-JSON\restaurants_sitdown_only.csv"


# Read the restaurant CSV file into a pandas DataFrame.
restaurants = pd.read_csv(path)


# Print the total number of restaurants before applying the restaurant type filters.
print("Number of restaurants:", len(restaurants))


# Define categories that will be classified as bars and excluded from the sit-down restaurant dataset.
bars = [
    "Bars",
    "Beach Bars",
    "Beer Bar",
    "Champagne Bars",
    "Cigar Bars",
    "Cocktail Bars",
    "Dive Bars",
    "Drive-Thru Bars",
    "Gay Bars",
    "Hookah Bars",
    "Hotel bar",
    "Piano Bars",
    "Sports Bars",
    "Tiki Bars",
    "Vermouth Bars",
    "Whiskey Bars",
    "Wine Bars"
]


# Define categories that will be classified as cafes and excluded from the sit-down restaurant dataset.
cafes = [
    "Cafes",
    "Bubble Tea",
    "Coffee & Tea",
    "Coffeeshops",
    "Hong Kong Style Cafe",
    "Tea Rooms",
    "Themed Cafes"
]


# Define the fast food category separately because it is given the highest classification priority.
fast_food = [
    "Fast Food"
]


# Define categories that will be classified as sit-down restaurants and retained in the final dataset.
sit_down = [
    "Afghan",
    "African",
    "Barbeque",
    "Breakfast & Brunch",
    "Buffets",
    "Burgers",
    "Caribbean",
    "Cafeteria",
    "Cheesesteaks",
    "Chicken Shop",
    "Chicken Wings",
    "Chinese",
    "Comfort Food",
    "Delicatessen",
    "Delis",
    "Desserts",
    "French",
    "Greek",
    "Indian",
    "Italian",
    "Japanese",
    "Japanese Curry",
    "Korean",
    "Mediterranean",
    "Mexican",
    "New Mexican Cuisine",
    "Pizza",
    "Pop-Up Restaurants",
    "Restaurants",
    "Sandwiches",
    "Seafood",
    "Soul Food",
    "South African",
    "Steakhouses",
    "Sushi Bars",
    "Tacos",
    "Tapas Bars",
    "Thai",
    "Vietnamese",
    "Senegalese"
]


# Define a function to assign each restaurant to a restaurant type based on its Yelp categories.
def classify_restaurant(categories):

    # Classify restaurants with missing category information as "Other".
    if pd.isna(categories):
        return "Other"

    # Split the categories string into individual categories using commas as separators.
    categories = categories.split(",")

    # Remove extra spaces from the beginning and end of each category.
    categories = [x.strip() for x in categories]

    # Priority 1: Classify any restaurant with a Fast Food category as "Fast Food".
    # This category is checked first so that restaurants with multiple categories are classified consistently.
    if any(x in categories for x in fast_food):
        return "Fast Food"

    # Priority 2: Classify any restaurant with a bar category as "Bar".
    # This is checked before the sit-down category so that restaurants also categorized as bars are excluded.
    if any(x in categories for x in bars):
        return "Bar"

    # Priority 3: Classify any restaurant with a cafe category as "Cafe".
    # This prevents businesses with both restaurant and cafe categories from being classified as sit-down restaurants.
    if any(x in categories for x in cafes):
        return "Cafe"

    # Priority 4: Classify restaurants matching one of the sit-down categories as "Sit Down".
    if any(x in categories for x in sit_down):
        return "Sit Down"

    # Classify any business that does not match the categories above as "Other".
    return "Other"


# Apply the classify_restaurant function to the categories of every restaurant and store the result in a new column.
restaurants["restaurant_type"] = restaurants["categories"].apply(
    classify_restaurant
)


# Display the number of restaurants assigned to each restaurant type.
print("Restaurant types:")
print(restaurants["restaurant_type"].value_counts())


# Filter the dataset to keep only businesses classified as "Sit Down".
# .copy() creates a separate DataFrame containing only the selected restaurants.
sit_down_restaurants = restaurants[restaurants["restaurant_type"] == "Sit Down"].copy()


# Keep only the business information needed for the final sit-down restaurant dataset.
sit_down_restaurants = sit_down_restaurants[["business_id", "name", "city", "state", "stars", "categories"]]


# Save the sit-down restaurant information as a CSV file at the specified output location.
sit_down_restaurants.to_csv(output,index=False)


# Print the total number of restaurants remaining after filtering for sit-down restaurants.
print("Number of sit-down restaurants:", len(sit_down_restaurants))

# Confirm that the sit-down restaurant information has been saved.
print("Sit-down restaurant information saved.")


# Print the location where the final sit-down restaurant dataset was saved.
print(f"Files saved to:")
print(output)
