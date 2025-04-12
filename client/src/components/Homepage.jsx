import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ForecastCard from './ForecastCard';
import '../styles/Homepage.css';
import { API_BASE } from '../config';

function Homepage() {
  const [randomLocation, setRandomLocation] = useState(null);

  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const response = await fetch(`${API_BASE}/saved-locations`);
        if (!response.ok) throw new Error('Failed to fetch locations');
        const data = await response.json();
        const locations = data.map(item => item.location_name);
        const randomLoc = locations[Math.floor(Math.random() * locations.length)] || 'New York';
        setRandomLocation(randomLoc);
      } catch (err) {
        console.error('Error fetching locations:', err);
        setRandomLocation('New York');
      }
    };
    fetchLocations();
  }, []);

  return (
    <div className="homepage">
      <section className="hero-section">
        <div className="hero-overlay">
          <div className="hero-content">
            <h1>Welcome to Weather Watch Lite ☀️</h1>
            <p>Track weather in real time, save favorite locations, and get a 7-day forecast—wherever you are.</p>
            <div className="hero-buttons">
              <Link to="/newsletter" className="btn primary-btn">Subscribe to Newsletter</Link>
            </div>
          </div>
        </div>
      </section>
      <section className="preview-forecast">
        <div className="forecast-container">
          <h2>{randomLocation ? `7-Day Forecast for ${randomLocation}` : 'Loading forecast...'}</h2>
          {randomLocation && <ForecastCard location={randomLocation} />}
        </div>
      </section>
    </div>
  );
}

export default Homepage;


