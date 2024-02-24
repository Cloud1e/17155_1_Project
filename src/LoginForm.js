// Importing React hooks for managing state within the component.
import React, { useState } from "react";
// Importing CSS styles for the LoginForm component.
// import "./LoginForm.css";

// LoginForm component where users can sign in.
const LoginForm = ({ onSignIn }) => {
  // State variables for username and password.
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // Function to handle the form submission.
  const handleSubmit = (event) => {
    event.preventDefault(); // Preventing default form submit action.
    onSignIn(username, password); // Prop function to handle sign-in.
  };

  // Render method for the login form.
  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Sign In</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};

// Exporting LoginForm for use in other components.
export default LoginForm;
