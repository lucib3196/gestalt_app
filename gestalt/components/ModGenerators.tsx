import React from "react";
import { Container } from "react-bootstrap";
import "../styles/ModGeneratorStyles.css";

// 📌 Interfaces
interface ExampleItem {
  name: string;
  text: string;
}

interface ModGeneratorProps {
  title: string;
  subtitle: string;
  examples: ExampleItem[];
  inputComponent?: React.ReactNode|React.FC
}

interface ModInfoProps {
  title: string;
  subtitle: string;
}

interface IndividualExample {
  example: string;
  name?: string;
  index: number;
}

// 📘 Components

// Renders title and subtitle
const ModInfo: React.FC<ModInfoProps> = ({ title, subtitle }) => (
  <div className="gen-info-container">
    <h1 className="gen-title">{title}</h1>
    <h2 className="gen-subheading">{subtitle}</h2>
  </div>
);

// Renders a single example
const IndividualExampleContainer: React.FC<IndividualExample> = ({
  example,
  index,
  name,
}) => (
  <div className="ind-ex-container">
    <span className="fw-bold">
      Example {index} {name && `- ${name}`}
    </span>
    <span className="underline"></span>
    <p>{example}</p>
  </div>
);

// Renders the full example list
const ModExample: React.FC<{ examples: ExampleItem[] }> = ({ examples }) => (
  <>
    <h3 className="gen-example-text">The following are examples of valid inputs</h3>
    <div className="example-container">
      <ul className="mod-example-list">
        {examples.map((example, index) => (
          <li className="mod-example-list" key={index}>
            <IndividualExampleContainer
              example={example.text}
              name={example.name}
              index={index + 1}
            />
          </li>
        ))}
      </ul>
    </div>
  </>
);

// Top-level generator component
const ModGenerators: React.FC<ModGeneratorProps> = ({
  title,
  subtitle,
  examples,
  inputComponent
}) => (
  <Container className="mod-container">
    <ModInfo title={title} subtitle={subtitle} />
    <ModExample examples={examples} />
    {inputComponent && <>{inputComponent}</>}
  </Container>
);

export default ModGenerators;
