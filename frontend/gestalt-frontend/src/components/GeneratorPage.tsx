import React, { JSX, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "../styles/GeneratorPage.css";
import api from "../api";

// ───────────────────────────────────────────────
// 🔹 Generator Info Component (Header section)
// ───────────────────────────────────────────────
type GeneratorInfoProps = {
  title: string;
  subtitle: string;
};

function GeneratorInfo({ title, subtitle }: GeneratorInfoProps) {
  return (
    <div className="gen-info-container">
      <div className="gen-title">{title}</div>
      <div className="gen-subheading">{subtitle}</div>
    </div>
  );
}

// ───────────────────────────────────────────────
// 🔹 Generator Example Component (Each item)
// ───────────────────────────────────────────────
type GeneratorExampleProps = {
  name: string;
  text: string;
};

function GeneratorExample({ name, text }: GeneratorExampleProps) {
  return (
    <div className="example-section">
      <ul className="list-group mx-5">
        <li className="list-group-item d-flex justify-content-between align-items-start">
          <div className="ms-2 me-auto">
            <div className="fw-bold">{name}</div>
            <p>{text}</p>
          </div>
        </li>
      </ul>
    </div>
  );
}

// ───────────────────────────────────────────────
// 🔹 Text-Based Generator Info and Examples
// ───────────────────────────────────────────────
function TextGenerator() {
  const info = {
    name: "QuickQuery",
    subtitle:
      "Input a question below to automatically generate a question module.",
  };

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

  return (
    <>
      <GeneratorInfo title={info.name} subtitle={info.subtitle} />
      <ul className="list-group mx-5">
        {examples.map((example, idx) => (
          <GeneratorExample key={idx} name={example.name} text={example.text} />
        ))}
      </ul>
    </>
  );
}

// ───────────────────────────────────────────────
// 🔹 Image-Based Generator Info and Examples
// ───────────────────────────────────────────────
function ImageGenerator() {
  const info = {
    name: "Image Upload",
    subtitle:
      "Upload your images below to generate personalized modules instantly.",
  };

  const examples = [
    {
      name: "Textbook solutions:",
      text: "Officially published problems and solutions ensure high accuracy.",
    },
    {
      name: "Handwritten solutions:",
      text: "Personal notes or handwritten solutions will be effectively processed.",
    },
    {
      name: "Lecture materials:",
      text: "Slides or instructional content from lectures can be used to create modules.",
    },
  ];

  return (
    <>
      <GeneratorInfo title={info.name} subtitle={info.subtitle} />
      <ul className="list-group mx-5">
        {examples.map((example, idx) => (
          <GeneratorExample key={idx} name={example.name} text={example.text} />
        ))}
      </ul>
    </>
  );
}

// ───────────────────────────────────────────────
// 🔹 Generator Form Submission Section
// ───────────────────────────────────────────────
function GeneratorFormText() {
  const [modName, setModName] = useState("");
  const [bodyText, setBodyText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await api.post("/chains", {
        query: bodyText,
        folder_name: modName,
      });
      console.log(response);
    } catch (error: any) {
      console.error("Error Posting Data", error.response?.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="nameInput" className="form-label">
          Name
        </label>
        <input
          type="text"
          id="nameInput"
          className="form-control"
          value={modName}
          onChange={(e) => setModName(e.target.value)}
          required
        />
      </div>

      <div className="mb-3">
        <label htmlFor="bodyText" className="form-label">
          Body Text
        </label>
        <textarea
          id="bodyText"
          className="form-control"
          rows={5}
          value={bodyText}
          onChange={(e) => setBodyText(e.target.value)}
          required
        ></textarea>
      </div>

      <button type="submit" className="btn btn-primary" disabled={loading}>
        {loading ? "Processing..." : "Submit"}
      </button>
      {/* Loading spiner */}
      {loading && (
        <div className="text-center mt-3">
          <div className="spinner-border" role="status">
            <span className="visually-hidden"></span>
          </div>
        </div>
      )}
    </form>
  );
}

// ───────────────────────────────────────────────
// 🔹 Main Generator Page Component
// ───────────────────────────────────────────────
type GeneratorType = "text" | "image";

const componentMap: Record<GeneratorType, JSX.Element> = {
  text: <TextGenerator />,
  image: <ImageGenerator />,
};

export default function GeneratorPage() {
  const [selectedGenerator, setSelectedGenerator] =
    useState<GeneratorType>("text");

  return (
    <div className="gen-container">
      <div className="selection-container">
        <label>Select a generator type: </label>
        <select
          className="form-select"
          value={selectedGenerator}
          onChange={(e) =>
            setSelectedGenerator(e.target.value as GeneratorType)
          }
        >
          <option value="text">Text Generator</option>
          <option value="image">Image Generator</option>
        </select>
      </div>

      {/* Dynamically rendered component based on selected type */}
      {componentMap[selectedGenerator]}

      {/* Form below generator output */}
      <GeneratorFormText />
    </div>
  );
}
