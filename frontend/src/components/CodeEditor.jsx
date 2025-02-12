import React, { useState } from "react";
import { Editor } from "@monaco-editor/react";

const CodeEditor = () => {
  const [code, setCode] = useState("// Write your code here...");

  return (
    <div style={{ height: "90vh", border: "1px solid #ccc" }}>
      <Editor
        height="100%"
        language="javascript"
        theme="vs-dark"
        value={code}
        onChange={(newCode) => setCode(newCode)}
      />
    </div>
  );
};

export default CodeEditor;
