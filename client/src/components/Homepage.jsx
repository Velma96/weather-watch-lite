import { Link } from 'react-router-dom';
import ForecastCard from './ForecastCard';
import '../styles/Homepage.css';

function Homepage() {
  return (
    <div className="homepage">
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to Weather Watch Lite ☀️</h1>
          <p>Track weather in real time, save favorite locations, and get a 7-day forecast—wherever you are.</p>
          <div className="hero-buttons">
            <Link to="/signup" className="btn">Get Started</Link>
            <Link to="/login" className="btn btn-secondary">Login</Link>
          </div>
        </div>
      </section>

      <section className="preview-forecast">
        <h2>Today's Forecast for Nairobi</h2>
        <ForecastCard location="Nairobi" />
      </section>
    </div>
  );
}

export default Homepage;

