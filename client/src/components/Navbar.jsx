import { Link } from 'react-router-dom';
import '../styles/Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/" className="navbar-brand">Weather Watch Lite</Link>
      </div>
      <div className="navbar-right">
        <Link to="/dashboard" className="nav-link">Dashboard</Link>
        <Link to="/newsletter" className="nav-link">Newsletter</Link>
      </div>
    </nav>
  );
}

export default Navbar;
