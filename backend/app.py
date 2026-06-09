from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import MovieRecommender

app = FastAPI(title="Movie Recommendation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = MovieRecommender("data/enriched_movies.csv")


@app.get("/")
def home():
    return {
        "message": "Movie Recommendation API is running",
        "dataset": "enriched_movies.csv"
    }


@app.get("/recommend")
def recommend(movie: str = Query(..., min_length=1)):
    try:
        result = recommender.recommend(movie, limit=10)

        if result is None:
            return {
                "found": False,
                "message": "Movie not found",
                "selected_movie": None,
                "recommendations": []
            }

        selected_movie, recommendations = result

        return {
            "found": True,
            "selected_movie": selected_movie,
            "recommendations": recommendations
        }

    except Exception as e:
        return {
            "found": False,
            "message": "Something went wrong",
            "error": str(e),
            "selected_movie": None,
            "recommendations": []
        }
