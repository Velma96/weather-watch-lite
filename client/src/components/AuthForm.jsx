import { useState } from 'react';
import '../styles/AuthForm.css'; 

function AuthForm({ isLogin, onSubmit }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Mock backend response simulation
  const mockBackendResponse = (endpoint, email, password) => {
    if (endpoint === '/users/signup') {
      // Simulate successful sign-up response
      return { token: 'mock-token-12345' };
    } else if (endpoint === '/users/login') {
      // Simulate successful login response
      if (email === 'awuorphoebi@gmail.com' && password === 'Test1234!') {
        return { token: 'mock-token-12345' };
      } else {
        throw new Error('Authentication failed. Invalid email or password.');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!email || !password) {
      setError('Please fill in both fields.');
      setLoading(false);
      return;
    }

    const endpoint = isLogin ? '/users/login' : '/users/signup';

    try {
      // Mock API Response
      const data = mockBackendResponse(endpoint, email, password);

      if (data.token) {
        onSubmit(data.token); // Pass token to parent component
      } else {
        setError('Authentication failed. No token received.');
      }
    } catch (error) {
      setError(error.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        className="input-field"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        className="input-field"
      />
      <button type="submit" disabled={loading} className="submit-button">
        {loading ? 'Loading...' : isLogin ? 'Log In' : 'Sign Up'}
      </button>
    </form>
  );
}

export default AuthForm;

