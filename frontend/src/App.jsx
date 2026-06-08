import { useState } from "react";
import "./index.css";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState("");
  const [message, setMessage] = useState("");

  const getRecommendations = async () => {
    if (!movie.trim()) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/recommend?movie=${movie}`
      );

      const data = await response.json();

      if (!data.found) {
        setMessage("Movie not found");
        setRecommendations([]);
        return;
      }

      setMessage("");
      setSelectedMovie(data.selected_movie);
      setRecommendations(data.recommendations);
    } catch (error) {
      setMessage("Backend not running");
    }
  };

  return (
    <div className="app">
      <h1>🎬 Bollywood Movie Recommender</h1>

      <div className="search-section">
        <input
          type="text"
          placeholder="Enter movie name..."
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
        />
        <button onClick={getRecommendations}>Recommend</button>
      </div>

      {message && <p className="error">{message}</p>}

      {selectedMovie && (
        <h2 className="heading">
          Recommendations based on: {selectedMovie}
        </h2>
      )}

      <div className="movie-grid">
        {recommendations.map((movie, index) => (
          <div className="movie-card" key={movie.movieId}>
            <div className="rank">{index + 1}</div>

            <h3>{movie.title}</h3>

            <p className="genres">{movie.genres}</p>

            <p className="score">
              Similarity Score: {movie.score}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;