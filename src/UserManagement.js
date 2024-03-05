import React, { useState } from "react";
// import './UserManagement.css'; // You can uncomment and use this if you have a CSS file.

// UserManagement component for handling projects.
const UserManagement = ({
  onCreateProject,
  onUseExistingProject,
}) => {
  // State variables for form fields.
  const [projectName, setProjectName] = useState("");
  const [projectDescription, setProjectDescription] = useState("");
  const [existingProjectId, setExistingProjectId] = useState("");

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

// Exporting UserManagement for use in other components.
export default UserManagement;
