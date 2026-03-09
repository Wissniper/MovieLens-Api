# MovieLens API

A FastAPI backend serving MovieLens movie ratings data with data science-powered endpoints — ETL pipelines, SQL analytics, genre analysis, interactive visualizations, and content-based recommendations.

Built with **FastAPI**, **SQLAlchemy**, **pandas**, **Plotly**, and **scikit-learn** on a SQLite database loaded from the [MovieLens](https://grouplens.org/datasets/movielens/) `ml-latest-small` dataset (~100K ratings, ~9,700 movies, ~600 users).

## Features

- **Top-Rated Movies** — SQL aggregations with `HAVING`, `ROW_NUMBER()` window functions
- **Genre Analysis** — Pandas `explode` + `groupby` on pipe-separated genre strings
- **User Rating History** — Time-series with SQL moving averages (sliding window)
- **Content-Based Recommendations** — TF-IDF vectorization + cosine similarity on genres
- **Interactive Charts** — Plotly visualizations returned as JSON
- **Dataset Statistics** — Overall stats and rating distribution

## Tech Stack

| Layer | Tools |
|-------|-------|
| Backend | FastAPI, Uvicorn |
| Database | SQLite, SQLAlchemy ORM |
| Data Processing | pandas, NumPy |
| Visualization | Plotly (JSON export) |
| Recommendations | scikit-learn (TF-IDF, cosine similarity) |
| Migrations | Alembic |
| Testing | pytest, httpx (async) |
| Packaging | Poetry |
| Deployment | Docker |

## Project Structure

```
movielens-api/
├── app/
│   ├── main.py            # FastAPI app + router registration
│   ├── database.py        # SQLAlchemy engine & session
│   ├── models.py          # Movie, Rating ORM models
│   ├── schemas.py         # Pydantic response models
│   └── crud.py            # SQL queries + pandas transforms
├── api/routes/
│   ├── movies.py          # /movies/* endpoints
│   ├── users.py           # /users/* endpoints
│   └── stats.py           # /stats/* endpoints
├── analysis/
│   ├── stats.py           # Overall stats & distribution
│   └── recommender.py     # TF-IDF content-based recommender
├── etl/
│   └── load_data.py       # CSV → SQLite ETL pipeline
├── scripts/
│   └── download_data.py   # Download MovieLens dataset
├── migrations/            # Alembic schema migrations
├── tests/
│   └── test_api.py        # Async API integration tests
├── task_guides/           # Educational deep-dive docs
├── data/                  # Raw CSVs (gitignored)
├── Dockerfile
├── pyproject.toml
└── alembic.ini
```

## Quick Start

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/)

### Setup

```bash
# Clone the repo
git clone https://github.com/Wissniper/MovieLens-Api.git
cd MovieLens-Api

# Install dependencies
poetry install

# Download the MovieLens dataset
poetry run python scripts/download_data.py

# Run database migrations
poetry run alembic upgrade head

# Load data into SQLite
poetry run python -c "from etl.load_data import load_data; load_data()"

# Start the server
poetry run uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/movies/top-rated` | Top-rated movies (params: `min_ratings`, `limit`) |
| GET | `/movies/top-rated/chart` | Plotly bar chart of top-rated movies |
| GET | `/movies/genres/avg-rating` | Average rating per genre |
| GET | `/movies/genres/chart` | Plotly bar chart of genre ratings |
| GET | `/movies/{movie_id}/similar` | Similar movies via TF-IDF (param: `top_k`) |
| GET | `/users/{user_id}/ratings` | User's rating history with moving averages |
| GET | `/stats/overview` | Total movies, ratings, users, avg rating |
| GET | `/stats/rating-distribution` | Count of each rating value |

### Example Requests

```bash
# Top 5 movies with at least 100 ratings
curl "http://localhost:8000/movies/top-rated?min_ratings=100&limit=5"

# Movies similar to Toy Story (movie_id=1)
curl "http://localhost:8000/movies/1/similar?top_k=5"

# User 1's rating history
curl "http://localhost:8000/users/1/ratings"

# Dataset overview
curl "http://localhost:8000/stats/overview"
```

## Docker

```bash
docker build -t movielens-api .
docker run -p 8000:8000 movielens-api
```

## Testing

```bash
poetry run pytest tests/ -v
```

Tests use `httpx.AsyncClient` with `ASGITransport` to test all endpoints without starting a server.

## Database Schema

**movies**
| Column | Type | Description |
|--------|------|-------------|
| movie_id | Integer (PK) | MovieLens movie ID |
| title | String | Movie title with year |
| genres | String | Pipe-separated genres (e.g. `"Action\|Comedy"`) |

**ratings**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Auto-generated |
| user_id | Integer | User identifier |
| movie_id | Integer | References movies |
| rating | Float | 0.5 to 5.0 |
| timestamp | BigInteger | Unix epoch seconds |

## Task Guides

The `task_guides/` directory contains educational deep-dives for each implementation phase:

1. **DB Models** — ORM mapping, normalization, ACID, B-tree indexing
2. **ETL Script** — Extract-Transform-Load lifecycle, idempotency, data quality
3. **Core API** — REST architecture, SQL joins, parameter binding, query plans
4. **Genre Analysis** — Vectorized ops, explode pattern, split-apply-combine
5. **User History** — Window functions, frames, time-series, moving averages
6. **Recommender** — TF-IDF, cosine similarity, content vs collaborative filtering
7. **Test & Visualize** — Testing pyramid, Plotly, data drift
8. **Deploy & Polish** — Docker layers, Gunicorn/Uvicorn, CI/CD, MLOps

## License

This project uses the [MovieLens dataset](https://grouplens.org/datasets/movielens/) provided by GroupLens Research.
