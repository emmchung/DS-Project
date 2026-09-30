import pandas as pd

path = r"C:\Users\bryso\Downloads\Yelp-JSON\restaurants.csv"
output = r"C:\Users\bryso\Downloads\Yelp-JSON\restaurants_sitdown_only.csv"

restaurants = pd.read_csv(path)

print("Number of restaurants:", len(restaurants))

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

cafes = [
    "Cafes",
    "Bubble Tea",
    "Coffee & Tea",
    "Coffeeshops",
    "Hong Kong Style Cafe",
    "Tea Rooms",
    "Themed Cafes"
]

fast_food = [
    "Fast Food"
]

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


def classify_restaurant(categories):

    if pd.isna(categories):
        return "Other"

    categories = categories.split(",")
    categories = [x.strip() for x in categories]

    # Priority 1: Fast Food
    if any(x in categories for x in fast_food):
        return "Fast Food"

    # Priority 2: Actual bars
    if any(x in categories for x in bars):
        return "Bar"

    # Priority 3: Cafes
    if any(x in categories for x in cafes):
        return "Cafe"

    # Priority 4: Sit-down restaurants
    if any(x in categories for x in sit_down):
        return "Sit Down"

    return "Other"

restaurants["restaurant_type"] = restaurants["categories"].apply(
    classify_restaurant
)

print("Restaurant types:")
print(restaurants["restaurant_type"].value_counts())

sit_down_restaurants = restaurants[restaurants["restaurant_type"] == "Sit Down"].copy()

sit_down_restaurants = sit_down_restaurants[["business_id", "name", "city", "state", "stars", "categories"]]

sit_down_restaurants.to_csv(output,index=False)

print("Number of sit-down restaurants:", len(sit_down_restaurants))
print("Sit-down restaurant information saved.")

print(f"Files saved to:")
print(output)
