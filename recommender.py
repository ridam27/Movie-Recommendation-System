import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    def __init__(self, movies_path):
        self.movies = pd.read_csv(movies_path)
        self.movies["genres"] = self.movies["genres"].fillna("")

        self.tfidf = TfidfVectorizer(token_pattern=r"[^|]+")
        self.genre_matrix = self.tfidf.fit_transform(self.movies["genres"])
        self.similarity_matrix = cosine_similarity(self.genre_matrix)

    def recommend(self, movie_name, limit=5):
        matched_movies = self.movies[
            self.movies["title"].str.contains(movie_name, case=False, na=False)
        ]

        if matched_movies.empty:
            return None

        movie_index = matched_movies.index[0]
        selected_movie = self.movies.iloc[movie_index]["title"]

        similarity_scores = list(
            enumerate(self.similarity_matrix[movie_index]))
        similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1], reverse=True)

        recommended_indexes = similarity_scores[1: limit + 1]

        recommendations = []

        for index, score in recommended_indexes:
            movie = self.movies.iloc[index]
            recommendations.append({
                "title": movie["title"],
                "genres": movie["genres"],
                "score": round(score, 2)
            })

        return selected_movie, recommendations
