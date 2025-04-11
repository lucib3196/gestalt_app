"use client";
import React from "react";
import ModGenerators from "@/components/ModGenerators";
import "@/styles/ModGeneratorStyles.css";
import api from "@/api";
import { useState } from "react";

const examples = [
  {
    name: "Projectile Motion",
    text: "A ball is thrown horizontally from the top of a 50-meter high building with an initial speed of 15 meters per second. Assuming there is no air resistance, calculate the time it takes for the ball to reach the ground.",
  },
  {
    name: "Spring Oscillation",
    text: "A mass-spring system oscillates with a period of 2 seconds. If the spring constant is 100 N/m, calculate the mass attached to the spring. Assume the motion is simple harmonic.",
  },
  {
    name: "Pressure Calculation",
    text: "A force of 200 Newtons is applied perpendicular to a circular cross-sectional area with a radius of 0.1 meters. Calculate the pressure exerted on the area.",
  },
];
const TextGeneratorConst = {
  name: "Text Based Generator",
};


interface QuestionData {
  question: string;
  folder_name: string;
}

const InputForm: React.FC = () => {
  const [FormData, setFormData] = useState<QuestionData>({
    question: "",
    folder_name: "",
  });
  const [loading, setLoading] = useState<boolean>(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({ ...FormData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await api.post("/code_generator_chains/v1", FormData);
      console.log(response.data);
    } catch (error) {
      console.log("Error Submitting Form", error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="text-gen-form">
      {loading ? (
        <div className="loading-indicator">
          {/* Replace with your loading spinner or message */}
          Loading...
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="folder_name"
            className="form-control"
            value={FormData.folder_name}
            onChange={handleChange}
            placeholder="Folder Name"
            required
          />

          <div className="form-floating">
            <textarea
              name="question"
              className="form-control"
              value={FormData.question}
              id="questionTextArea"
              onChange={handleChange}
              required
            />
            <label htmlFor="questionTextArea">Enter Question</label>
          </div>

          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </form>
      )}
    </div>
  );
};

export default function TextGenerator() {
  return (
    <>
      <ModGenerators
        title="Text Generator"
        subtitle="Creates dynamic educational modules based on input"
        examples={examples}
        inputComponent={<InputForm />}
      />
    </>
  );
}
