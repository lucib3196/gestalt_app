import Editor from "@monaco-editor/react";

function CodeEditor() {
  return (
    <Editor
      height="400px"
      defaultLanguage="javascript"
      defaultValue="// write your code here"
      theme="vs-dark"
      onChange={(value) => console.log(value)}
    />
  );
}

export default CodeEditor