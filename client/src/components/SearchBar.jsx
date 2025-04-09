import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SearchBar.css';

function SearchBar() {
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
    setIsLoading(true); // start loading

    try {
      const data = await fetchWeatherData(location);
      if (data && data.temp) {
        setWeatherData(data);
        setIsLocationValid(true);
      } else {
        setError('Location not found. Please try again.');
        setWeatherData(null);
        setIsLocationValid(false);
      }
    } catch (err) {
      setError('Error fetching weather data. Please try again.');
      setWeatherData(null);
      setIsLocationValid(false);
    } finally {
      setIsLoading(false); // stop loading
    }
  };

  const fetchWeatherData = async (location) => {
    const response = await fetch(`http://localhost:5000/weather/search?location=${location}`);
    if (!response.ok) {
      throw new Error('Failed to fetch weather data');
    }
    return await response.json();
  };

  const handleSave = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setError('You must be logged in to save a location.');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/saved_locations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ location })
      });

      if (!response.ok) {
        throw new Error('Failed to save location');
      }

      navigate('/dashboard');
    } catch (err) {
      setError('Error saving location. Try again.');
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
        <button type="submit">Search</button>
      </form>

      {isLoading && <div className="loader"></div>}

      {error && <p>{error}</p>}

      {isLocationValid && !isLoading && (
        <div className="save-button fade-in">
          <button onClick={handleSave}>Save Location</button>
        </div>
      )}
    </div>
  );
}

export default SearchBar;






