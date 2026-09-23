# README file for data establishment information
## Summary
This dataset contains business-level listings for sit-down restaurants drawn from the Yelp Open Dataset, including each restaurant's name, location, aggregate star rating, and number of reviews. Fast food, cafe, and bar establishments have been excluded to match the project's narrowed focus on sit-down dining experiences. The two files are too large to put on GitHub, and therefore live in our team's shared OneDrive and are derived from Yelp's official Open Dataset, available at business.yelp.com/data/resources/open-dataset, titled business.json and review.json. The review text is joined with business data by the business_id. 
## Provenance
Yelp collects ratings and reviews directly from users as part of normal platform activity, then periodically releases a snapshot of business and review data as the Yelp Open Dataset for research and educational use. This working file is a filtered subset of that snapshot: non-restaurant businesses were removed, and the data was further narrowed to exclude fast food establishments and drop the restaurant_type column, aligning the dataset with the project's refined scope of sit-down restaurants only. 
The data originated from the Yelp Open Dataset. However, we cleaned and filtered the data through several steps to create the dataset used for our analysis. First, we examined the business categories and used relevant keywords to identify businesses that could potentially be food or restaurant related. We then filtered the businesses based on these categories and removed businesses that were clearly unrelated to food service. Next, we created a classification system to separate the remaining businesses into categories such as Sit-Down, Bar, Cafe, and Fast Food based on their Yelp category information. We then selected the businesses classified as sit-down restaurants for the primary analysis. After establishing the sit-down restaurant subset, we matched the selected businesses to their corresponding reviews using the unique business_id identifier. We then removed duplicate business records and reviews where applicable and retained the review text, overall Yelp star rating, business information, and other variables relevant to our analysis. Finally, the resulting reviews were stored as a single JSON file that we share as a single OneDrive file.
## License
Yelp permits use and modification of the dataset for non-commercial educational data science purposes but prohibits redistribution or transfer of the data.
## Ethical Statement
The Yelp Open Dataset contains publicly available, user-generated reviews, but the text may reflect subjective opinions, demographic differences, cultural expectations, and other biases in who chooses to leave reviews. We will not use user-identifying information as model features and will focus on restaurant-level rather than individual-level conclusions. We will also acknowledge that Yelp reviewers may not be representative of all restaurant customers. 
## Data Dictionary

| Variable | Type | Description | Uncertainties
| -------- | -------- | -------- |
| review_id | string | Identifier for each Yelp review | Treat as an identifier rather than a numeric value. |
| user_id | string | Unique identifier for the Yelp user who wrote the review | Identifies the reviewer but does not provide demographic information. Multiple reviews may come from the same user. |

## Exploratory Plots 
