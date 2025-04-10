import { Route, Routes, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import AuthForm from './components/AuthForm';
import Dashboard from './components/Dashboard';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Homepage from './components/Homepage'; // ✅ Import the Homepage
import LocationForecast from './components/LocationForecast'; // ✅ Import the LocationForecast component
import './styles/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) setIsAuthenticated(true);
  }, []);

  const handleAuth = (token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  return (
    <>
      <Navbar />
      <Routes>
        {/* ✅ Homepage route */}
        <Route path="/" element={<Homepage />} />

        {/* Dashboard route */}
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />

        {/* Location Forecast Route */}
        <Route
          path="/forecast/:location" // Route for location-specific forecast
          element={isAuthenticated ? <LocationForecast /> : <Navigate to="/login" />}
        />

        <Route
          path="/login"
          element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <AuthForm isLogin={true} onSubmit={handleAuth} />
          }
        />

        <Route
          path="/signup"
          element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <AuthForm isLogin={false} onSubmit={handleAuth} />
          }
        />
      </Routes>
      <Footer />
    </>
  );
}

export default App;

