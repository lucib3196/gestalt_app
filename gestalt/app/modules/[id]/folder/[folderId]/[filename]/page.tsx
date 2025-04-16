// app/modules/[moduleId]/file/[fileId]/page.tsx
"use client";

import { useParams } from "next/navigation";
import { Container } from "react-bootstrap";
import { useState, useEffect } from "react";
import api from "@/api";

export default function FileViewPage() {
  const params = useParams();
  const moduleId = params.id as string;
  const fileId = params.fileId as string;

  console.log()

  const [data, setData] = useState<any>([]);

  // Define the fetch function
  const fetchData = async () => {
    try {
      const response = await api.get(
        `/packages/simple/${moduleId}/folder/file_contents/${fileId}`
      );
      console.log(response);
      // Store the fetched data if needed
      setData(response.data);
    } catch (err) {
      console.log("There was an error", err);
    }
  };

  // Call fetchData inside a useEffect callback
  useEffect(() => {
    fetchData();
  }, [moduleId, fileId]);

  return (
    <Container className="mt-4">
      <h2>
        Module: {moduleId}, File: {fileId}
      </h2>
      {/* Render fetched data if applicable */}
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </Container>
  );
}
