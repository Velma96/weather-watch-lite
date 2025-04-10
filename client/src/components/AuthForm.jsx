import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/AuthForm.css";

const AuthForm = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ 
      ...formData, 
      [e.target.name]: e.target.value 
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newUser = {
      username: formData.username,
      email: formData.email,
      password_hash: formData.password // Match your backend’s expected key
    };

    try {
      const res = await fetch("http://localhost:5555/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newUser),
      });

      if (!res.ok) {
        const errorData = await res.json();
        setError(errorData.message || "Registration failed.");
        return;
      }

      const data = await res.json();
      console.log("Registered:", data);
      navigate("/dashboard"); // or wherever you redirect post-auth
    } catch (err) {
      setError("Server error. Please try again later.");
    }
  };

  return (
    <div className="auth-form-container">
      <h2>Sign Up</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          type="text"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          name="password"
          type="password"
          placeholder="Password (min 6 chars)"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">Create Account</button>
      </form>
    </div>
  );
};

export default AuthForm;


