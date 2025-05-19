import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import PsychotherapistDashboard from "./PsychotherapistDashboard";
import ChatBot from "./Chatbot";

const App = () => {
  return (
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<PsychotherapistDashboard />} />
          <Route path="/chat" element={<ChatBot />} />
        </Routes>
  );
};

export default App;
