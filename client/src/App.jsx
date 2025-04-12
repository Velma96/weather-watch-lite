import { Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Homepage from './components/Homepage';
import Dashboard from './components/Dashboard';
import LocationForecast from './components/LocationForecast';
import NewsletterSignup from './components/NewsletterSignup';
import './styles/App.css';

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/forecast/:location" element={<LocationForecast />} />
        <Route path="/newsletter" element={<NewsletterSignup />} />
      </Routes>
      <Footer />
    </>
  );
}

export default App;

