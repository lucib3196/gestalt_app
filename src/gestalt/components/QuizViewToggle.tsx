import { useQuizMode } from "@/app/context/QuizModeContext";
import { ToggleOptions } from "./ToggleLanguage";
import { QuizMode } from "@/.next/types/types";

const QuizViewToggle: React.FC = () => {
  const { selectedMode, setSelectedMode } = useQuizMode();
  return (
    <>
      <ToggleOptions
        initialVal="student"
        options={["student", "developer"] as QuizMode[]}
        onClick={(mode: QuizMode) => setSelectedMode(mode)}
        tipMessage={{
          text: "Toggle Quiz Mode",
          message: "Toggle between dev mode for testing and student view ",
        }}
      />
    </>
  );
};

export default QuizViewToggle;
