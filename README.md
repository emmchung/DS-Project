# DS-Project
## Contents
## Software and Platform Selection
### Software Types Used
- Visual Studio Code (VS Code)
- Python 3.12
- Git/GitHub
- Windows 11 / macOS 26.2 
### Add-on packages
Pandas, numpy, nltk, scikit-learn, matplotlib
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
    * 02_preprocessing.py
    * 03_preprocessing_2.py
    * 04_merge_reviews_business.py
    * 05_reduce_dataset.py
    * 06_load_data.py
    * 07_train_model.py

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

Note: The original data were obtained from the Yelp Open Dataset. Because the complete Yelp dataset is too large to store in this GitHub repository, the original Yelp JSON files must be downloaded separately to reproduce the full data acquisition process.

The following steps to reproduce this model from the original dataset can be found in /Data/DataRetrieval.md and are as follows: 
1. Go to https://business.yelp.com/data/resources/open-dataset/
2. Download JSON
3. Unzip the File: this contains a review.json file (review text) and business.json file (business_level listings)
4. Place these data files into this repository in the "Data" folder. **Note:** The path to these files should match the path in the scripts in the "Scripts" folder. 
5. Within the scripts folder of this repository, use (1) Business ID Preprocessing and (2) Review Text Preprocessing to filter only for sitdown restaurants.
6. Use (4) Cut down the data set script to cut the data set using random selection.
7. End result: sitdown_review.csv containing 32000 rows (this should be identical to the sitdown_reviews.csv in the Data folder in this repository)

The preprocessing scripts in the `Scripts` folder document the process used to transform the original Yelp data into the processed dataset used for analysis.

After preprocessing the original Yelp data, run the remaining preprocessing scripts in the order described in the repository map to produce the final analysis dataset.
