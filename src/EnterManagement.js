// Importing React hooks for managing state within the component.
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
// Importing CSS styles for the EnterManagement component.
// import "./EnterManagement.css";

// EnterManagement component where users can sign in & sign up.
const EnterManagement = () => {
  // State variables for username and password.
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const navigate = useNavigate();

  const onSignIn = async ( username, password ) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/login/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'username': username, 'password': password})
    })
    await fetch("/loginTry/", requestOptions)
    .then(response => response.json())
    .then(data => {
      if (data.message.includes("Success!")) {
        const id = data.id;
        navigate('/home/', {state: {"id": id, "username": username}});
      } else {
        alert(data.message);
      }
    })
  };

  const onCreateUser = async ( newUsername, newPassword ) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/createUser/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'username': newUsername, 'password': newPassword})
    })
    await fetch("/createUserTry/", requestOptions)
    .then(response => response.json())
    .then(data => {
      if (data.message.includes("Success!")) {
        const id = data.id;
        navigate('/home/', {state: {"id": id, "username": newUsername}});
      } else {
        alert(data.message);
      }
    })
  };

  // Handle sign-in form submission.
  const handleSignInSubmit = (event) => {
    event.preventDefault();
    onSignIn(username, password);
  };

  // Handle create new user form submission.
  const handleCreateUserSubmit = (event) => {
    event.preventDefault();
    onCreateUser(newUsername, newPassword);
  };

  // Render method for the login form.
  return (
    <div className="enter-management-container">
      {/* Sign-in form */}
      <div className="login-container">
        <form className="login-form" onSubmit={handleSignInSubmit}>
          <h2>User Sign In</h2>
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

      {/* Create user form */}
      <div className="create-user-container">
        <form className="create-user-form" onSubmit={handleCreateUserSubmit}>
          <h2>Create New User</h2>
          <input
            type="text"
            placeholder="New Username"
            value={newUsername}
            onChange={(e) => setNewUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <button type="submit">Create User</button>
        </form>
      </div>
    </div>
  );
};

// Exporting EnterManagement for use in other components.
export default EnterManagement;
