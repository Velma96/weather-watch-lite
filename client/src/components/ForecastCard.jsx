import { useState, useEffect } from 'react';
import '../styles/ForecastCard.css';
import { API_BASE } from '../config';

const getWeekdayName = (offset) => {
  const today = new Date();
  const forecastDate = new Date(today);
  forecastDate.setDate(today.getDate() + offset);
  return forecastDate.toLocaleDateString('en-US', { weekday: 'long' });
};

const getWeatherIcon = (condition) => {
  const lower = condition.toLowerCase();
  if (lower.includes('sun') || lower.includes('clear')) return '☀️';
  if (lower.includes('cloud')) return '☁️';
  if (lower.includes('rain')) return '🌧️';
  if (lower.includes('storm') || lower.includes('thunder')) return '⛈️';
  if (lower.includes('snow')) return '❄️';
  if (lower.includes('wind')) return '🌬️';
  return '🌡️';
};

function ForecastCard({ location }) {
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const response = await fetch(`${API_BASE}/weather-data?location=${encodeURIComponent(location)}`);
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.error || 'Failed to fetch forecast');
        }
        const data = await response.json();
        setForecast(data.forecast_data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchForecast();
  }, [location]);

  if (loading) {
    return <div className="forecast-card">Loading forecast...</div>;
  }

  if (error || !forecast) {
    return <div className="forecast-card error">Error: {error || 'No forecast data available'}</div>;
  }

  return (
    <div className="forecast-card">
      <h3>7-Day Forecast for {location}</h3>
      <div className="forecast-list">
        {forecast.map((day, index) => (
          <div key={index} className="forecast-day">
            <p><strong>{getWeekdayName(day.day - 1)}</strong></p>
            <p>Temp: {day.temperature}°C</p>
            <p>Humidity: {day.humidity}%</p>
            <p>Condition: {getWeatherIcon(day.condition)} {day.condition}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ForecastCard;


