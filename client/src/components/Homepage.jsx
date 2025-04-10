import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import ForecastCard from './ForecastCard';
import '../styles/Homepage.css';

function Homepage() {
  const [randomLocation, setRandomLocation] = useState(null);

  useEffect(() => {
    // List of new locations
    const locations = [
      'New Joshuastad', 'Terrellborough', 'Smithmouth', 'Molinabury', 'North Jennifer', 
      'Orrstad', 'Lake Monique', 'Chadburgh', 'Karenfort', 'Dustinmouth', 'Mcdonaldchester', 
      'Lake Michael', 'Ericksonburgh', 'Ericahaven', 'Keithville', 'West Kevinland', 
      'North Jasmine', 'Marquezshire', 'East Elizabeth', 'Lake Drew', 'Chenshire', 
      'Stevenland', 'West James', 'South Charlesmouth', 'Grantfort', 'Wintersmouth', 
      'Kristimouth', 'New Dalton', 'New Stephanie', 'Lake Robert'
    ];

    // Select a random location from the list
    const randomLoc = locations[Math.floor(Math.random() * locations.length)];
    setRandomLocation(randomLoc);
  }, []);

  return (
    <div className="homepage">
      <section className="hero-section">
        <div className="hero-overlay">
          <div className="hero-content">
            <h1>Welcome to Weather Watch Lite ☀️</h1>
            <p>Track weather in real time, save favorite locations, and get a 7-day forecast—wherever you are.</p>
            <div className="hero-buttons">
              <Link to="/signup" className="btn primary-btn">Get Started</Link>
              <Link to="/login" className="btn secondary-btn">Login</Link>
            </div>
          </div>
        </div>
      </section>

      <section className="preview-forecast">
        <div className="forecast-container">
          <h2>{randomLocation ? `7-Day Forecast for ${randomLocation}` : 'Loading forecast...'}</h2>
          {/* Show ForecastCard only when randomLocation is set */}
          {randomLocation && <ForecastCard location={randomLocation} />}
        </div>
      </section>

      <noscript>
        <p className="no-js-warning">JavaScript is required to view the forecast. Please enable it in your browser settings.</p>
      </noscript>
    </div>
  );
}

export default Homepage;



