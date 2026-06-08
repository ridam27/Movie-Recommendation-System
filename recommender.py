import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movies_path):
        # Load dataset
        self.movies = pd.read_csv(movies_path)

        # Handle missing genres
        self.movies["genres"] = self.movies["genres"].fillna("")

        # Convert genres into numerical vectors
        self.vectorizer = TfidfVectorizer(token_pattern=r"[^|]+")

        self.genre_matrix = self.vectorizer.fit_transform(
            self.movies["genres"]
        )

        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(
            self.genre_matrix,
            self.genre_matrix
        )

    def recommend(self, movie_name, limit=5):
        # Find matching movie
        matched_movies = self.movies[
            self.movies["title"].str.contains(
                movie_name,
                case=False,
                na=False
            )
        ]

        if matched_movies.empty:
            return None

        # Take first matching movie
        movie_index = matched_movies.index[0]

        selected_movie = self.movies.iloc[movie_index]["title"]

        # Get similarity scores
        similarity_scores = list(
            enumerate(self.similarity_matrix[movie_index])
        )

        # Sort descending
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        # Skip itself and take top recommendations
        similarity_scores = similarity_scores[1:limit + 1]

        recommendations = []

        for index, score in similarity_scores:
            movie = self.movies.iloc[index]

            recommendations.append({
                "movieId": movie["movieId"],
                "title": movie["title"],
                "genres": movie["genres"],
                "score": round(score, 3)
            })

        return selected_movie, recommendations
