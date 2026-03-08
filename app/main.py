from fastapi import FastAPI
from api.routes import movies

app = FastAPI(title="MovieLens API", description="A simple API for movie data and ratings")

# Include the movies router
app.include_router(movies.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MovieLens API! Visit /docs for API documentation."}