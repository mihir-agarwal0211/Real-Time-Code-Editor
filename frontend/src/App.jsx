// import React from "react";
// import CodeEditor from "./components/CodeEditor";

// function App() {
//   return (
//     <div>
//       <h1>Real-Time Collaborative Code Editor</h1>
//       <CodeEditor />
//     </div>
//   );
// }

// export default App;

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CodeEditor from "./components/CodeEditor";

function App() {
  return (
    <Router>
      <Routes>
        {/* Route for the home page ("/") */}
        <Route path="/" element={<h1>Welcome to the App</h1>} />
        
        {/* Route for the code editor ("/editor") */}
        <Route path="/editor" element={<CodeEditor />} />
      </Routes>
    </Router>
  );
}

export default App;