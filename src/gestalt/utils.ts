type FileMeta = {
    displayName: string;
    language: string;
  };
export const FileNameMap: Record<string, FileMeta> = {
    question_txt: { displayName: "question.txt", language: "txt" },
    question_html: { displayName: "question.html", language: "html" },
    server_js: { displayName: "server.js", language: "javascript" },
    server_py: { displayName: "server.py", language: "python" },
    solution_html: { displayName: "solution.html", language: "html" },
    metadata: { displayName: "info.json", language: "json" },
  };