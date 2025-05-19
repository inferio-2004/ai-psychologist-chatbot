import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Signup.css";

const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    phone: "",
    role: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.role) {
      alert("Please select a role (Patient or Psychotherapist).");
      return;
    }

    console.log("Signing up:", formData);
    // TODO: Call backend API to register user

    navigate("/login"); // Redirecting to login after signup
  };

  return (
    <div className="sign-up-container">
      <h2 style={{color:"white"}}>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Username</label>
          <input type="text" name="username" value={formData.username} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Phone Number</label>
          <input type="tel" name="phone" value={formData.phone} onChange={handleChange} required />
        </div>

        <div className="form-group">
          <label>Role</label>
          <select name="role" value={formData.role} onChange={handleChange} required>
            <option value="">Select</option>
            <option value="patient">Patient</option>
            <option value="psychotherapist">Psychotherapist</option>
          </select>
        </div>

        <button type="submit" className="signup-btn">Sign Up</button>
      </form>

      <p style={{ color: "grey" }}>Already have an account? 
        <button className="signup-btn" onClick={() => navigate("/login")}>Log in</button>
      </p>
    </div>
  );
};

export default Signup;  
