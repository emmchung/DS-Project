"""
DS 4002 - Group 8
Script: Train Modeling

Purpose:
This script performs the primary analysis for the Yelp restaurant review
project. It identifies review text related to quality, price, and convenience,
calculates VADER sentiment scores for each aspect, aggregates the sentiment
scores at the restaurant level, and uses multiple linear regression to examine
the relationship between aspect sentiment and overall restaurant Yelp ratings.

Input:
- Data/sitdown_reviews_25mb.csv

Outputs:
- Restaurant-level aspect sentiment results
- Regression coefficients
- Model evaluation metrics (R², MAE, and RMSE)
- Figures and summary files saved to MODEL_OUTPUT

Required packages:
pandas, numpy, nltk, scikit-learn, matplotlib, joblib
"""
import os
import re
from pathlib import Path

import joblib
import matplotlib
import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

matplotlib.use("Agg")
import matplotlib.pyplot as plt

nltk.download("vader_lexicon", quiet=True)

DATA_PATH = Path("Data/sitdown_reviews_25mb.csv")
OUTPUT_DIR = Path("MODEL_OUTPUT")
MODEL_PATH = OUTPUT_DIR / "restaurant_review_model.joblib"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    if OUTPUT_DIR.exists() and not OUTPUT_DIR.is_dir():
        raise IsADirectoryError(
            f"Cannot use {OUTPUT_DIR} because a file already exists there. "
            "Please remove or rename that file before running the model."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    original_rows = len(df)

    print(f"Original number of rows: {original_rows}")

    # Keep only rows with review text and a valid rating
    cleaned_df = df[["text", "stars"]].dropna().copy()
    cleaned_df["stars"] = cleaned_df["stars"].astype(int)

    print(f"Rows after dropping missing text/stars: {len(cleaned_df)}")

    if "review_id" in df.columns:
        print(f"Number of unique reviews: {df['review_id'].nunique()}")

    rating_counts = cleaned_df["stars"].value_counts().sort_index()
    rating_percentages = (rating_counts / rating_counts.sum() * 100).round(2)

    print("\nStar rating counts and percentages:")
    for rating in range(1, 6):
        count = int(rating_counts.get(rating, 0))
        percentage = rating_percentages.get(rating, 0.0)
        print(f"  {rating}: {count} ({percentage:.2f}%)")

    quality_keywords = [
        "food", "delicious", "tasty", "fresh", "flavor", "flavour",
        "quality", "meal", "dish", "excellent", "amazing", "great food",
        "taste", "texture", "cooked well", "ingredients", "portion"
    ]
    price_keywords = [
        "price", "cheap", "expensive", "value", "worth", "cost", "budget",
        "affordable", "reasonable", "overpriced", "deal", "priced"
    ]
    convenience_keywords = [
        "fast", "quick", "easy", "parking", "location", "close", "convenient",
        "access", "pickup", "takeout", "delivery", "wait time", "friendly staff",
        "service", "busy", "line"
    ]

    def mentions_keywords(text, keywords):
        if pd.isna(text):
            return False
        lower_text = str(text).lower()
        return any(keyword.lower() in lower_text for keyword in keywords)

    aspect_df = cleaned_df.copy()
    aspect_df["mentions_quality"] = aspect_df["text"].apply(
        lambda text: mentions_keywords(text, quality_keywords)
    )
    aspect_df["mentions_price"] = aspect_df["text"].apply(
        lambda text: mentions_keywords(text, price_keywords)
    )
    aspect_df["mentions_convenience"] = aspect_df["text"].apply(
        lambda text: mentions_keywords(text, convenience_keywords)
    )

    print("\nAspect mention summary:")
    for aspect_name, column_name in [
        ("quality", "mentions_quality"),
        ("price", "mentions_price"),
        ("convenience", "mentions_convenience"),
    ]:
        count = int(aspect_df[column_name].sum())
        percentage = (count / len(aspect_df) * 100) if len(aspect_df) > 0 else 0.0
        print(f"  {aspect_name}: {count} ({percentage:.2f}%)")

    print("\nRandom review examples for each aspect:")
    for aspect_name, column_name in [
        ("quality", "mentions_quality"),
        ("price", "mentions_price"),
        ("convenience", "mentions_convenience"),
    ]:
        examples = aspect_df[aspect_df[column_name]].sample(n=10, random_state=42)
        print(f"\n--- {aspect_name.title()} examples ---")
        for idx, row in examples.iterrows():
            print(f"Star rating: {row['stars']}")
            print(row["text"])
            print("---")

    # Aspect-based sentiment analysis using VADER on only the sentences that mention
    # the target aspect. This is separate from the overall star rating model.
    sia = SentimentIntensityAnalyzer()

    def extract_aspect_sentences(text, keywords):
        if pd.isna(text):
            return []
        sentences = re.split(r"(?<=[.!?])\s+", str(text))
        lower_keywords = [keyword.lower() for keyword in keywords]
        matches = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in lower_keywords):
                matches.append(sentence.strip())
        return matches

    def aspect_sentiment(text, keywords):
        sentences = extract_aspect_sentences(text, keywords)
        if not sentences:
            return float("nan")
        scores = [sia.polarity_scores(sentence)["compound"] for sentence in sentences]
        return float(sum(scores) / len(scores))

    aspect_df["quality_sentiment"] = aspect_df["text"].apply(
        lambda text: aspect_sentiment(text, quality_keywords)
        if mentions_keywords(text, quality_keywords) else float("nan")
    )
    aspect_df["price_sentiment"] = aspect_df["text"].apply(
        lambda text: aspect_sentiment(text, price_keywords)
        if mentions_keywords(text, price_keywords) else float("nan")
    )
    aspect_df["convenience_sentiment"] = aspect_df["text"].apply(
        lambda text: aspect_sentiment(text, convenience_keywords)
        if mentions_keywords(text, convenience_keywords) else float("nan")
    )

    print("\nAspect sentiment examples (10 random samples per aspect):")
    for aspect_name, column_name, score_column in [
        ("quality", "mentions_quality", "quality_sentiment"),
        ("price", "mentions_price", "price_sentiment"),
        ("convenience", "mentions_convenience", "convenience_sentiment"),
    ]:
        examples = aspect_df[aspect_df[column_name]].sample(n=10, random_state=42)
        print(f"\n--- {aspect_name.title()} sentiment examples ---")
        for _, row in examples.iterrows():
            relevant_sentences = extract_aspect_sentences(row["text"], {
                "quality": quality_keywords,
                "price": price_keywords,
                "convenience": convenience_keywords,
            }[aspect_name])
            print(f"Star rating: {row['stars']}")
            print("Relevant aspect text:")
            print(" ".join(relevant_sentences))
            print(f"Sentiment score: {row[score_column]:.4f}")
            print("---")

    # Evaluation: check how well aspect sentiment lines up with the actual Yelp star
    # ratings before any conversion to aspect-specific 1-5 scores.
    aspect_mapping = {
        "quality": "quality_sentiment",
        "price": "price_sentiment",
        "convenience": "convenience_sentiment",
    }

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
    fig.suptitle("Mean aspect sentiment by Yelp star rating")

    for ax, (aspect_name, score_column) in zip(axes, aspect_mapping.items()):
        filtered = aspect_df[aspect_df[score_column].notna()].copy()
        filtered = filtered[filtered["stars"].isin([1, 2, 3, 4, 5])]

        corr = filtered[score_column].corr(filtered["stars"])
        print(f"\n{aspect_name.title()} aspect sentiment correlation with stars:")
        print(f"  Pearson correlation: {corr:.4f}")
        print(f"  Number of reviews used: {len(filtered)}")

        mean_by_star = filtered.groupby("stars")[score_column].mean().reindex([1, 2, 3, 4, 5])
        print(f"  Mean sentiment by star rating:")
        for star in [1, 2, 3, 4, 5]:
            value = mean_by_star.get(star, float("nan"))
            print(f"    {star}: {value:.4f}")

        ax.bar(mean_by_star.index.astype(str), mean_by_star.values, color="steelblue")
        ax.set_title(aspect_name.title())
        ax.set_xlabel("Yelp star rating")
        ax.set_ylabel("Mean sentiment")
        ax.axhline(0, color="black", linewidth=0.8)

    plot_path = OUTPUT_DIR / "aspect_sentiment_by_star.png"
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(plot_path, dpi=150)
    print(f"\nSaved aspect sentiment bar plot to: {plot_path}")

    # Convert each non-missing aspect sentiment score into a predicted 1-5 rating by
    # matching it to the observed mean sentiment value for each Yelp star level.
    aspect_pred_cols = {
        "quality": "quality_rating",
        "price": "price_rating",
        "convenience": "convenience_rating",
    }

    for aspect_name, score_column in aspect_mapping.items():
        filtered = aspect_df[aspect_df[score_column].notna()].copy()
        score_to_rating = {}
        mean_by_star = filtered.groupby("stars")[score_column].mean().reindex([1, 2, 3, 4, 5])

        for star in [1, 2, 3, 4, 5]:
            if pd.notna(mean_by_star.get(star)):
                score_to_rating[star] = mean_by_star[star]

        if not score_to_rating:
            aspect_df[aspect_pred_cols[aspect_name]] = float("nan")
            continue

        def map_score_to_rating(value):
            if pd.isna(value):
                return float("nan")
            closest_star = min(score_to_rating, key=lambda star: abs(score_to_rating[star] - value))
            return int(closest_star)

        aspect_df[aspect_pred_cols[aspect_name]] = aspect_df[score_column].apply(map_score_to_rating)

    for aspect_name, rating_col in aspect_pred_cols.items():
        print(f"\n{aspect_name.title()} predicted aspect rating distribution:")
        counts = aspect_df[rating_col].value_counts().sort_index()
        for star in [1, 2, 3, 4, 5]:
            count = int(counts.get(star, 0))
            print(f"  {star}: {count}")

    print("\nRandom aspect rating validation examples:")
    for aspect_name, score_column, rating_col in [
        ("quality", "quality_sentiment", "quality_rating"),
        ("price", "price_sentiment", "price_rating"),
        ("convenience", "convenience_sentiment", "convenience_rating"),
    ]:
        valid_rows = aspect_df[aspect_df[score_column].notna()].copy()
        examples = valid_rows.sample(n=10, random_state=42)
        print(f"\n--- {aspect_name.title()} rating examples ---")
        for _, row in examples.iterrows():
            relevant_sentences = extract_aspect_sentences(row["text"], {
                "quality": quality_keywords,
                "price": price_keywords,
                "convenience": convenience_keywords,
            }[aspect_name])
            print(f"Actual overall star rating: {row['stars']}")
            print("Relevant aspect text:")
            print(" ".join(relevant_sentences))
            print(f"Sentiment score: {row[score_column]:.4f}")
            print(f"Predicted {aspect_name} rating: {int(row[rating_col])}")
            print("---")

    # Regression analysis using the continuous aspect sentiment scores.
    # This is separate from the TF-IDF text model and uses only reviews where all
    # three aspect sentiments are available.
    regression_df = aspect_df[
        ["stars", "quality_sentiment", "price_sentiment", "convenience_sentiment"]
    ].dropna().copy()

    print(f"\nReviews with all three aspect sentiment scores available: {len(regression_df)}")

    X_reg = regression_df[["quality_sentiment", "price_sentiment", "convenience_sentiment"]].copy()
    y_reg = regression_df["stars"]

    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
        X_reg,
        y_reg,
        test_size=0.2,
        random_state=42,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_reg)
    X_test_scaled = scaler.transform(X_test_reg)

    reg_model = LinearRegression()
    reg_model.fit(X_train_scaled, y_train_reg)

    y_pred_reg = reg_model.predict(X_test_scaled)

    print("\nAspect sentiment regression results:")
    print(f"  Standardized coefficient for quality: {reg_model.coef_[0]:.4f}")
    print(f"  Standardized coefficient for price: {reg_model.coef_[1]:.4f}")
    print(f"  Standardized coefficient for convenience: {reg_model.coef_[2]:.4f}")
    print(f"  Intercept: {reg_model.intercept_:.4f}")
    print(f"  Test-set R-squared: {r2_score(y_test_reg, y_pred_reg):.4f}")
    print(f"  Test-set MAE: {mean_absolute_error(y_test_reg, y_pred_reg):.4f}")
    rmse = mean_squared_error(y_test_reg, y_pred_reg) ** 0.5
    print(f"  Test-set RMSE: {rmse:.4f}")

    corr_matrix = regression_df[["quality_sentiment", "price_sentiment", "convenience_sentiment", "stars"]].corr(method="pearson")
    print("\nPearson correlation matrix:")
    print(corr_matrix.round(4))

    coef_df = pd.DataFrame({
        "aspect": ["quality", "price", "convenience"],
        "standardized_coefficient": reg_model.coef_
    })

    plt.figure(figsize=(8, 5))
    plt.bar(coef_df["aspect"], coef_df["standardized_coefficient"], color=["steelblue", "darkorange", "forestgreen"])
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Standardized regression coefficients for aspect sentiment")
    plt.xlabel("Aspect")
    plt.ylabel("Coefficient")
    plt.tight_layout()
    plot_reg_path = OUTPUT_DIR / "aspect_regression_coefficients.png"
    plt.savefig(plot_reg_path, dpi=150)
    print(f"\nSaved aspect regression coefficient plot to: {plot_reg_path}")

    df = cleaned_df
    X = df["text"]
    y = df["stars"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=2,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    multi_class="auto",
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    mae = (abs(y_test - y_pred)).mean()

    print(f"Model accuracy: {acc:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_PATH)
    print(f"\nSaved model to: {MODEL_PATH}")

    # Final results summary using the aspect analysis results already calculated.
    summary_rows = []
    for aspect_name, score_column, coefficient in zip(
        ["quality", "price", "convenience"],
        ["quality_sentiment", "price_sentiment", "convenience_sentiment"],
        reg_model.coef_,
    ):
        aspect_rows = aspect_df[aspect_df[score_column].notna()]
        summary_rows.append({
            "aspect": aspect_name,
            "reviews_mentioning_aspect": len(aspect_rows),
            "pearson_correlation_with_stars": aspect_rows[score_column].corr(
                aspect_rows["stars"]
            ),
            "standardized_regression_coefficient": coefficient,
        })

    aspect_results_summary = pd.DataFrame(summary_rows)
    summary_path = OUTPUT_DIR / "aspect_results_summary.csv"
    aspect_results_summary.to_csv(summary_path, index=False)
    print(f"Saved aspect results summary to: {summary_path}")

    # Save one scatter plot with a fitted regression line for each aspect.
    for aspect_name, score_column in zip(
        ["quality", "price", "convenience"],
        ["quality_sentiment", "price_sentiment", "convenience_sentiment"],
    ):
        aspect_rows = aspect_df[aspect_df[score_column].notna()]
        line_model = LinearRegression()
        line_model.fit(aspect_rows[[score_column]], aspect_rows["stars"])
        sorted_scores = aspect_rows[[score_column]].sort_values(score_column)
        fitted_stars = line_model.predict(sorted_scores)

        plt.figure(figsize=(7, 5))
        plt.scatter(aspect_rows[score_column], aspect_rows["stars"], alpha=0.2)
        plt.plot(sorted_scores[score_column], fitted_stars, color="red")
        plt.title(f"{aspect_name.title()} sentiment versus Yelp stars")
        plt.xlabel(f"{aspect_name.title()} sentiment score")
        plt.ylabel("Yelp star rating")
        plt.tight_layout()
        scatter_path = OUTPUT_DIR / f"{aspect_name}_sentiment_vs_stars.png"
        plt.savefig(scatter_path, dpi=150)
        plt.close()
        print(f"Saved {aspect_name} scatter plot to: {scatter_path}")

    # Compare the multiple regression predictions with the actual test-set stars.
    plt.figure(figsize=(7, 5))
    plt.scatter(y_test_reg, y_pred_reg, alpha=0.4)
    plot_min = min(y_test_reg.min(), y_pred_reg.min())
    plot_max = max(y_test_reg.max(), y_pred_reg.max())
    plt.plot([plot_min, plot_max], [plot_min, plot_max], color="red")
    plt.title("Predicted versus actual Yelp stars")
    plt.xlabel("Actual Yelp stars")
    plt.ylabel("Predicted Yelp stars")
    plt.tight_layout()
    predicted_actual_path = OUTPUT_DIR / "aspect_regression_predicted_vs_actual.png"
    plt.savefig(predicted_actual_path, dpi=150)
    plt.close()
    print(f"Saved predicted-versus-actual plot to: {predicted_actual_path}")

    largest_aspect = aspect_results_summary.loc[
        aspect_results_summary["standardized_regression_coefficient"].idxmax(),
        "aspect",
    ]
    print("\nFinal aspect-based results summary:")
    print(f"  Full dataset reviews: {original_rows}")
    print(f"  Reviews used in three-aspect regression: {len(regression_df)}")
    print(f"  R-squared: {r2_score(y_test_reg, y_pred_reg):.4f}")
    print(f"  MAE: {mean_absolute_error(y_test_reg, y_pred_reg):.4f}")
    print(f"  RMSE: {rmse:.4f}")
    for row in summary_rows:
        print(
            f"  {row['aspect'].title()} standardized coefficient: "
            f"{row['standardized_regression_coefficient']:.4f}"
        )
    print(f"  Largest standardized coefficient: {largest_aspect}")


if __name__ == "__main__":
    main()
