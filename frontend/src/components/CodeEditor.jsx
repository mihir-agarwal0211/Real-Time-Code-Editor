import React, { useState, useEffect, useRef } from "react";
import { Editor } from "@monaco-editor/react";

const CodeEditor = () => {
  const [code, setCode] = useState("// Write your code here...");
  const [cursorPosition, setCursorPosition] = useState({});
  const socket = useRef(null);
  const editorRef = useRef(null);

  useEffect(() => {
    socket.current = new WebSocket("ws://127.0.0.1:8000/ws/test-session");

    socket.current.onopen = () => console.log("Connected to WebSocket server");

    socket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data);

      if (data.type === "code") {
        setCode(data.content);
      } else if (data.type === "cursor") {
        setCursorPosition((prev) => ({ ...prev, [data.user]: data.cursor }));
      }
    };

    socket.current.onclose = () => console.log("Disconnected from WebSocket server");

    return () => socket.current.close();
  }, []);

  useEffect(() => {
    if (editorRef.current) {
      const editor = editorRef.current;
  
      let decorations = [];
  
      Object.entries(cursorPosition).forEach(([user, position]) => {
        decorations = editor.deltaDecorations(decorations, [
          {
            range: new monaco.Range(position.lineNumber, 1, position.lineNumber, 1),
            options: {
              className: "cursor-marker",
              inlineClassName: "cursor-highlight",
            },
          },
        ]);
      });
    }
  }, [cursorPosition]); // 👈 Runs every time cursorPosition updates
  

  const handleCodeChange = (newCode) => {
    setCode(newCode);
    if (socket.current?.readyState === WebSocket.OPEN) {
      socket.current.send(JSON.stringify({ type: "code", content: newCode }));
    }
  };

  const handleCursorChange = (event) => {
    if (socket.current?.readyState === WebSocket.OPEN) {
      const position = event.position;
      socket.current.send(JSON.stringify({ type: "cursor", user: "User1", cursor: position }));
    }
  };

  return (
    <div style={{ height: "90vh", border: "1px solid #ccc" }}>
      <Editor
        height="100%"
        language="javascript"
        theme="vs-dark"
        value={code}
        onChange={(newCode) => {
          setCode(newCode);
          if (socket.current?.readyState === WebSocket.OPEN) {
            socket.current.send(JSON.stringify({ type: "code", content: newCode }));
          }
        }}
        onMount={(editor) => {
          editorRef.current = editor;
          editor.onDidChangeCursorPosition(handleCursorChange);
        }}
      />
    </div>
  );
};

export default CodeEditor;