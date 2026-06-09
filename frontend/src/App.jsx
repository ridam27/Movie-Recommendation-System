import { useState } from "react";
import "./index.css";

function App() {
  const [movie, setMovie] = useState("");
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const getRecommendations = async () => {
    if (!movie.trim()) {
      setMessage("Please enter a movie name.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setRecommendations([]);

      const response = await fetch(
        `http://127.0.0.1:8000/recommend?movie=${encodeURIComponent(movie)}`
      );

      const data = await response.json();

      if (!data.found) {
        setMessage("Movie not found.");
        setSelectedMovie(null);
        return;
      }

      setSelectedMovie(data.selected_movie);
      setRecommendations(data.recommendations);
    } catch (error) {
      setMessage("Backend server not running.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      getRecommendations();
    }
  };

  return (
    <div className="app">
      <div className="hero">
        <h1>🎬 Movie Recommendation Engine</h1>
        <p>AI-powered recommendations using movie metadata</p>
      </div>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search movie..."
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
          onKeyDown={handleKeyPress}
        />

        <button onClick={getRecommendations}>
          {loading ? "Searching..." : "Recommend"}
        </button>
      </div>

      {message && (
        <div className="message">
          {message}
        </div>
      )}

      {selectedMovie && (
        <div className="selected-movie">
          <h2>Based on</h2>

          <div className="selected-card">
            {selectedMovie.poster && (
              <img
                src={selectedMovie.poster}
                alt={selectedMovie.title}
              />
            )}

            <div>
              <h3>{selectedMovie.title}</h3>

              <p>
                <strong>Year:</strong> {selectedMovie.year}
              </p>

              <p>
                <strong>Director:</strong> {selectedMovie.director}
              </p>

              <p>
                <strong>Genres:</strong> {selectedMovie.genres}
              </p>

              <p className="overview">
                {selectedMovie.overview}
              </p>
            </div>
          </div>
        </div>
      )}

      {recommendations.length > 0 && (
        <>
          <h2 className="section-title">
            Recommended Movies
          </h2>

          <div className="movies-grid">
            {recommendations.map((movie) => (
              <div
                key={movie.movieId}
                className="movie-card"
              >
                {movie.poster ? (
                  <img
                    src={movie.poster}
                    alt={movie.title}
                  />
                ) : (
                  <div className="poster-placeholder">
                    No Poster
                  </div>
                )}

                <div className="movie-content">
                  <h3>{movie.title}</h3>

                  <p>
                    <strong>Year:</strong> {movie.year}
                  </p>

                  <p>
                    <strong>Director:</strong>{" "}
                    {movie.director}
                  </p>

                  <p>
                    <strong>Genres:</strong>{" "}
                    {movie.genres}
                  </p>

                  <p className="overview">
                    {movie.overview}
                  </p>

                  <div className="score">
                    Similarity Score: {movie.score}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default App;