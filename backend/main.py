from recommender import MovieRecommender


def main():
    recommender = MovieRecommender("data/enriched_movies.csv")

    print("\nMovie Recommendation Engine")
    print("Dataset used: enriched_movies.csv")
    print("Type 'exit' to stop")

    while True:
        movie_name = input("\nEnter movie name you like: ").strip()

        if movie_name.lower() == "exit":
            print("Goodbye!")
            break

        if not movie_name:
            print("Please enter a movie name.")
            continue

        result = recommender.recommend(movie_name, limit=10)

        if result is None:
            print("Movie not found. Try another movie name.")
            continue

        selected_movie, recommendations = result

        print(f"\nRecommendations based on: {selected_movie['title']}")
        print(f"Year: {selected_movie['year']}")
        print(f"Director: {selected_movie['director']}")
        print("-" * 60)

        for index, movie in enumerate(recommendations, start=1):
            print(f"{index}. {movie['title']}")
            print(f"   Year: {movie['year']}")
            print(f"   Director: {movie['director']}")
            print(f"   Genres: {movie['genres']}")
            print(f"   Score: {movie['score']}")
            print()

        print("-" * 60)


if __name__ == "__main__":
    main()
