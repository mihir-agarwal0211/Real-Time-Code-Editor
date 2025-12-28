import React, { useState, useEffect, useRef } from "react";
import { Editor } from "@monaco-editor/react";
import { v4 as uuidv4 } from "uuid";  // ✅ Import UUID
import { API_BASE_URL } from "../config";


const CodeEditor = () => {
  const [code, setCode] = useState("// Write your code here...");
  const userId = useRef(uuidv4());  // ✅ Generate unique user ID per session
  const [suggestions, setSuggestions] = useState(null);
  const [decorations, setDecorations] = useState([]); // Store cursor decorations
  const [cursorPosition, setCursorPosition] = useState({});
  const [role, setRole] = useState("new");
  const [username, setUsername] = useState(null);

  const socket = useRef(null);
  const editorRef = useRef(null);

  // ✅ Fetch Role from JWT Token
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split(".")[1])); // Decode JWT payload
        setRole(payload.role);
        setUsername(payload.sub);
        console.log("User Role:", payload.role);
        console.log("User Role2:", role);
      } catch (error) {
        console.error("Failed to decode token:", error);
      }
    }
  }, []);

  useEffect(() => {
    console.log("🎯 Role updated in state:", role);
  }, [role]);  // ✅ Runs whenever `role` changes
  

  // ✅ Establish WebSocket connection
  useEffect(() => {
    const WS_URL = API_BASE_URL.replace("http", "ws");
    socket.current = new WebSocket(`${WS_URL}/ws/test-session`);

    socket.current.onopen = () => console.log("✅ Connected to WebSocket server");

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "code") {
        setCode(data.content);
      } else if (data.type === "cursor") {
        setCursorPosition((prev) => ({ ...prev, [data.user]: data.cursor })); 
        console.log("📌 Updated Cursor Positions:", cursorPosition);
      }
    };

    socket.current.onclose = () => console.log("❌ Disconnected from WebSocket server");
    socket.onerror = (error) => console.error("WebSocket error:", error);
    return () => socket.current.close();
  }, []);

  // ✅ Apply Cursor Decorations
  useEffect(() => {
    if (editorRef.current && window.monaco) {
      const editor = editorRef.current;
      const monacoInstance = window.monaco;

      let newDecorations = [];

      Object.entries(cursorPosition).forEach(([user, position]) => {
        console.log(`🎨 Applying Cursor Decoration for ${user}:`, position); // Debugging

        newDecorations.push({
          range: new monacoInstance.Range(
            position.lineNumber,
            position.column,
            position.lineNumber,
            position.column + 1
          ),
          options: {
            className: "cursor-marker",
            isWholeLine: false,
            inlineClassName: "cursor-highlight",
          },
        });
      });

      // ✅ Apply new decorations
      const appliedDecorations = editor.deltaDecorations(decorations, newDecorations);
      setDecorations(appliedDecorations);

      console.log("✅ Decorations Applied:", appliedDecorations);
    }
  }, [cursorPosition]); // Runs every time cursorPosition updates

  // ✅ Handle Code Changes
  const handleCodeChange = (newCode) => {
    if (!role) {
      console.warn("🚨 Role not set yet, preventing edit.");
      return;
    }
  
    if (role === "viewer") {
      console.warn("🚨 Editing disabled for viewers.");
      return;  // 🚫 Prevent editing
    }
    setCode(newCode);
    if (socket.current?.readyState === WebSocket.OPEN) {
      socket.current.send(JSON.stringify({ type: "code", content: newCode }));
    }
  };
  // 🛠️ Call the AI Debugging API
  const handleDebug = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/debug`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      const data = await response.json();
      console.log("🐞 Debugging Response:", data);
      setSuggestions(data.suggestions); // Save AI suggestions
    } catch (error) {
      console.error("Debugging failed:", error);
    }
  };

  // 🛠️ Apply AI-Suggested Fix
  const applyFix = () => {
    if (suggestions && suggestions.includes("fixed_code")) {
      const match = suggestions.match(/```json\n([\s\S]*?)\n```/);
      if (match){ 
        console.log("match ->", match[1]);
        const cleanJSON = match[1]
        // // .replace(/\\n/g, "") // Convert escaped newlines
        // .replace(/\\"/g, "")   // Convert escaped double quotes
        // .trim(); 
        const parsedData = JSON.parse(cleanJSON);
        console.log("🛠️ Applying Fix:", cleanJSON);
        console.log("Parsed Data:", parsedData["fixed_code"]);
        setCode(parsedData["fixed_code"]);
      }
      else console.log("No Match available");
    }
    else console.log("No fix available");
  };
  // ✅ Handle Cursor Position Updates
  const handleCursorChange = (event) => {
    if (socket.current?.readyState === WebSocket.OPEN) {
      const position = event.position;
      const cursorUpdate = {
        type: "cursor",
        user: userId.current, // Replace with dynamic username
        cursor: position,
      };

      console.log("📤 Sending Cursor Update:", JSON.stringify(cursorUpdate));
      socket.current.send(JSON.stringify(cursorUpdate));
    }
  };

  return (
    <div style={{ height: "60vh", border: "1px solid #ccc" }}>
        <p><strong>👤 User:</strong> {username || "Loading..."}</p>
        <p><strong>🔑 Role:</strong> {role || "Loading..."}</p>
      <Editor
        height="100%"
        language="python"
        theme="vs-dark"
        value={code}
        options={{ readOnly: role === "viewer" }}
        onChange={handleCodeChange}
        onMount={(editor, monaco) => {
          editorRef.current = editor;
          window.monaco = monaco;
          editor.onDidChangeCursorPosition(handleCursorChange);
        }}
      />

      {/* Debugging Button */}
      <button onClick={handleDebug} style={{ margin: "10px" }}>
        Debug Code
      </button>

      {/* Display AI Suggestions */}
      {suggestions && (
        <div style={{ marginTop: "10px", color: "red", fontWeight: "bold" }}>
          <strong>AI Suggestions:</strong>
          <p><strong>Error : </strong>{JSON.parse(suggestions.match(/```json\n([\s\S]*?)\n```/)[1]).error}</p>
          <p><strong>Suggestec fix : </strong>{JSON.parse(suggestions.match(/```json\n([\s\S]*?)\n```/)[1]).fixed_code}</p>
          {/* <pre>{JSON.stringify(suggestions, null, 2)}</pre> */}
          <button onClick={applyFix} style={{ marginTop: "5px" }}>
            Apply Fix
          </button>
        </div>
      )}
    </div>
  );
};

export default CodeEditor;