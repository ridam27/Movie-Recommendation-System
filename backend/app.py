from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import MovieRecommender

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = MovieRecommender("data/movies.csv")


@app.get("/")
def home():
    return {"message": "Bollywood Movie Recommendation API is running"}


@app.get("/recommend")
def recommend(movie: str = Query(...)):
    try:
        result = recommender.recommend(movie, limit=5)

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
            "selected_movie": str(selected_movie),
            "recommendations": recommendations
        }

    except Exception as e:
        return {
            "found": False,
            "error": str(e),
            "recommendations": []
        }
