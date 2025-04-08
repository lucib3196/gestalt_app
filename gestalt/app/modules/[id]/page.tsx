"use client";

import { useParams } from "next/navigation";
import { DataRenderer } from "@/components/DataRenderer";
import { Container } from "react-bootstrap";
import { Table } from "react-bootstrap";
import { useRouter } from 'next/navigation';

type FileResponse = {
  id: number;
  name: string;
  content: string;
  save_name: string | null;
  folder_id: number;
};

const FileNameMap: Record<string, string> = {
  question_txt: "question.txt",
  question_html: "question.html",
  server_js: "server.js",
  server_py: "server.py",
  solution_html: "solution.html",
  metadata: "info.json",
};

type ApiResponse = Array<FileResponse>

export default function SingleModule() {
  const router = useRouter();
  const params = useParams();
  const id = params.id as string;

  const source = {
    url: `/modules/simple/${id}/folder/file_contents`,
  };

  const loadingComponent = (
    <div className="text-center p-4">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );

  const errorComponent = (
    <div className="alert alert-danger">Error loading files</div>
  );

  const renderFiles = (rawData: ApiResponse, isLoading: boolean) => {
    console.log("API Response:", rawData);
    if (isLoading) return loadingComponent;

    // Safely handle the response data
    const files = rawData
    console.log("These are the files")
    console.log(files)

    return (
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>File Name</th>
          </tr>
        </thead>
        <tbody>
          {files.length > 0 ? (
            files.map((file) => (
              <tr key={file.id}>
                <td>
                  <button
                    className="btn btn-link p-0 text-start"

                    onClick={() => router.push(`/modules/${id}/file/${file.id}`)}
                  >
                    {FileNameMap[file.name] || file.name}
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td>No files found</td>
            </tr>
          )}
        </tbody>
      </Table>
    );
  };

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Module Files</h2>
      <DataRenderer<ApiResponse>
        source={source}
        loadingComponent={loadingComponent}
        errorComponent={errorComponent}
      >
        {renderFiles}
      </DataRenderer>
    </Container>
  );
}