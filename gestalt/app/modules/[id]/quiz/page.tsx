"use client";

import { useEffect, useState } from "react";
import api from "@/api";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import DeveloperMode from "@/components/DeveloperMode";
import QuizView from "@/components/QuizView";
import { LanguageProvider } from "@/app/hooks/LanguageContext";

type ReviewComponentProps = {
  reviewed: boolean | undefined;
};

const QuizPage: React.FC = () => {
  const [devMode, setDevMode] = useState(false);
  const [Question, setQuestion] = useState<QuestionFolder | null>(null);

  const question_id = 6;

  const handleToggleDevMode = () => setDevMode((prev) => !prev);

  const fetchQuestion = async () => {
    try {
      const res = await api.get(`/packages/question/${question_id}`);
      setQuestion(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const ReviewComponent: React.FC<ReviewComponentProps> = ({ reviewed }) => {
    return (
      <div className="inline-grid grid-cols-2 gap-4 my-3 mx-2 items-baseline">
        <p className="font-semibold">Reviewed:</p>
        <div
          className={`w-full rounded-full py-2 text-center shadow border font-medium ${
            reviewed ? "bg-green-500 text-white" : "bg-red-500 text-white"
          }`}
        >
          {reviewed ? "True" : "False"}
        </div>
      </div>
    );
  };

  useEffect(() => {
    fetchQuestion();
  }, [question_id]);

  return (
    <>
      {/* Header */}
      <header className="bg-gray-100 shadow-sm">
        <div className="flex justify-between items-center mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
          <div>
            <h1 className="text-gray-800 text-3xl font-bold border-b-2 pb-1">
              {Question?.title.split(/(?=[A-Z])/).join(" ") ?? "Loading..."}
            </h1>
            <div className="flex flex-wrap gap-2 mt-2">
              {Question?.tags.map((value, index) => (
                <span
                  key={index}
                  className="px-3 py-1 text-sm font-semibold border rounded-full text-gray-700 bg-white shadow"
                >
                  {value.split(/(?=[A-Z])/).join(" ")}
                </span>
              ))}
            </div>
            <ReviewComponent reviewed={Question?.reviewed ?? false} />
          </div>

          <button
            onClick={handleToggleDevMode}
            className="rounded-xl bg-indigo-600 text-white font-semibold px-4 py-2 hover:bg-indigo-700 active:bg-indigo-800 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 transition"
          >
            Developer Mode
          </button>
        </div>
      </header>

      {/* Content Panel */}
      <PanelGroup direction="horizontal">
        {devMode && (
          <>
            <Panel defaultSize={30} minSize={10} id="left" order={1}>
              <DeveloperMode question_id={question_id} />
            </Panel>
            <PanelResizeHandle />
          </>
        )}

        <Panel defaultSize={70} minSize={20} id="main" order={2}>
          <QuizView folder_id={question_id} />
        </Panel>
      </PanelGroup>
    </>
  );
};

const Page: React.FC = () => {
  return (
    <LanguageProvider>
      <QuizPage />;
    </LanguageProvider>
  );
};

export default Page;
