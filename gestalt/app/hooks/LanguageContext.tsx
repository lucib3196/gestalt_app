import { languages } from "monaco-editor";
import React, { createContext, useContext, useState } from "react";

type Language = "javascript" | "python";

interface LanguageContextType {
  selectedLanguage: Language;
  setSelectedLanguage: (lang: Language) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(
  undefined
);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [selectedLanguage, setSelectedLanguage] =
    useState<Language>("javascript");

  return (
    <LanguageContext.Provider value={{ selectedLanguage, setSelectedLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error("useLanguage must be used within a Language Provider");
  }
  return context;
};
