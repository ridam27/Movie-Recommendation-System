import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movies_path="data/enriched_movies.csv"):
        self.movies = pd.read_csv(movies_path)

        self.movies.columns = self.movies.columns.str.strip().str.lower()

        self.movies = self.movies.rename(columns={
            "movieid": "movieId"
        })

        required_columns = ["movieId", "title", "genres",
                            "year", "director", "cast", "overview"]

        for column in required_columns:
            if column not in self.movies.columns:
                self.movies[column] = ""

        self.movies["movieId"] = self.movies["movieId"].fillna(0).astype(int)
        self.movies["title"] = self.movies["title"].fillna("").astype(str)
        self.movies["genres"] = self.movies["genres"].fillna("").astype(str)
        self.movies["year"] = self.movies["year"].fillna("").astype(str)
        self.movies["director"] = self.movies["director"].fillna(
            "").astype(str)
        self.movies["cast"] = self.movies["cast"].fillna("").astype(str)
        self.movies["overview"] = self.movies["overview"].fillna(
            "").astype(str)

        if "poster" not in self.movies.columns:
            self.movies["poster"] = ""

        self.movies["poster"] = self.movies["poster"].fillna("").astype(str)

        self.movies["search_title"] = self.movies["title"].apply(
            self.clean_text)

        self.movies["combined_features"] = (
            self.movies["genres"] + " " +
            self.movies["director"] + " " +
            self.movies["cast"] + " " +
            self.movies["overview"]
        ).apply(self.clean_text)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        self.feature_matrix = self.vectorizer.fit_transform(
            self.movies["combined_features"]
        )

        self.similarity_matrix = cosine_similarity(self.feature_matrix)

    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def recommend(self, movie_name, limit=5):
        movie_name_clean = self.clean_text(movie_name)

        matched_movies = self.movies[
            self.movies["search_title"].str.contains(
                movie_name_clean,
                case=False,
                na=False,
                regex=False
            )
        ]

        if matched_movies.empty:
            return None

        movie_index = matched_movies.index[0]
        selected_movie = self.movies.loc[movie_index]

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
                "year": str(movie["year"]),
                "genres": str(movie["genres"]),
                "director": str(movie["director"]),
                "cast": str(movie["cast"]),
                "overview": str(movie["overview"]),
                "poster": str(movie["poster"]),
                "score": float(round(score, 3))
            })

            if len(recommendations) == limit:
                break

        selected_movie_data = {
            "movieId": int(selected_movie["movieId"]),
            "title": str(selected_movie["title"]),
            "year": str(selected_movie["year"]),
            "genres": str(selected_movie["genres"]),
            "director": str(selected_movie["director"]),
            "cast": str(selected_movie["cast"]),
            "overview": str(selected_movie["overview"]),
            "poster": str(selected_movie["poster"]),
        }

        return selected_movie_data, recommendations
