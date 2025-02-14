import React, { useState, useEffect, useRef } from "react";
import { Editor } from "@monaco-editor/react";

const CodeEditor = () => {
  const [code, setCode] = useState("// Write your code here...");
  const [decorations, setDecorations] = useState([]); // Store cursor decorations
  const [cursorPosition, setCursorPosition] = useState({});

  const socket = useRef(null);
  const editorRef = useRef(null);

  // ✅ Establish WebSocket connection
  useEffect(() => {
    socket.current = new WebSocket("ws://127.0.0.1:8000/ws/test-session");

    socket.current.onopen = () => console.log("✅ Connected to WebSocket server");

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "code") {
        setCode(data.content);
      } else if (data.type === "cursor") {
        setCursorPosition((prev) => ({ ...prev, [data.user]: data.cursor }));
        console.log("📥 Received Cursor Update:", data);
      }
    };

    socket.current.onclose = () => console.log("❌ Disconnected from WebSocket server");

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
    setCode(newCode);
    if (socket.current?.readyState === WebSocket.OPEN) {
      socket.current.send(JSON.stringify({ type: "code", content: newCode }));
    }
  };

  // ✅ Handle Cursor Position Updates
  const handleCursorChange = (event) => {
    if (socket.current?.readyState === WebSocket.OPEN) {
      const position = event.position;
      const cursorUpdate = {
        type: "cursor",
        user: "User1", // Replace with dynamic username
        cursor: position,
      };

      // console.log("📤 Sending Cursor Update:", cursorUpdate);
      socket.current.send(JSON.stringify(cursorUpdate));
    }
  };

  return (
    <div style={{ height: "90vh", border: "1px solid #ccc" }}>
      <Editor
        height="100%"
        language="javascript"
        theme="vs-dark"
        value={code}
        onChange={handleCodeChange}
        onMount={(editor, monaco) => {
          editorRef.current = editor;
          window.monaco = monaco;
          editor.onDidChangeCursorPosition(handleCursorChange);
        }}
      />
    </div>
  );
};

export default CodeEditor;
