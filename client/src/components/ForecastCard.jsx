import { useState, useEffect } from 'react';
import '../styles/ForecastCard.css';

function ForecastCard({ location }) {
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Use a Vite environment variable
    const apiUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5555';

    fetch(`${apiUrl}/weather/forecast?location=${location}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch forecast data');
        }
        return res.json();
      })
      .then((data) => setForecast(data))
      .catch((err) => {
        setError(err.message);
        console.error('Failed to fetch forecast data:', err);
      });
  }, [location]);

  if (error) {
    return <div className="forecast-card error">Error: {error}</div>;
  }

  return (
    <div className="forecast-card">
      <h3>7-Day Forecast for {location}</h3>
      {forecast ? (
        <div className="forecast-list">
          {forecast.map((day, index) => (
            <div key={index} className="forecast-day">
              <p>{day.date}</p>
              <p>Temp: {day.temp}°C</p>
              <p>Condition: {day.condition}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading forecast...</p>
      )}
    </div>
  );
}

export default ForecastCard;
