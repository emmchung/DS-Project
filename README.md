# DS-Project
## Contents
## Software and Platform Selection
### Software Types Used
- Visual Studio Code (VS Code)
- Python 3.12
- Git/GitHub
### Add-on packages
Pandas, numpy, nltk, scikit-learn, matplotlib, job lib
### Platform used
Visual Studio Code (VS Code) with Python 3.12 and the VS Code integrated terminal
## Map of Documentation
* DS Project Repository
  * README.md
  * Data: Initial & Final data sets
    * DataRetrieval.md
    * README.md
    * sitdown_reviews.csv: raw data file
  * Scripts : contains all source code for the project. 
    * 01_data_extraction.py
    * 02_load_data.py
    * 03_preprocessing.py
    * 04_merge_reviews_business.py
    * 05_reduce_dataset.py
    * 06_train_model.py
  * License
  * MODEL_OUTPUT
    * aspect_regression_coefficients.png
    * aspect_regression_predicted_vs_actual.png
    * aspect_results_summary.csv
    * aspect_sentiment_by_star.png
    * convenience_sentiment_vs_stars.png
    * output.txt
    * price_sentiment_vs_stars.png
    * quality_sentiment_vs_stars.png
  * References
## Instructions for Reproducing results
### Software and Environment
- Python 3.12
- Visual Studio Code (VS Code)
- Required Python packages: pandas, nltk, scikit-learn, matplotlib, joblib

Install the required packages by running:

pip install pandas nltk scikit-learn matplotlib joblib

### Option 1: Reproduce the Final Analysis

The processed dataset required for the final analysis is provided in the `Data` folder. Therefore, users do not need to download and preprocess the complete Yelp Open Dataset to reproduce the final results.

1. Clone or download this GitHub repository and open the project folder in Visual Studio Code.

2. Confirm that `sitdown_reviews.csv` is located in the `Data` folder.

3. Install the required Python packages using the command above.

4. Run the final modeling script from the project directory:

python3 "Scripts/05_train_model.py"

5. The modeling script will:
   - Load and clean the processed Yelp review data.
   - Identify review text related to quality, price, and convenience.
   - Calculate VADER sentiment scores for the three aspects.
   - Perform the project's regression analysis.
   - Evaluate model performance.
   - Generate figures and summary files.

6. Generated results and figures will be saved in the `MODEL_OUTPUT` folder.

### Option 2: Reproduce Data Acquisition and Preprocessing

The original data were obtained from the Yelp Open Dataset. Because the complete Yelp dataset is too large to store in this GitHub repository, the original Yelp JSON files must be downloaded separately to reproduce the full data acquisition process.

The preprocessing scripts in the `Scripts` folder document the process used to transform the original Yelp data into the processed dataset used for analysis.

The initial restaurant extraction script:
- Loads the Yelp business and review JSON files.
- Identifies businesses categorized as restaurants.
- Extracts their business IDs and restaurant information.
- Processes the large review dataset in chunks of 100,000 reviews.
- Retains reviews associated with restaurant business IDs.
- Saves the resulting restaurant data and review chunks as CSV files.

The file paths in the original preprocessing script reflect the local computer used during data acquisition. To rerun this script, users must update the `business`, `reviews`, and `output` paths at the beginning of the script to match the locations of the Yelp files on their own computer.

After preprocessing the original Yelp data, run the remaining preprocessing scripts in the order described in the repository map to produce the final analysis dataset.
