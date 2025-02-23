import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("collaborator"); // Default role
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const id = Math.floor(Math.random() * 1000000); // Temporary ID

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    console.log("Registering:",id, username, password, role);
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/auth/register",
            null,
            {
                params: {  // ✅ Send data as query parameters
                    id,
                    username,
                    password,
                    role
                },
            headers: { "Content-Type": "application/json" } 
        }
          );
      console.log("Registration Successful:", response.data);
      alert("Registration successful! You can now log in.");
      navigate("/"); // ✅ Redirect to Login Page
    } catch (err) {
      console.error("Registration failed:", err);
      setError("Registration failed. Try a different username.");
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="collaborator">Collaborator</option>
          <option value="viewer">Viewer</option>
        </select>
        <button type="submit">Register</button>
      </form>
      <p>Already have an account? <a href="/">Login</a></p>
    </div>
  );
};

export default RegisterPage;
