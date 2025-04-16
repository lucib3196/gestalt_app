import React from 'react';
import Editor from '@monaco-editor/react';

function CodeEditor() {
  return (
    <Editor
      height="90vh"
      defaultLanguage="javascript"
      defaultValue="// Start coding..."
    />
  );
}

export default CodeEditor;
