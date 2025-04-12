import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/WeatherCard.css';
import { API_BASE } from '../config';

function WeatherCard() {
  const { location } = useParams();
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchWeather = async () => {
      try {
        const response = await fetch(`${API_BASE}/weather-data?location=${encodeURIComponent(location)}`);
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.error || 'Failed to fetch weather data');
        }
        const data = await response.json();
        setWeather({
          temp: data.current_temperature,
          condition: data.weather_condition,
          humidity: data.current_humidity,
          wind_speed: data.current_wind_speed,
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWeather();
  }, [location]);

  return (
    <div className="weather-card">
      {loading && <p>Loading weather data...</p>}
      {error && <p>Error: {error}</p>}
      {weather && !loading && !error && (
        <>
          <h3>{location}</h3>
          <p>Temperature: {weather.temp}°C</p>
          <p>Condition: {weather.condition}</p>
          <p>Humidity: {weather.humidity}%</p>
          <p>Wind Speed: {weather.wind_speed} km/h</p>
        </>
      )}
    </div>
  );
}

export default WeatherCard;
