"use client";

import { useParams } from "next/navigation";
import { Container, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import ResizableSidebar from "@/components/SideBar";
import "@/styles/DeveloperModeStyles.css";
import api from "@/api";
import Dropdown from "react-bootstrap/Dropdown";

type FileResponse = {
  id: number;
  name: string;
  content: string;
  save_name: string | null;
  folder_id: number;
};

type FileMeta = {
  displayName: string;
  language: string;
};

const FileNameMap: Record<string, FileMeta> = {
  question_txt: { displayName: "question.txt", language: "txt" },
  question_html: { displayName: "question.html", language: "html" },
  server_js: { displayName: "server.js", language: "javascript" },
  server_py: { displayName: "server.py", language: "python" },
  solution_html: { displayName: "solution.html", language: "html" },
  metadata: { displayName: "info.json", language: "json" },
};

type FileDropDownProps = {
  files: FileResponse[];
  onChange?: (value: string) => void;
};
import React from 'react';
import Editor from '@monaco-editor/react';
import CodeEditor from "@/components/CodeEditor";


type CodeEditorProps = {
  content?: string;
  language:string;
}

const DeveloperCodeEditor:React.FC<CodeEditorProps> = ({content, language}) =>{
  return (
    <Editor
      height="60vh"
      defaultLanguage={language}
      defaultValue={content ?? "//Start Typing"}
    />

  )
}






const CodeDropDown: React.FC<FileDropDownProps> = ({ files, onChange }) => {
  const [selectedLanguage, setSelectedLanguage] = useState("");

  // Define the language
  useEffect(() => {
    if (files.length > 0) {
      const defaultOption =
        FileNameMap[files[0].name].displayName || files[0].name;
      setSelectedLanguage(defaultOption);
      onChange?.(files[0].name);
    }
  }, [files]);

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedLanguage(event.target.value);
    console.log("Selected:", event.target.value);
    onChange?.(event.target.value);
  };

  const prepareOptions = () => {
    return files.map((file, id) => {
      return (
        <option
          key={file.name}
          value={FileNameMap[file.name].displayName || file.name}
        >
          {FileNameMap[file.name].displayName || file.name}
        </option>
      );
    });
  };
  return (
    <select
      id="code-dropdown"
      className="code_dropdown"
      onChange={handleChange}
      value={selectedLanguage}
    >
      {prepareOptions()}
    </select>
  );
};

const DeveloperMode: React.FC = () => {
  const [files, setFiles] = useState<FileResponse[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const params = useParams();
  const module_id = params.id as string;
  // const folder_id = params.folderId as string;
  const folder_id = 7;

  const fetchFiles = async () => {
    try {
      const response = await api.get(
        `/packages/simple/${module_id}/${folder_id}/get_all_files`
      );
      setFiles(response.data);
    } catch (error) {
      console.log("There was an error getting the folder contents", error);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [folder_id, module_id]);

  const handleDropDownChange = (value: string) => {
    setSelectedFile(value);
    console.log("Parent Received Selection", value);
  };

  return (
    <div className="developer_mode_container">
      <div className="developer_mode_header">
        <h1>Developer Mode</h1>
        {selectedFile && <p>You selected the option of {selectedFile}</p>}
        <div className="setting-container">
          <CodeDropDown files={files} onChange={handleDropDownChange} />
          <button>Style Settings</button>
          <button>Report Bug</button>
          <button>Finish Review</button>
        </div>
      </div>
      {selectedFile}
    </div>
  );
};

export default function QuizView() {
  const params = useParams();
  const moduleId = params.id as string;
  const fileId = params.fileId as string;

  const [quizHTML, setQuizHTML] = useState("");
  const [solutionHTML, setSolutionHTML] = useState("");
  const [csrfToken, setCsrfToken] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.post(`/quiz/adaptive_quiz/${moduleId}/7`);
        setQuizHTML(response.data);
      } catch (err) {
        console.error("Error loading quiz:", err);
      }
    };
    fetchData();
  }, [moduleId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    try {
      const response = await api.post("/quiz/grade", formData);
      console.log("Grading response:", response.data);
    } catch (err) {
      console.error("Submission error:", err);
    }
  };

  return (
    <>
      <Container className="mt-4">
        <form onSubmit={handleSubmit}>
          <h1 className="mb-4">
            Module: {moduleId}, File: {fileId}
          </h1>

          <div
            className="form-field mb-3"
            dangerouslySetInnerHTML={{ __html: quizHTML }}
          />
          {/* <div className="container mb-3" dangerouslySetInnerHTML={{ __html: solutionHTML }} /> */}

          <div className="quiz-btn-container mb-2">
            <Button type="submit" variant="primary">
              Submit
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => location.reload()}
            >
              New Variant
            </Button>
          </div>

          <div className="step-btn-container">
            <Button type="submit" name="action" value="hint" variant="info">
              Show Hint
            </Button>
          </div>
        </form>
      </Container>
      <DeveloperMode />
    </>
  );
}
