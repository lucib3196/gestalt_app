"use client";

import { useParams } from "next/navigation";
import { Container, Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import api from "@/api";

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
        const response = await api.post(`/quiz/adaptive_quiz/${moduleId}`);
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
    <Container className="mt-4">
      <form onSubmit={handleSubmit}>
        <h1 className="mb-4">Module: {moduleId}, File: {fileId}</h1>

        <div className="form-field mb-3" dangerouslySetInnerHTML={{ __html: quizHTML }} />
        {/* <div className="container mb-3" dangerouslySetInnerHTML={{ __html: solutionHTML }} /> */}

        {/* <input type="hidden" name="csrf_token" value={csrfToken} /> */}

        <div className="quiz-btn-container mb-2">
          <Button type="submit" variant="primary">Submit</Button>
          <Button type="button" variant="secondary" onClick={() => location.reload()}>New Variant</Button>
        </div>

        <div className="step-btn-container">
          <Button type="submit" name="action" value="hint" variant="info">Show Hint</Button>
        </div>
      </form>
    </Container>
  );
}
