import React, { createContext, useContext, useState } from "react";
import { QuizModeContextType, QuizMode } from "@/.next/types/types";

const QuizModeContext = createContext<QuizModeContextType | undefined>(
  undefined
);

export const QuizModeProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [selectedMode, setSelectedMode] = useState<QuizMode>("student");
  return (
    <QuizModeContext.Provider value={{ selectedMode, setSelectedMode }}>
      {children}
    </QuizModeContext.Provider>
  );
};

export const useQuizMode = (): QuizModeContextType => {
  const context = useContext(QuizModeContext);

  if (!context) {
    throw new Error("useLanguage must be used within a Language Provider");
  }
  return context;
};
