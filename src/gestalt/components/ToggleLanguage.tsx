import TooltipExample from "./ToolTipComponent";
import { useLanguage } from "@/context/DeveloperLanguageContext";
import React, { useEffect, useState } from "react";

const ToggleLanguage: React.FC = () => {
  const { selectedLanguage, setSelectedLanguage } = useLanguage();
  return (
    <div className="flex flex-col items-center">
      <TooltipExample text="Choose Code to Run" message="Choose code to run" />
      <div className="inline-flex items-center border rounded-md overflow-hidden">
        {["javascript", "python"].map((lang) => (
          <button
            key={lang}
            className={`px-4 py-2 text-sm font-medium ${
              selectedLanguage === lang
                ? "bg-indigo-600 text-white"
                : "bg-white text-gray-700"
            }`}
            onClick={() => setSelectedLanguage(lang as "javascript" | "python")}
          >
            {lang[0].toUpperCase() + lang.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};

interface ToggleOptionsProps<T extends string> {
  initialVal: T;
  options: T[];
  onClick?: (option: T) => void;
  tipMessage?: { text: string; message: string };
}

export const ToggleOptions = <T extends string>({
  initialVal,
  options,
  onClick,
  tipMessage,
}: ToggleOptionsProps<T>) => {
  const [selectedOption, setSelectedOption] = useState<any>(initialVal);

  const handleClick = (option: T) => {
    setSelectedOption(option); // Update the selected option locally
    if (onClick) {
      onClick(option); // Call the parent-provided onClick handler
    }
  };

  const handleTip = () => {
    if (!tipMessage) {
      return;
    }
    return (
      <TooltipExample text={tipMessage.text} message={tipMessage.message} />
    );
  };

  return (
    <div className="flex flex-col items-center">
      {handleTip()}
      <div className="inline-flex items-center border rounded-md overflow-hidden">
        {options.map((option) => (
          <button
            key={option}
            className={`px-4 py-2 text-sm font-medium ${
              selectedOption === option
                ? "bg-indigo-600 text-white"
                : "bg-white text-gray-700"
            }`}
            onClick={() => handleClick(option)}
          >
            {option[0].toUpperCase() + option.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ToggleLanguage;
