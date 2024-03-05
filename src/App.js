import React from "react";
import { Routes, Route } from "react-router-dom";
import EnterManagement from "./EnterManagement";
import UserManagement from "./UserManagement";
import ResourceManagement from "./ResourceManagement";
function App() {
  return (
    <div className="App">   
      <Routes>
        <Route path="/" element={<EnterManagement/>}></Route>
        <Route path="/home" element={ <UserManagement />}></Route>
      </Routes>
      <ResourceManagement />
    </div>
  );
}

export default App;
