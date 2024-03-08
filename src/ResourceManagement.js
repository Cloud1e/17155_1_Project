import React, { useState } from "react";
import { useNavigate, useLocation } from 'react-router-dom';
// import './ResourceManagement.css'; // You can uncomment and use this if you have a CSS file.

const initialResources = {
  HWSet1: { capacity: 10, available: 10, request: 0 },
  HWSet2: { capacity: 8, available: 8, request: 0 },
};

const ResourceManagement = () => {
  const [resources, setResources] = useState(initialResources);
  const [addUsername, setAddUsername] = useState("");
  const [addUsernameMessage, setAddUsernameMessage] = useState("");
  const [addUsernameSuccess, setAddUsernameSuccess] = useState("");

  const [removeUsername, setRemoveUsername] = useState("");
  const [removeUsernameMessage, setRemoveUsernameMessage] = useState("");
  const [removeUsernameSuccess, setRemoveUsernameSuccess] = useState("");

  const navigate = useNavigate();
  const location = useLocation();
  const username = location.state.username;
  const userId = location.state.id;
  const projectid = location.state.projectid;

  // Update the request amount in the state
  const handleRequestChange = (set, value) => {
    const intValue = parseInt(value, 10) || 0;
    if (intValue < 0 || intValue > resources[set].capacity) {
      alert("Requested amount is out of range.");
      return;
    }
    setResources({
      ...resources,
      [set]: { ...resources[set], request: intValue },
    });
  };

  // Checkout resources
  const handleCheckout = (set) => {
    if (resources[set].request <= 0) {
      alert("Please enter a valid request amount.");
      return;
    }
    if (resources[set].available >= resources[set].request) {
      setResources({
        ...resources,
        [set]: {
          ...resources[set],
          available: resources[set].available - resources[set].request,
          // Reset request to 0 after checkout
          request: 0,
        },
      });
    } else {
      alert("Not enough resources available to fulfill the request.");
    }
  };

  // Checkin resources
  const handleCheckin = (set) => {
    const checkedOut = resources[set].capacity - resources[set].available;
    if (resources[set].request <= 0 || resources[set].request > checkedOut) {
      alert("Cannot check in more resources than were checked out.");
      return;
    }
    setResources({
      ...resources,
      [set]: {
        ...resources[set],
        available: resources[set].available + resources[set].request,
        // Reset request to 0 after checkin
        request: 0,
      },
    });
  };

  const onAddUserToProject = async ( addUsername ) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/project/addUser/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'addUsername': addUsername, 'projectid': projectid})
    })
    await fetch("/project/addUserTry/", requestOptions)
    .then(response => response.json())
    .then(data => {
      setAddUsernameSuccess(data.success);
      setAddUsernameMessage(data.message);
    })
  };

  const addUserToProjectMessage = () => {
    return (
    <div
      className="addUsernameMessage"
      style={{
        display: addUsernameMessage === "" ? 'none' : '',
      }}>
      <p>{addUsernameMessage}</p>
    </div>
    );
  };

  const onRemoveUserFromProject = async ( removeUsername ) => {
    const requestOptions = {
      method: "GET"
    }
    await fetch("/project/removeUser/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      // mode: "cors",
      body: JSON.stringify({'removeUsername': removeUsername, 'projectid': projectid, 'removedBy': username})
    })
    await fetch("/project/removeUserTry/", requestOptions)
    .then(response => response.json())
    .then(data => {
      setRemoveUsernameSuccess(data.success);
      setRemoveUsernameMessage(data.message);
    })
  };

  const onRemoveUserFromProjectFinal = async ( removeUsername, choice ) => {
    if (choice === 'Yes') {
      const requestOptions = {
        method: "GET"
      }
      await fetch("/project/removeUserFinal/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        // mode: "cors",
        body: JSON.stringify({'removeUsername': removeUsername, 'projectid': projectid})
      })
      await fetch("/project/removeUserFinalTry/", requestOptions)
      .then(response => response.json())
      .then(data => {
        setRemoveUsernameSuccess(data.success);
        setRemoveUsernameMessage(data.message);
        if (removeUsername === username) {
          navigate('/home/', {state: {"id": userId, "username": username}});
        }
      })
    } else if (choice === 'No') {
      setRemoveUsernameSuccess('False');
      setRemoveUsernameMessage('');
    }
  };

  const removeUserFromProjectMessage = () => {
    return (
    <div
      className="removeUsernameMessage"
      style={{
        display: removeUsernameMessage === "" ? 'none' : '',
      }}>
      <p>{removeUsernameMessage}</p>
      <form
        style={{
          display: removeUsernameSuccess === "Pending" ? '' : 'none',
        }}
        className="remove-user-from-project-final-form"
        onSubmit={handleRemoveUserFromProjectFinalSubmit}
      >
        <button type="submit">Yes</button>
        <button type="submit">No</button>
      </form>
    </div>
    );
  };

  // Handle adding user to project
  const handleAddUserToProjectSubmit = (event) => {
    event.preventDefault();
    onAddUserToProject(addUsername);
  };

  // Handle removing user from project (first check)
  const handleRemoveUserFromProjectSubmit = (event) => {
    event.preventDefault();
    onRemoveUserFromProject(removeUsername);
  };

  // Handle removing user from project (double check)
  const handleRemoveUserFromProjectFinalSubmit = (event) => {
    event.preventDefault();
    const choice = event.nativeEvent.submitter.textContent;
    onRemoveUserFromProjectFinal(removeUsername, choice);
  };

  return (
    <div className="resource-management-container">
      <div className="resources-header">
        <div className="header-item">Capacity</div>
        <div className="header-item">Available</div>
        <div className="header-item">Request</div>
        <div className="header-item">Actions</div>
      </div>
      {Object.keys(resources).map((set) => (
        <div key={set} className="resource-item">
          <div className="resource-capacity">{resources[set].capacity}</div>
          <div className="resource-available">{resources[set].available}</div>
          <input
            type="number"
            className="resource-request-input"
            min="0"
            max={resources[set].capacity}
            value={resources[set].request}
            onChange={(e) => handleRequestChange(set, e.target.value)}
          />
          <div className="resource-actions">
            <button onClick={() => handleCheckout(set)}>Checkout</button>
            <button onClick={() => handleCheckin(set)}>Checkin</button>
          </div>
        </div>
      ))}
      <div className="add-user-to-project-container">
        <form
          className="add-user-to-project-form"
          onSubmit={handleAddUserToProjectSubmit}
        >
          <h2>Add User To Project</h2>
          <input
            type="text"
            placeholder="Username to add"
            value={addUsername}
            onChange={(e) => setAddUsername(e.target.value)}
          />
          <button type="submit">Add</button>
        </form>
        <div className="addUserToProjectMessages">
          {addUserToProjectMessage()}
	      </div>
      </div>
      <div className="remove-user-from-project-container">
        <h2>Remove User From Project</h2>
        <form
          className="remove-user-from-project-form"
          onSubmit={handleRemoveUserFromProjectSubmit}
          style={{
            display: removeUsernameSuccess === "Pending" ? 'none' : '',
          }}
        >
          <input
            type="text"
            placeholder="Username to remove"
            value={removeUsername}
            onChange={(e) => setRemoveUsername(e.target.value)}
          />
          <button type="submit" id="remove-user-from-project-button">Remove</button>
        </form>
        <div className="removeUserFromProjectMessages">
          {removeUserFromProjectMessage()}
	      </div>
      </div>
    </div>
  );
};

export default ResourceManagement;
