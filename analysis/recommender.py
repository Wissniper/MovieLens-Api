import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import text
from app.database import engine

def get_similar_movies(movie_id: int, top_k: int = 5):
    # Laad de films en genres in (in het echt gebruik je caching of een vector DB)
    query = "SELECT movie_id, title, genres FROM movies"
    df = pd.read_sql_query(query, engine)
    
    # Bereid de genres voor (vervang | met spatie zodat Tfidf het als losse woorden ziet)
    df["genres_clean"] = df["genres"].str.replace("|", " ")
    
    # Tfidf Vectorisatie
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df["genres_clean"])
    
    # Cosine Similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Vind de index van de gewenste film
    try:
        idx = df.index[df['movie_id'] == movie_id].tolist()[0]
    except IndexError:
        return [] # Film niet gevonden

    # Zoek de meest vergelijkbare
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Sla de film zelf over (index 0) en haal de top_k op
    sim_scores = sim_scores[1:top_k+1]
    
    # Bereid output voor
    movie_indices = [i[0] for i in sim_scores]
    results = df.iloc[movie_indices][["movie_id", "title", "genres"]].copy()
    results["similarity_score"] = [round(i[1], 2) for i in sim_scores]
    
    return results.to_dict(orient="records")
