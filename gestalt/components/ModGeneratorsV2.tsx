import React from "react";

// Types for Example
type ExampleItem = {
  exampleName: string;
  exampleText: string;
};

// General Types for Mod
type ModProps = {
  title: string;
  subtitle: string;
  examples: ExampleItem[];
  formComponent?: React.ComponentType<any>;
};

const IndividualExampleContainer: React.FC<ExampleItem & { index: number }> = ({
  exampleName,
  exampleText,
  index,
}) => {
  return (
    <div className="flex flex-col gap-1 mb-4 p-4 border-b-2 rounded-b-lg bg-white shadow-sm  border-gray-200">
      <span className="!text-xl font-semibold !text-mainBrand border-b border-lightAccent pb-1">
        Example {index + 1}
        {exampleName && ` – ${exampleName}`}
      </span>
      <p className="text-gray-700 leading-relaxed">{exampleText}</p>
    </div>
  );
};

const ModGenerator: React.FC<ModProps> = ({
  title,
  subtitle,
  examples,
  formComponent,
}) => {
  return (
    <div className="w-full max-w-5xl mx-auto my-8 px-6 py-8 bg-white rounded-2xl shadow-xl border border-gray-200">
      {/* Header */}
      <div className="text-center border-b border-gray-300 pb-4 mb-6">
        <h1 className="!text-4xl !font-bold !text-DarkShades">{title}</h1>
        <h2 className="!text-lg italic !text-lightAccent mt-1">{subtitle}</h2>
      </div>

      {/* Example Section */}
      <div className="mb-8">
        <h3 className="!text-xl font-medium  !text-DarkShades text-center mb-4">
          What can I upload?
        </h3>
        <ul className="flex flex-col gap-4">
          {examples.map((example, index) => (
            <li key={index}>
              <IndividualExampleContainer {...example} index={index} />
            </li>
          ))}
        </ul>
      </div>

      {/* Form Section */}
      {formComponent && (
        <div className="mt-6">{React.createElement(formComponent)}</div>
      )}
    </div>
  );
};

export default ModGenerator;
