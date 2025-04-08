import { Route, Routes, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import AuthForm from './components/AuthForm';
import Dashboard from './components/Dashboard';
import Navbar from './components/Navbar';
import Footer from './components/Footer'; // Footer component
import './styles/App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check for existing token on first load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleAuth = (token) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  return (
    <>
      <Navbar />
      <Routes>
        {/* Dashboard route - protected */}
        <Route
          path="/dashboard"  // Changed from '/' to '/dashboard'
          element={
            isAuthenticated ? (
              <Dashboard />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        {/* Login route - redirect to dashboard if already logged in */}
        <Route
          path="/login"
          element={
            isAuthenticated ? (
              <Navigate to="/dashboard" />  // Redirect to /dashboard after login
            ) : (
              <AuthForm isLogin={true} onSubmit={handleAuth} />
            )
          }
        />

        {/* Signup route - redirect to dashboard if already logged in */}
        <Route
          path="/signup"
          element={
            isAuthenticated ? (
              <Navigate to="/dashboard" />  // Redirect to /dashboard after signup
            ) : (
              <AuthForm isLogin={false} onSubmit={handleAuth} />
            )
          }
        />
      </Routes>
      <Footer />
    </>
  );
}

export default App;

