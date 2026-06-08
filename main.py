from recommender import MovieRecommender


def main():
    recommender = MovieRecommender("data/movies.csv")

    print("\nMovie Recommendation Engine")
    print("Type 'exit' to stop")

    while True:
        movie_name = input("\nEnter movie name: ")

        if movie_name.lower() == "exit":
            print("Goodbye!")
            break

        result = recommender.recommend(movie_name)

        if result is None:
            print("Movie not found. Try another name.")
            continue

        selected_movie, recommendations = result

        print(f"\nRecommendations based on: {selected_movie}")
        print("-" * 40)

        for index, movie in enumerate(recommendations, start=1):
            print(f"{index}. {movie['title']}")
            print(f"   Genres: {movie['genres']}")
            print(f"   Similarity Score: {movie['score']}")


if __name__ == "__main__":
    main()
