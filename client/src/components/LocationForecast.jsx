import { useParams } from 'react-router-dom';
import ForecastCard from './ForecastCard';

function LocationForecast() {
  const { location } = useParams(); // Get location from the URL parameter

  return (
    <div className="location-forecast">
      <h2>Weather Forecast for {location}</h2>
      <ForecastCard location={location} /> {/* Use ForecastCard for the selected location */}
    </div>
  );
}

export default LocationForecast;
