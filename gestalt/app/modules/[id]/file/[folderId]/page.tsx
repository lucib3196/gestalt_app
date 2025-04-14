"use client";
import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { useRouter } from "next/navigation";
import api from "@/api";

interface FileResponse {
  id: number;
  name: string;
  content: string;
  save_name: string | null;
  folder_id: number;
}

const FileNameMap: Record<string, string> = {
  question_txt: "question.txt",
  question_html: "question.html",
  server_js: "server.js",
  server_py: "server.py",
  solution_html: "solution.html",
  metadata: "info.json",
};

interface FileTableProps {
  files: FileResponse[];
}

const FilesTable: React.FC<FileTableProps> = ({ files }) => {
  const router = useRouter();

  const renderFile = (file: FileResponse) => {
    return (
      <tr key={file.id}>
        <td>
          <button className="btn btn-link p-0 text-start">
            {FileNameMap[file.name] || file.name}
          </button>
        </td>
      </tr>
    );
  };
  return (
    <>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>File Names</th>
          </tr>
        </thead>
        <tbody>{files.map(renderFile)}</tbody>
      </table>
    </>
  );
};

const FilePage: React.FC = () => {
  const [files, setFiles] = useState<FileResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const params = useParams();
  const module_id = params.id as string;
  const folder_id = params.folderId as string;

  const fetchFiles = async () => {
    setLoading(true);
    try {
      console.log(module_id, folder_id);
      const response = await api.get(
        `/modules/simple/${module_id}/${folder_id}/get_all_files`
      );
      console.log(response.data);
      setFiles(response.data);
    } catch (error) {
      console.log("There was an error getting the folder contents", error);
    } finally {
      setLoading(false);
    }
  };

  const DownLoadButton: React.FC = () => {
    const handleDownload = async () => {
      try {
        console.log(module_id, folder_id);

        const response = await api.get(
          `/modules/simple/${module_id}/${folder_id}/download`,
          {
            responseType: "blob", // 👈 Important for binary files
          }
        );

        // Get the filename from Content-Disposition header
        const disposition = response.headers["content-disposition"];
        const filenameMatch = disposition?.match(/filename="?(.+?)"?$/);
        const filename = filenameMatch?.[1] || "module.zip";

        // Create a Blob URL and trigger download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error(
          "There was an error downloading the folder contents",
          error
        );
      }
    };

    return (
      <>
        <button className="btn btn-primary" onClick={handleDownload}>
          Download Files
        </button>
      </>
    );
  };

  useEffect(() => {
    fetchFiles();
  }, [folder_id, module_id]);

  return (
    <div className="container-fluid m-4">
      
      {loading ? <p>Loading folders...</p> : <FilesTable files={files} />}
      <DownLoadButton />
    </div>
  );
};

export default FilePage;
