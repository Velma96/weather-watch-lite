import { useState, useEffect } from 'react';
import '../styles/ForecastCard.css';

// Get day of the week based on offset from today
const getWeekdayName = (offset) => {
  const today = new Date();
  const forecastDate = new Date(today);
  forecastDate.setDate(today.getDate() + (offset - 1));
  return forecastDate.toLocaleDateString('en-US', { weekday: 'long' });
};

// Map weather condition to emoji
const getWeatherIcon = (condition) => {
  const lower = condition.toLowerCase();
  if (lower.includes('sun') || lower.includes('clear')) return '☀️';
  if (lower.includes('cloud')) return '☁️';
  if (lower.includes('rain')) return '🌧️';
  if (lower.includes('storm') || lower.includes('thunder')) return '⛈️';
  if (lower.includes('snow')) return '❄️';
  if (lower.includes('wind')) return '🌬️';
  return '🌡️'; // default icon
};

function ForecastCard({ location }) {
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
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
              <p><strong>{getWeekdayName(day.day)}</strong></p>
              <p>Temp: {day.temperature}°C</p>
              <p>Humidity: {day.humidity}%</p>
              <p>Condition: {getWeatherIcon(day.condition)} {day.condition}</p>
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


