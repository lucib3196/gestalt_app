// app/modules/[moduleId]/file/[fileId]/page.tsx
"use client";

import { useParams } from "next/navigation";
import { Container } from "react-bootstrap";
import { useState, useEffect } from "react";
import api from "@/api";
import CodeEditor from "@/components/CodeEditor";


export default function FileViewPage() {
  const params = useParams();
  const moduleId = params.id as string;
  const folderID = params.folderId as string;
  const filename = params.filename as string


  const [data, setData] = useState<any>([]);

  // Define the fetch function
  const fetchData = async () => {
    try {
      console.log(folderID)
      const response = await api.get(
        `/packages/simple/${moduleId}/${folderID}/${filename}`
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
  }, [moduleId, folderID]);

  return (
    <Container className="mt-4">
      <h2>
        Module: {moduleId}, File: {folderID}
      </h2>
      <CodeEditor content={data.content}/>
    </Container>
  );
}
