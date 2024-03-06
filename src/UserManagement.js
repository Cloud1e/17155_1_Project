import React, { useState } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
// import './UserManagement.css'; // You can uncomment and use this if you have a CSS file.

// UserManagement component for handling projects.
const UserManagement = ({
  onUseExistingProject,
}) => {
  // State variables for form fields.
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [createProjectError, setCreateProjectError] = useState("");

  const [existingProjectId, setExistingProjectId] = useState("");

  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;
  const userId = location.state.id;

  const onCreateProject = async (projectName, projectId, projectDescription) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/project/create/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'projectname': projectName,
        'projectid': projectId,
        'description': projectDescription,
        'authusers': username})
    })
    await fetch("/project/createTry/", requestOptions)
    .then(async data => {
      const jsonMessage = await data.json();
      if (jsonMessage.message.includes("Success!")) {
        const projectid = jsonMessage.projectid;
        navigate('/project/' + projectid);
      } else {
        setCreateProjectError(jsonMessage.message);
      }
    })
  }

  const createProjectErrorMessage = () => {
    return (
    <div
      className="createProjectError"
      style={{
        display: createProjectError === "" ? 'none' : '',
      }}>
      <p>{createProjectError}</p>
    </div>
    );
  };

  // Handle create new project form submission.
  const handleCreateProjectSubmit = (event) => {
    event.preventDefault();
    onCreateProject(projectName, projectId, projectDescription);
  };

  // Handle use existing project form submission.
  const handleUseExistingProjectSubmit = (event) => {
    event.preventDefault();
    onUseExistingProject(existingProjectId);
  };

  // Render method for the user management form.
  return (
    <div className="user-management-container">
      {/* Use existing project form */}
      <p>Welcome, {username}!</p>
      <p>Your ID: {userId}</p>
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
          <input
            type="text"
            placeholder="Project ID"
            value={projectId}
            onChange={(e) => setProjectId(e.target.value)}
          />
          <textarea
            placeholder="Project Description"
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
          />
          <button type="submit">Create Project</button>
        </form>
        <div className="createProjectMessages">
          {createProjectErrorMessage()}
	      </div>
      </div>
    </div>
  );
};

// Exporting UserManagement for use in other components.
export default UserManagement;
