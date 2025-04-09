import { Link, useNavigate } from 'react-router-dom';
import '../styles/Navbar.css'; // Make sure this path matches your folder structure

function Navbar() {
  const isAuthenticated = !!localStorage.getItem('token');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="navbar-brand">Weather Watch Lite</Link>
      </div>
      <div className="navbar-right">
        {isAuthenticated ? (
          <>
            <Link to="/dashboard" className="nav-link">Dashboard</Link>
            <button onClick={handleLogout} className="nav-button logout-button">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/signup" className="nav-button signup-button">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;

