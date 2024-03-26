import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
import './UserManagement.css'; // You can uncomment and use this if you have a CSS file.

// UserManagement component for handling projects.
const UserManagement = () => {
  // State variables for form fields.
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [projectDescription, setProjectDescription] = useState("");

  const [existingProjectIdToUse, setExistingProjectIdToUse] = useState("");
  const [existingProjectIdToJoin, setExistingProjectIdToJoin] = useState("");

  const [projectList, setProjectList] = useState("");

  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;
  const userId = location.state.id;

  const onLogout = async () => {
    await fetch("/logout/", {
      method: "POST"
    })
    navigate('/')
  };

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

  const onUseExistingProject = async (existingProjectIdToUse) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/project/get/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'projectid': existingProjectIdToUse})
    })
    await fetch("/project/getTry/", requestOptions)
    .then(response => response.json())
    .then(data =>  {
      if (data.message.includes("Success!")) {
        navigate('/project/' + existingProjectIdToUse, {state: {"id": userId, "username": username, "projectid": existingProjectIdToUse}});
      } else {
        alert(data.message);
      }
    })
  };

  const onJoinExistingProject = async (existingProjectIdToJoin) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/project/join/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'projectid': existingProjectIdToJoin})
    })
    await fetch("/project/joinTry/", requestOptions)
    .then(response => response.json())
    .then(data =>  {
      if (data.message.includes("Success!")) {
        navigate('/project/' + existingProjectIdToJoin, {state: {"id": userId, "username": username, "projectid": existingProjectIdToJoin}});
      } else {
        alert(data.message);
      }
    })
  };

  // Handle log out.
  const handleLogoutSubmit = (event) => {
    event.preventDefault();
    onLogout();
  };

  // Handle create new project form submission.
  const handleCreateProjectSubmit = (event) => {
    event.preventDefault();
    onCreateProject(projectName, projectId, projectDescription);
  };

  // Handle use existing project form submission.
  const handleUseExistingProjectSubmit = (event) => {
    event.preventDefault();
    onUseExistingProject(existingProjectIdToUse);
  };

  // Handle join existing project form submission.
  const handleJoinExistingProjectSubmit = (event) => {
    event.preventDefault();
    onJoinExistingProject(existingProjectIdToJoin);
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

      <div className="logout-container">
        <form
          className="logout-form"
          onSubmit={handleLogoutSubmit}
        >
          <button type="submit">Log out</button>
        </form>
      </div>

      <div className="use-existing-project-container">
        <form
          className="use-existing-project-form"
          onSubmit={handleUseExistingProjectSubmit}
        >
          <h2>Use Existing Project</h2>
          <input
            type="text"
            placeholder="Existing Project ID"
            value={existingProjectIdToUse}
            onChange={(e) => setExistingProjectIdToUse(e.target.value)}
          />
          <button type="submit">Use Project</button>
        </form>
        {/* <p>Existing Projects: {JSON.stringify(projectList)}</p> */}
      </div>

      <div className="join-existing-project-container">
        <form
          className="join-existing-project-form"
          onSubmit={handleJoinExistingProjectSubmit}
        >
          <h2>Join Existing Project</h2>
          <input
            type="text"
            placeholder="Existing Project ID"
            value={existingProjectIdToJoin}
            onChange={(e) => setExistingProjectIdToJoin(e.target.value)}
          />
          <button type="submit">Join Project</button>
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
              <div className="project-joined-or-not">Joined: {JSON.parse(JSON.stringify(project.authusers)).includes(username).toString()}</div>
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
