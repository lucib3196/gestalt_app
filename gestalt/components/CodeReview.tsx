import Modal from "./MyModals";
import React, { useState } from "react";
import DropDown from "./DropDown";

type CodeReviewQuestion = {
  purpose: string;
  question: string;
  options: string[];
};
type CodeReviewQuestions = {
  q: CodeReviewQuestion[];
};

const CodeReviewForm: React.FC<CodeReviewQuestions> = ({ q }) => {
  q.map((value, index) => console.log(value.purpose));

  const handleQ = () => {
    return q.map((value, index) => (
      <div
        key={index}
        className="flex flex-col items-start gap-3 p-4 w-full border-b border-gray-200"
      >
        <p className="m-0 border-b-4 text-DarkShades opacity-75">
          <strong>{value.purpose}</strong>
        </p>
        <p className="m-0 text-DarkShades">
          <strong>{value.question}</strong>
        </p>
        <select className="m-0 p-2 border rounded-md">
          {value.options.map((option, idx) => (
            <option key={idx}>{option}</option>
          ))}
        </select>
      </div>
    ));
  };

  return <>{handleQ()}</>;
};


const codeReview: CodeReviewQuestions = {
  q: [
    {
      purpose: "Initial Code Validity",
      question: "Did the AI-generated code run without error?",
      options: ["Yes", "No"],
    },
    {
      purpose: "Correctness of Output",
      question: "Does the output match the expected physical result?",
      options: ["Yes", "No", "Partially"],
    },
    {
      purpose: "Fix Required?",
      question: "Was a manual fix required to make it correct or runnable?",
      options: ["Yes", "No"],
    },
    {
      purpose: "Fix Time Estimate",
      question: "How long did it take to fix? (hr) (Estimate)",
      options: ["0", "0.5", "1", "1.5", "2"],
    },
    {
      purpose: "Fix Type",
      question: "What was the issue?",
      options: ["Syntax", "Logic", "Units", "Other"],
    },
    {
      purpose: "Unit Handling Correct?",
      question:
        "Are physical units applied and managed correctly (e.g., m/s, N, kg)?",
      options: ["Yes", "No", "Partially"],
    },
  ],
};

export default function CodeReview() {
  const [showModal, setShowModal] = useState(false);
  return (
    <>
      <button
        type="button"
        className="inline-flex items-center justify-center px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition-colors duration-200 hover:bg-indigo-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 active:bg-indigo-700"
        onClick={() => setShowModal(true)}
      >
        Submit Review
      </button>
      <Modal
        show={showModal}
        onClose={() => setShowModal(false)}
        title="Code Review"
      >
        <CodeReviewForm q={codeReview.q} />
      </Modal>
    </>
  );
}
