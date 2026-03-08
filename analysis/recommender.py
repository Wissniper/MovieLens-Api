import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.database import engine


def get_similar_movies(movie_id: int, top_k: int = 5):
    """Content-based recommender using TF-IDF on genres with cosine similarity."""
    query = "SELECT movie_id, title, genres FROM movies"
    df = pd.read_sql_query(query, engine)

    if df.empty:
        return []

    # Replace pipe separator with spaces so TF-IDF treats each genre as a token
    df["genres_clean"] = df["genres"].str.replace("|", " ", regex=False)

    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["genres_clean"])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find the index of the requested movie
    try:
        idx = df.index[df["movie_id"] == movie_id].tolist()[0]
    except IndexError:
        return []

    # Sort by similarity score descending, skip the movie itself
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1 : top_k + 1]

    movie_indices = [i[0] for i in sim_scores]
    results = df.iloc[movie_indices][["movie_id", "title", "genres"]].copy()
    results["similarity_score"] = [round(i[1], 2) for i in sim_scores]

    return results.to_dict(orient="records")
