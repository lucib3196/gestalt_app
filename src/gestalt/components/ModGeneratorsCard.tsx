import Link from "next/link";
import "../styles/ModGeneratorsCard.css"

interface GeneratorInfoProps {
  name: string;
  description: string;
  bestFor: string;
  inputType: string;
  outputType: string;
  path: string;
}

const ModGeneratorsCard: React.FC<GeneratorInfoProps> = ({
  name,
  description,
  bestFor,
  inputType,
  outputType,
  path,
}) => {
  return (
    <div className="generator-card">
      <div className="text-container">
        <h3 className="text-center">{name}</h3>
        <hr className="divider" />
      </div>
      <p className="text-center ital">{description}</p>

      <ul className="list-group list-group-flush mb-3">
        <li className="list-group-item">
          <strong>Best For:</strong> {bestFor}
        </li>
        <li className="list-group-item">
          <strong>Input:</strong> {inputType}
        </li>
        <li className="list-group-item">
          <strong>Output:</strong> {outputType}
        </li>
      </ul>

      <Link href={path} className="my-button-primary w-100">
      <span className="my-button-primary-text"> Get Started</span>
      </Link>
    </div>
  );
};

export default ModGeneratorsCard;
