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
    * Business ID Preprocessing
    * Merge Reviews and Business Data Script
    * Cut down the data set
    * Load Data
    * Review Text Preprocessing
    * Train Modeling
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
Platform: Visual Studio Code (VS Code)
Programming Language: Python 3.12
Steps to reproduce the analysis:
1. Clone or download this GitHub repository and open the project folder in Visual Studio Code.
2. Confirm that the Yelp review dataset is located in the Data folder.
3. Install the required Python packages by running the following command in the VS Code terminal:
pip install pandas numpy nltk scikit-learn matplotlib joblib
4. Run the modeling script from the project directory:
python3 "Scripts/06_train_model.py"
5. The script will reproduce the analysis by:
- Loading and cleaning the Yelp review data.
- Identifying review sentences related to quality, price, and convenience.
- Calculating VADER sentiment scores for each aspect.
- Aggregating the aspect sentiment scores at the restaurant level.
- Retaining restaurants with sentiment scores for all three aspects.
- Splitting the restaurant-level data into 80% training and 20% testing sets.
- Standardizing the three aspect sentiment predictors.
- Fitting a multiple linear regression model to predict overall restaurant Yelp ratings.
- Evaluating the model using R², MAE, and RMSE.
- Generating the final regression coefficients, summary files, and figures.
6. The primary results should be approximately:
- Restaurants included: 1,866
- Training restaurants: 1,492
- Testing restaurants: 374
- Test R²: 0.1227
- Test MAE: 0.4753
- Test RMSE: 0.5923
- Quality coefficient: 0.1995
- Convenience coefficient: 0.1282
- Price coefficient: 0.0644
7. Generated results and figures can be found in the MODEL_OUTPUT folder.
