import React, { useState, useEffect } from "react";
import { useLanguage } from "@/context/DeveloperLanguageContext";
import api from "@/api";
import { MathJax } from "better-react-mathjax";

const SolutionPanel: React.FC<{ question_id: number | string }> = ({
  question_id,
}) => {
  const [solutionHTML, setSolutionHTML] = useState("");
  const { selectedLanguage } = useLanguage();

  const fetchQuiz = async () => {
    const payload = {
      server_type: selectedLanguage,
    };
    try {
      const response = await api.post(
        `/quiz/adaptive_quiz/get_solution/${question_id}`,
        payload
      );
      setSolutionHTML(response.data);
    } catch (err) {
      console.error("Error loading quiz:", err);
    }
  };
  useEffect(() => {
    fetchQuiz();
  }, [question_id, selectedLanguage]);

  return (
    <MathJax>
      <div className="" dangerouslySetInnerHTML={{ __html: solutionHTML }} />
    </MathJax>
  );
};

export default SolutionPanel;
