import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';
import SearchBar from './SearchBar';
import { API_BASE } from '../config';

function Dashboard() {
  const [savedLocations, setSavedLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchSavedLocations = async () => {
    try {
      const response = await fetch(`${API_BASE}/saved-locations`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to fetch locations");
      }
      const data = await response.json();
      setSavedLocations(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSavedLocations();
  }, []);

  const handleLocationClick = (location) => {
    navigate(`/forecast/${encodeURIComponent(location.location_name)}`);
  };

  const handleLocationSaved = (newLocation) => {
    setSavedLocations((prev) => {
      if (prev.some((loc) => loc.id === newLocation.id || loc.location_name === newLocation.location_name)) {
        return prev;
      }
      return [...prev, newLocation];
    });
  };

  const handleDeleteLocation = async (id) => {
    try {
      const response = await fetch(`${API_BASE}/saved-locations/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete location');
      }

      // Update state to remove the deleted location
      setSavedLocations((prev) => prev.filter((loc) => loc.id !== id));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="dashboard">
      <h2>Saved Locations</h2>
      {savedLocations.length === 0 ? (
        <p>No saved locations available</p>
      ) : (
        <ul>
          {savedLocations.map((location) => (
            <li key={location.id} style={{ display: 'flex', alignItems: 'center' }}>
              <span
                onClick={() => handleLocationClick(location)}
                style={{ cursor: 'pointer', flexGrow: 1 }}
              >
                {location.location_name}
              </span>
              <button
                onClick={() => handleDeleteLocation(location.id)}
                style={{ marginLeft: '10px', color: 'red' }}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
      <SearchBar onLocationSaved={handleLocationSaved} />
    </div>
  );
}

export default Dashboard;

