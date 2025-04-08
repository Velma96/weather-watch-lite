import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SearchBar.css';

function SearchBar() {
  const [location, setLocation] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();  // Prevent page reload on form submit

    if (location.trim() !== '') {
      navigate(`/weather/${location}`); // Navigate to the weather page with the searched location
    }
  };

  return (
    <div className="search-bar">
      <form onSubmit={handleSearch}> {/* Use form to handle submit */}
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter city or country"
        />
        <button type="submit">Search</button> {/* Use submit type for button */}
      </form>
    </div>
  );
}

export default SearchBar;


