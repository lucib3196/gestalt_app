// app/modules/[moduleId]/file/[fileId]/page.tsx
"use client";

import { useParams } from "next/navigation";
import { Container } from "react-bootstrap";

export default function FileViewPage() {
  const params = useParams();
  const moduleId = params.id as string;
  const fileId = params.fileId as string;

  return (
    <Container className="mt-4">
      <h2>
        Module: {moduleId}, File: {fileId}
      </h2>
      {/* You can fetch data here using these IDs */}
    </Container>
  );
}
