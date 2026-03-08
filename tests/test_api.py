import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture
def transport():
    return ASGITransport(app=app)


# --- Root ---

@pytest.mark.asyncio
async def test_root(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


# --- Movies ---

@pytest.mark.asyncio
async def test_get_top_rated_movies(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/movies/top-rated?min_ratings=50&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5
        if data:
            movie = data[0]
            assert "movie_id" in movie
            assert "title" in movie
            assert "avg_rating" in movie
            assert "num_ratings" in movie
            assert "rank" in movie
            assert movie["num_ratings"] >= 50


@pytest.mark.asyncio
async def test_get_top_rated_chart(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/movies/top-rated/chart?min_ratings=50&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "layout" in data


@pytest.mark.asyncio
async def test_get_genre_avg_rating(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/movies/genres/avg-rating")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        genre = data[0]
        assert "genres" in genre
        assert "mean" in genre
        assert "count" in genre


@pytest.mark.asyncio
async def test_get_genre_chart(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/movies/genres/chart")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "layout" in data


@pytest.mark.asyncio
async def test_get_similar_movies(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/movies/1/similar?top_k=3")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        similar = data[0]
        assert "movie_id" in similar
        assert "title" in similar
        assert "similarity_score" in similar


@pytest.mark.asyncio
async def test_get_similar_movies_not_found(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/movies/9999999/similar")
        assert response.status_code == 200
        assert response.json() == []


# --- Users ---

@pytest.mark.asyncio
async def test_get_user_ratings(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/1/ratings")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        entry = data[0]
        assert "title" in entry
        assert "rating" in entry
        assert "moving_avg" in entry
        assert "date" in entry


@pytest.mark.asyncio
async def test_get_user_ratings_empty(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/9999999/ratings")
        assert response.status_code == 200
        assert response.json() == []


# --- Stats ---

@pytest.mark.asyncio
async def test_stats_overview(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/stats/overview")
        assert response.status_code == 200
        data = response.json()
        assert data["total_movies"] > 0
        assert data["total_ratings"] > 0
        assert data["unique_users"] > 0
        assert 0 < data["average_rating"] <= 5


@pytest.mark.asyncio
async def test_stats_rating_distribution(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/stats/rating-distribution")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        entry = data[0]
        assert "rating" in entry
        assert "count" in entry
