import { useEffect, useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import '../styles/Dashboard.css';
import SearchBar from './SearchBar';

function Dashboard() {
  const [savedLocations, setSavedLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [redirect, setRedirect] = useState(false);

  const navigate = useNavigate(); // Hook for navigation

  const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5555';

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setRedirect(true);
      return;
    }

    const fetchSavedLocations = async () => {
      try {
        const response = await fetch(`${backendUrl}/saved-locations`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const contentType = response.headers.get('Content-Type');
        if (!contentType || !contentType.includes('application/json')) {
          throw new Error('Invalid JSON response');
        }

        const data = await response.json();
        setSavedLocations(data);
      } catch (error) {
        console.error('Error fetching saved locations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSavedLocations();
  }, [backendUrl]);

  if (redirect) {
    return <Navigate to="/login" />;
  }

  if (loading) return <div>Loading...</div>;

  const handleLocationClick = (location) => {
    // Navigate to the location-specific forecast page
    navigate(`/forecast/${location}`);
  };

  return (
    <div className="dashboard">
      <h2>Your Saved Locations</h2>
      {savedLocations.length === 0 ? (
        <p>You have no saved locations</p>
      ) : (
        <ul>
          {savedLocations.map((location) => (
            <li
              key={location.id}
              onClick={() => handleLocationClick(location.location_name)}
              style={{ cursor: 'pointer' }}
            >
              {location.location_name}
            </li>
          ))}
        </ul>
      )}

      <SearchBar />
    </div>
  );
}

export default Dashboard;


