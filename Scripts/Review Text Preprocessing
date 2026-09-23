import pandas as pd
import os


business= r"C:\Users\bryso\Downloads\Yelp-JSON\yelp_academic_dataset_business.json"
reviews = r"C:\Users\bryso\Downloads\Yelp-JSON\yelp_academic_dataset_review.json"
output = r"C:\Users\bryso\Downloads\Yelp-JSON\processed"

os.makedirs(output,exist_ok=True)

business = pd.read_json(business,lines=True)

print("Number of businesses:",len(business))

print("Identifying restaurants")

restaurants = business[
    business["categories"]
    .fillna("")
    .str.contains("Restaurants", case=False)
].copy()

print("Number of restaurants:", len(restaurants))

restaurants = restaurants[["business_id", "name", "stars", "categories"]]

restaurants.to_csv(os.path.join(output, "restaurants.csv"),index=False)

print("Restaurant information saved.")

restaurant_ids = set(restaurants["business_id"])

review_chunks = pd.read_json(reviews,lines=True,chunksize=100000)

chunk_number = 0
total_reviews_processed = 0
total_restaurant_reviews = 0

for reviews in review_chunks:

    total_reviews_processed += len(reviews)

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
