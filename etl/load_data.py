import pandas as pd
import os
from app.database import engine

DATA_PATH = "data/ml-latest-small"

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data path {DATA_PATH} not found. Run scripts/download_data.py first.")
        return

    print("Extracting and Transforming movies...")
    movies_df = pd.read_csv(os.path.join(DATA_PATH, "movies.csv"))
    # Rename 'movieId' to 'movie_id' to match our DB Model
    movies_df.rename(columns={"movieId": "movie_id"}, inplace=True)
    
    # Load into SQL
    # 'append' means add to the table without deleting it
    # 'index=False' means don't save the pandas index as a column
    movies_df.to_sql("movies", engine, if_exists="append", index=False)
    print(f"Successfully loaded {len(movies_df)} movies into the database.")

    print("Extracting and Transforming ratings...")
    # CSV: userId,movieId,rating,timestamp
    ratings_df = pd.read_csv(os.path.join(DATA_PATH, "ratings.csv"))
    
    # CLEANING: Remove duplicates
    # A user should not have two ratings for the same movie
    ratings_df.drop_duplicates(subset=["userId", "movieId"], keep="last", inplace=True)
    
    # CLEANING: Rename columns to match DB schema
    ratings_df.rename(columns={
        "userId": "user_id", 
        "movieId": "movie_id"
    }, inplace=True)
    
    # Load into SQL
    # Since we didn't provide an 'id' column, SQLAlchemy/SQLite will auto-generate it.
    ratings_df.to_sql("ratings", engine, if_exists="append", index=False)
    print(f"Successfully loaded {len(ratings_df)} ratings into the database.")
