import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import './UserManagement.css'; // You can uncomment and use this if you have a CSS file.

// UserManagement component for handling projects.
const UserManagement = () => {
  // State variables for form fields.
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [projectDescription, setProjectDescription] = useState("");

  const [existingProjectId, setExistingProjectId] = useState("");

  const [projectList, setProjectList] = useState("");

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
    .then(response => response.json())
    .then(data =>  {
      if (data.message.includes("Success!")) {
        const projectid = data.projectid;
        navigate('/project/' + projectid, {state: {"id": userId, "username": username, "projectid": projectid}});
      } else {
        alert(data.message);
      }
    })
  };

  const onUseExistingProject = async (existingProjectId) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/project/get/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'projectid': existingProjectId})
    })
    await fetch("/project/getTry/", requestOptions)
    .then(response => response.json())
    .then(data =>  {
      if (data.message.includes("Success!")) {
        navigate('/project/' + existingProjectId, {state: {"id": userId, "username": username, "projectid": existingProjectId}});
      } else {
        alert(data.message);
      }
    })
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

  const getAllProjects = () => {
    const requestOptions = {
      method: "GET"
    };
    fetch("/project/getAll/", requestOptions)
    .then(response => response.json())
    .then(data => setProjectList(data.data));
  }

  useEffect(() => {
    getAllProjects();
  }, []);

  // Render method for the user management form.
  return (
    <div className="user-management-container">
      {/* Use existing project form */}
      <h1>Welcome, {username}!</h1>
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
        {/* <p>Existing Projects: {JSON.stringify(projectList)}</p> */}
      </div>
      
      {/* Render each project as a styled component */}
      <div className="existing-projects-list">
        {projectList &&
          projectList.map((project, index) => (
            <div key={index} className="project-item">
              <div className="project-name">{project.projectname}</div>
              <div className="project-id">ID: {project.projectid}</div>
              <div className="project-description">{project.description}</div>
            </div>
          ))}
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
      </div>
    </div>
  );
};

// Exporting UserManagement for use in other components.
export default UserManagement;
