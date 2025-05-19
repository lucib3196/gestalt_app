import React from 'react';
import Editor from '@monaco-editor/react';

function CodeEditor({ content }: { content?: string }) {
  return (
    <Editor
      height="60vh"
      defaultLanguage="html"
      defaultValue={content ?? "//Start Typing"}
    />
  );
}


export default CodeEditor;
