import React from "react";
import { BrowserRouter as Router, Routes, Route,Navigate} from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import CodeEditor from "./components/CodeEditor";

// ✅ Function to Check Authentication
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem("token");

  if (!token) {
    alert("You must log in first!"); // ✅ Show alert message
    return <Navigate to="/" />;
  }
  return children;
};
function App() {
  return (
    <Router>
      <div>
        <h1 style={{ textAlign: "center" }}>Real-Time Collaborative Code Editor</h1>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage/>} />
          <Route
          path="/editor"
          element={
            <ProtectedRoute>
              <CodeEditor />
            </ProtectedRoute>
          }
        />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
