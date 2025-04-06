import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Table } from "react-bootstrap";
import api from "~/api";
import ModuleTableDetails from "~/components/ModuleTableDetails";

// Maps short identifiers to actual file names
const FileNameMap: Record<string, string> = {
  question_txt: "question.txt",
  question_html: "question.html",
  server_js: "server.js",
  server_py: "server.py",
  solution_html: "solution.html",
  metadata: "info.json",
};

type ResponseData = {
  content: string;
  folder_id: number;
  name: string;
  save_name: string;
  filename?: string;
};

// Adds filenames to each file entry using FileNameMap
function mapFileNames(data: Record<string, ResponseData>): Record<string, ResponseData> {
  const updated = { ...data };
  for (const [key, value] of Object.entries(updated)) {
    updated[key].filename = FileNameMap[value.name] || "Untitled.txt";
  }
  return updated;
}

type TableProps = {
  data: Record<string, ResponseData>;
};

function RenderTableRows({ data }: TableProps) {
  return (
    <>
      {Object.entries(data).map(([key, value]) => (
        <tr key={key}>
          <td>{value.filename}</td>
        </tr>
      ))}
    </>
  );
}

function RenderTable({ data }: TableProps) {
  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>File Name</th>
        </tr>
      </thead>
      <tbody>
        <RenderTableRows data={data} />
      </tbody>
    </Table>
  );
}

function ModuleDetails() {
  const [module, setModule] = useState<Record<string, ResponseData>>({});
  const { id } = useParams();

  useEffect(() => {
    const fetchModuleContent = async () => {
      try {
        const response = await api.get(`/modules/simple/${id}/folder/file_contents`);
        setModule(mapFileNames(response.data));
      } catch (error) {
        console.error("Error Fetching Content", error);
      }
    };

    if (id) fetchModuleContent();
  }, [id]);

  return (
    <div>
      <h2>Module Details</h2>
      <RenderTable data={module} />
    </div>
  );
}

export default ModuleDetails;
