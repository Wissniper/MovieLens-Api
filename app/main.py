from fastapi import FastAPI
from api.routes import movies, users, stats

app = FastAPI(
    title="MovieLens API",
    description="A FastAPI backend serving MovieLens data for Data Science interviews.",
    version="1.0.0"
)

app.include_router(movies.router)
app.include_router(users.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "Welcome to the MovieLens API! Go to /docs for the interactive API documentation."}
