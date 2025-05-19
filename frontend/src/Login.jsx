import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");

  const handleChange = (e) => {
    setUsername(e.target.value);
  };

  const handleLogin = (e) => {
    e.preventDefault();
    // Store the username in sessionStorage (this will clear automatically when the session ends)
    sessionStorage.setItem("username", username);
    // Route based on the username
    if (username.toLowerCase().includes("psychotherapist")) {
      navigate("/dashboard");
    } else {
      navigate("/chat");
    }
  };

  // Optionally clear sessionStorage on unload (if you want to force clearance even if sessionStorage persists)
  useEffect(() => {
    const handleUnload = () => {
      sessionStorage.clear();
    };
    window.addEventListener("beforeunload", handleUnload);
    return () => {
      window.removeEventListener("beforeunload", handleUnload);
    };
  }, []);

  return (
    <div className="login-container">
      <div className="left-section">
        <h1 className="topic">AI-Powered Mental Health Companion</h1>
        <p className="one-liner">
          An AI-driven chatbot for mental health support, bridging the gap between users and psychologists.
        </p>
        <div className="info">
          <br></br><br></br>
          <h2>About Us</h2>
          <p>
            Our AI-powered virtual psychotherapist interacts with users, detects emotional states, and generates structured reports for psychiatrists.
          </p>
        </div>
        
      </div>
      <div className="right-section">
        <h2>Welcome Back!</h2>
        
        <form onSubmit={handleLogin}>
          <input
            type="text"
            name="username"
            className="input-field"
            placeholder="Enter your username"
            value={username}
            onChange={handleChange}
            required
          />
          <input className="input-field" type="password" placeholder="Enter Your Password"/>
          <button type="submit" className="login-btn">
            Login Now
          </button>
          
        </form>
      </div>
    </div>
  );
};

export default Login;
