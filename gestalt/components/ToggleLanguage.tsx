import TooltipExample from "./ToolTipComponent";
import { useLanguage } from "@/app/hooks/LanguageContext";

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

export default ToggleLanguage;
