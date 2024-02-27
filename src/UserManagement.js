import React, { useState } from "react";
// import './UserManagementForm.css'; // You can uncomment and use this if you have a CSS file.

// UserManagementForm component for sign-in, creating new users, and handling projects.
const UserManagementForm = ({
  onSignIn,
  onCreateUser,
  onCreateProject,
  onUseExistingProject,
}) => {
  // State variables for form fields.
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [newUsername, setNewUsername] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [existingProjectId, setExistingProjectId] = useState("");

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

  // Handle create new project form submission.
  const handleCreateProjectSubmit = (event) => {
    event.preventDefault();
    onCreateProject(projectName, projectDescription);
  };

  // Handle use existing project form submission.
  const handleUseExistingProjectSubmit = (event) => {
    event.preventDefault();
    onUseExistingProject(existingProjectId);
  };

  // Render method for the user management form.
  return (
    <div className="user-management-container">
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

      {/* Use existing project form */}
      <div className="use-existing-project-container">
        <form
          className="use-existing-project-form"
          onSubmit={handleUseExistingProjectSubmit}
        >
          <h2>Use Existing Project</h2>
          <input
            type="text"
            placeholder="Existing Project ID"
            value={existingProjectId}
            onChange={(e) => setExistingProjectId(e.target.value)}
          />
          <button type="submit">Use Project</button>
        </form>
      </div>

      {/* Create new project form */}
      <div className="create-project-container">
        <form
          className="create-project-form"
          onSubmit={handleCreateProjectSubmit}
        >
          <h2>Create New Project</h2>
          <input
            type="text"
            placeholder="Project Name"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
          />
          <textarea
            placeholder="Project Description"
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
          />
          <button type="submit">Create Project</button>
        </form>
      </div>
    </div>
  );
};

// Exporting UserManagementForm for use in other components.
export default UserManagementForm;
