"use client";
import React, { useEffect, useState } from "react";
import api from "@/api";
import { useParams } from "next/navigation";

import { useRouter } from "next/navigation";
type Folder = {
  id: number; // folder_id
  title: string;
  package_id: number; // mod_id
}

interface FolderTableProps {
  folders: Folder[];
}

const FolderTable: React.FC<FolderTableProps> = ({ folders }) => {
  const router = useRouter();
  const renderRow = (folder: Folder) => {
    return (
      <tr key={folder.id}>
        <td>
          <button
            className="btn btn-link p-0 text-start"
            onClick={() =>
              router.push(`/modules/${folder.package_id}/file/${folder.id}`)
            }
          >
            {folder.title}
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
            <th>Folder Names</th>
          </tr>
        </thead>
        <tbody>{folders.map(renderRow)}</tbody>
      </table>
    </>
  );
};

const FolderPage: React.FC = () => {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const params = useParams();
  const id = params.id as string;

  // Fetch all folders for the module
  const fetchFolders = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/packages/simple/${id}/get_all_folders`);
      console.log(response.data);
      setFolders(response.data); //
    } catch (error) {
      console.error("There was an error getting the folders", error);
    } finally {
      setLoading(false);
    }
  };

  const DownLoadButton: React.FC = () => {
    const handleDownload = async () => {
      try {
        const response = await api.get(`/packages/simple/${id}/download`, {
          responseType: "blob",
        });
  
        const disposition = response.headers["content-disposition"];
        const filenameMatch = disposition?.match(/filename="?(.+?)"?$/);
        const filename = filenameMatch?.[1] || "module.zip";
  
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("There was an error downloading the folder contents", error);
      }
    };
  
    return (
      <button className="btn btn-primary mt-3" onClick={handleDownload}>
        Download All Folders
      </button>
    );
  };
  

  useEffect(() => {
    fetchFolders();
  }, [id]);

  return (
    <div className="container-fluid m-4">
      {loading ? <p>Loading folders...</p> : <FolderTable folders={folders} />}
      <DownLoadButton />
    </div>
  );
};

export default FolderPage;
