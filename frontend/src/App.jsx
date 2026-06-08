import { useState } from "react";
import "./index.css";

function App() {
  const [movie, setMovie] = useState("");
  const [selectedMovie, setSelectedMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [message, setMessage] = useState("");

  const getRecommendations = async () => {
    if (!movie.trim()) {
      setMessage("Please enter a movie name");
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/recommend?movie=${movie}`
      );

      const data = await response.json();

      if (!data.found) {
        setMessage("Movie not found");
        setRecommendations([]);
        setSelectedMovie("");
        return;
      }

      setSelectedMovie(data.selected_movie);
      setRecommendations(data.recommendations);
      setMessage("");
    } catch (error) {
      setMessage("Backend is not running");
    }
  };

  return (
    <div className="app">
      <h1>Bollywood Movie Recommendation Engine</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter movie name..."
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
        />

        <button onClick={getRecommendations}>Recommend</button>
      </div>

      {message && <p className="message">{message}</p>}

      {selectedMovie && (
        <h2>Recommendations based on: {selectedMovie}</h2>
      )}

      <div className="movie-list">
        {recommendations.map((item, index) => (
          <div className="movie-card" key={item.movieId}>
            <h3>
              {index + 1}. {item.title}
            </h3>
            <p>Genres: {item.genres}</p>
            <p>Similarity Score: {item.score}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;