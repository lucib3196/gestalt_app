type FileMeta = {
    displayName: string;
    language: string;
  };
export const FileNameMap: Record<string, FileMeta> = {
    question_txt: { displayName: "question.txt", language: "txt" },
    "question.html": { displayName: "question.html", language: "html" },
    "server.js": { displayName: "server.js", language: "javascript" },
    "server.py": { displayName: "server.py", language: "python" },
    "solution.html": { displayName: "solution.html", language: "html" },
    "info.json": { displayName: "info.json", language: "json" },
  };