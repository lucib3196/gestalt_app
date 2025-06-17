"use client";
import { useParams } from "next/navigation";
import { QuestionFiles } from "@/components/QuestionTables";
import { ToggleOptions } from "@/components/ToggleLanguage";
import { useState, useEffect } from "react";
import { LanguageProvider } from "@/context/DeveloperLanguageContext";
import { QuizModeProvider } from "@/context/QuizModeContext";
import QuizPage from "@/components/QuizView";
const Page: React.FC = () => {
  const [pageView, setPageView] = useState<string>("allFiles");

  const params = useParams();
  const id = params.folder_id as string;



  return (
    <>
      <div className="my-3">
        <ToggleOptions
          initialVal={pageView}
          options={["allFiles", "quizView"] as const}
          onClick={(option: "allFiles" | "quizView") => setPageView(option)}
        />
      </div>
      {pageView === "allFiles" && <QuestionFiles question_id={id} />}
      {pageView === "quizView" && (
        <QuizModeProvider>
          <LanguageProvider>
            <QuizPage question_id={id} />;
          </LanguageProvider>
        </QuizModeProvider>
      )}
    </>
  );
};

export default Page;
