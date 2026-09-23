# Details for Retrieving and using data
Our original data set is too large but this readme file describes how to obtain the data and steps for preprocessing to obtain the sitdown_reviews.csv set.

1. Go to https://business.yelp.com/data/resources/open-dataset/
2. Download JSON
3. Unzip the File: this contains a review.json file (review text) and business.json file (business_level listings)
4. Within the scripts folder of this repository, use (1) Business ID Preprocessing and (2) Review Text Preprocessing to filter only for sitdown restaurants.
5. Use (4) Cut down the data set script to cut the data set using random selection.
6. End result: sitdown_review.csv containing 32000 rows. 
