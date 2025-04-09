import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/WeatherCard.css';

function WeatherCard() {
  const { location } = useParams();
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        setLoading(true);  // Start loading
        const response = await fetch(`http://localhost:5000/weather/search?location=${location}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch weather data');
        }

        const data = await response.json();

        // Check if location data is valid
        if (!data || !data.temp) {
          throw new Error('Location not found');
        }

        setWeather(data);
      } catch (err) {
        setError(err.message);  // Handle errors
      } finally {
        setLoading(false);  // End loading
      }
    };

    fetchWeatherData();
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


