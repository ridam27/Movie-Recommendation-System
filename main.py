from recommender import MovieRecommender


def main():
    recommender = MovieRecommender("data/movies.csv")

    print("\nBollywood Movie Recommendation Engine")
    print("Dataset used: movies.csv")
    print("Type 'exit' to stop")

    while True:
        movie_name = input("\nEnter movie name you like: ").strip()

        if movie_name.lower() == "exit":
            print("Goodbye!")
            break

        if movie_name == "":
            print("Please enter a movie name.")
            continue

        result = recommender.recommend(movie_name, limit=5)

        if result is None:
            print("Movie not found. Try another movie name.")
            continue

        selected_movie, recommendations = result

        print(f"\nRecommendations based on: {selected_movie}")
        print("-" * 50)

        for index, movie in enumerate(recommendations, start=1):
            print(f"{index}. {movie['title']}")
            print(f"   Genres: {movie['genres']}")
            print(f"   Similarity Score: {movie['score']}")

        print("-" * 50)


if __name__ == "__main__":
    main()