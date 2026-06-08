import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movies_path):
        self.movies = pd.read_csv(movies_path)

        # Normalize column names
        self.movies.columns = self.movies.columns.str.strip().str.lower()

        # Rename movieid to movieId internally
        if "movieid" in self.movies.columns:
            self.movies = self.movies.rename(columns={"movieid": "movieId"})

        if "title" not in self.movies.columns or "genres" not in self.movies.columns:
            raise ValueError("CSV must contain movieId, title, genres columns")

        self.movies["movieId"] = self.movies["movieId"].astype(int)
        self.movies["title"] = self.movies["title"].astype(str).str.strip()
        self.movies["genres"] = self.movies["genres"].fillna(
            "").astype(str).str.strip()

        self.movies["search_title"] = self.movies["title"].str.lower()

        # Support both comma-separated and pipe-separated genres
        self.movies["genres_clean"] = (
            self.movies["genres"]
            .str.replace(",", " ", regex=False)
            .str.replace("|", " ", regex=False)
        )

        self.vectorizer = TfidfVectorizer()
        self.genre_matrix = self.vectorizer.fit_transform(
            self.movies["genres_clean"])
        self.similarity_matrix = cosine_similarity(self.genre_matrix)

    def recommend(self, movie_name, limit=5):
        movie_name = movie_name.lower().strip()

        matched_movies = self.movies[
            self.movies["search_title"].str.contains(
                movie_name, na=False, regex=False)
        ]

        if matched_movies.empty:
            return None

        movie_index = matched_movies.index[0]
        selected_movie = str(self.movies.loc[movie_index, "title"])

        similarity_scores = list(
            enumerate(self.similarity_matrix[movie_index]))
        similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1], reverse=True)

        recommendations = []

        for index, score in similarity_scores:
            if index == movie_index:
                continue

            movie = self.movies.iloc[index]

            recommendations.append({
                "movieId": int(movie["movieId"]),
                "title": str(movie["title"]),
                "genres": str(movie["genres"]),
                "score": float(round(score, 3))
            })

            if len(recommendations) == limit:
                break

        return selected_movie, recommendations
