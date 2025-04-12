import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SearchBar.css';
import { API_BASE } from '../config';

function SearchBar({ onLocationSaved }) {
  const [location, setLocation] = useState('');
  const [error, setError] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [isLocationValid, setIsLocationValid] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();

    if (location.trim() === '') {
      setError('Please enter a location.');
      return;
    }

    setError('');
    setIsLoading(true);

    try {
      const data = await fetchWeatherData(location);
      if (data && data.current_temperature) {
        setWeatherData(data);
        setIsLocationValid(true);
      } else {
        setError('Unable to retrieve weather data.');
        setWeatherData(null);
        setIsLocationValid(false);
      }
    } catch (err) {
      setError(err.message);
      setWeatherData(null);
      setIsLocationValid(false);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchWeatherData = async (location) => {
    const response = await fetch(`${API_BASE}/weather-data?location=${encodeURIComponent(location)}`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Failed to fetch weather data');
    }
    return await response.json();
  };

  const handleSave = async () => {
    try {
      const response = await fetch(`${API_BASE}/saved-locations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location_name: location }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Failed to save location');
      }

      const savedData = await response.json();
      if (onLocationSaved) {
        onLocationSaved({
          id: savedData.id,
          user_id: savedData.user_id,
          location_name: savedData.location_name,
          created_at: savedData.created_at || new Date().toISOString(),
        }); // Ensure data matches savedLocations structure
      }
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter city or country"
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {isLocationValid && !isLoading && (
        <div className="save-button fade-in">
          <button onClick={handleSave}>Save Location</button>
        </div>
      )}

      {weatherData && !isLoading && (
        <div className="weather-preview">
          <p>Temperature: {weatherData.current_temperature}°C</p>
          <p>Condition: {weatherData.weather_condition}</p>
          <p>Humidity: {weatherData.current_humidity}%</p>
          <p>Wind Speed: {weatherData.current_wind_speed} km/h</p>
        </div>
      )}
    </div>
  );
}

export default SearchBar;