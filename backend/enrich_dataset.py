import os
import time
import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import re

session = requests.Session()

retry_strategy = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

INPUT_FILE = "data/movies.csv"
OUTPUT_FILE = "data/enriched_movies.csv"
DELAY = 0.6


def clean_title_and_year(title):
    title = str(title)

    match = re.search(r"\((\d{4})\)", title)
    year = match.group(1) if match else ""

    clean_title = re.sub(r"\(\d{4}\)", "", title).strip()

    return clean_title, year


def search_movie(title):
    clean_title, year = clean_title_and_year(title)

    params = {
        "api_key": TMDB_API_KEY,
        "query": clean_title,
    }

    if year:
        params["year"] = year

    response = session.get(
        f"{BASE_URL}/search/movie",
        params=params,
        timeout=20,
    )

    if response.status_code != 200:
        return None

    results = response.json().get("results", [])
    return results[0] if results else None


def get_movie_details(tmdb_id):
    response = session.get(
        f"{BASE_URL}/movie/{tmdb_id}",
        params={
            "api_key": TMDB_API_KEY,
            "append_to_response": "credits",
        },
        timeout=20,
    )

    if response.status_code != 200:
        return None

    return response.json()


def get_director(credits):
    for person in credits.get("crew", []):
        if person.get("job") == "Director":
            return person.get("name", "")
    return ""


def get_genres(tmdb_genres):
    return " ".join(
        genre.get("name", "")
        for genre in tmdb_genres
    )


def get_cast(credits, limit=5):
    cast = credits.get("cast", [])[:limit]
    return " ".join(person.get("name", "") for person in cast)


def get_year(release_date):
    if not release_date:
        return ""
    return release_date[:4]


def create_empty_row(row):
    return {
        "movieId": int(row["movieId"]),
        "title": str(row["title"]),
        "genres": str(row["genres"]),
        "year": "",
        "director": "",
        "cast": "",
        "overview": "",
        "poster": "",
    }


def enrich_single_movie(row):
    movie_id = int(row["movieId"])
    title = str(row["title"])
    clean_title, extracted_year = clean_title_and_year(title)
    original_genres = str(row["genres"])

    search_result = search_movie(title)

    if search_result is None:
        return create_empty_row(row)

    tmdb_id = search_result.get("id")

    if tmdb_id is None:
        return create_empty_row(row)

    details = get_movie_details(tmdb_id)
    
    tmdb_genres = get_genres(
        details.get("genres", [])
    )

    if details is None:
        return create_empty_row(row)

    credits = details.get("credits", {})
    poster_path = details.get("poster_path", "")

    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

    return {
        "movieId": movie_id,
        "title": title,
        "year": get_year(details.get("release_date", "")) or extracted_year,
        "genres": tmdb_genres if tmdb_genres else original_genres,
        "year": get_year(details.get("release_date", "")),
        "director": get_director(credits),
        "cast": get_cast(credits),
        "overview": details.get("overview", ""),
        "poster": poster,
    }


def load_existing_enriched():
    if os.path.exists(OUTPUT_FILE):
        return pd.read_csv(OUTPUT_FILE)

    return pd.DataFrame(columns=[
        "movieId",
        "title",
        "genres",
        "year",
        "director",
        "cast",
        "overview",
        "poster",
    ])


def save_row(row_data):
    df = pd.DataFrame([row_data])
    file_exists = os.path.exists(OUTPUT_FILE)

    df.to_csv(
        OUTPUT_FILE,
        mode="a",
        index=False,
        header=not file_exists,
        encoding="utf-8",
    )


def enrich_movies():
    if not TMDB_API_KEY:
        print("TMDB_API_KEY not found. Add it in backend/.env")
        return

    movies = pd.read_csv(INPUT_FILE)

    movies.columns = movies.columns.str.strip()
    movies = movies.rename(columns={
        "movieID": "movieId",
        "MovieID": "movieId",
        "TITLE": "title",
        "Title": "title",
        "GENRES": "genres",
        "Genres": "genres",
    })

    existing = load_existing_enriched()

    already_done = set()

    if not existing.empty and "movieId" in existing.columns:
        already_done = set(existing["movieId"].dropna().astype(int).tolist())

    remaining_movies = movies[~movies["movieId"].astype(
        int).isin(already_done)]

    print(f"Total movies: {len(movies)}")
    print(f"Already enriched: {len(already_done)}")
    print(f"Remaining: {len(remaining_movies)}")

    for _, row in tqdm(remaining_movies.iterrows(), total=len(remaining_movies)):
        try:
            enriched_row = enrich_single_movie(row)
            save_row(enriched_row)
        except Exception as e:
            print(f"Error processing {row['title']}: {e}")
            save_row(create_empty_row(row))

        time.sleep(DELAY)

    print("Dataset enrichment completed.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    enrich_movies()
