import { useEffect, useState } from "react";
import api from "@/api";
import { useLanguage } from "@/context/DeveloperLanguageContext";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import DeveloperMode from "@/components/DeveloperMode";
import QuizOverviewHeader from "./QuizOverviewHeader";
import { QuestionFolder } from "@/.next/types/QuestionFolder";
import QuizViewToggle from "./QuizViewToggle";
import { IoBugOutline } from "react-icons/io5";

import QuizPanel from "./QuizPanel";
import SolutionPanel from "./SolutionPanel";
import { useQuizMode } from "@/context/QuizModeContext";

const panelStyles = `
relative
  my-5
  bg-white dark:bg-gray-800 
  border border-gray-200 dark:border-gray-700 
  shadow-lg 
  rounded-2xl 
  p-6 
  transition-all duration-200
  overflow-auto
  py-5
`;

function LeftSplitPanel({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Panel
        className={panelStyles}
        defaultSize={50}
        minSize={0}
        id="left"
        order={1}
        collapsible={true}
        collapsedSize={0}
      >
        {children}
      </Panel>
      <PanelResizeHandle
        className="
          w-2
          my-5
          flex items-center justify-center
          cursor-col-resize
          bg-indigo-500 hover:bg-indigo-700
          transition-colors duration-150
        "
      />
    </>
  );
}
type QuizPageProps = {
  question_id: number | string;
};

const QuizPanelToolBar: React.FC = () => {
  const { selectedMode } = useQuizMode();
  return (
    <div className="absolute w-full content-end top-0 left-0 border border-DarkShades border-b-8 bg-indigo-600 text-white z-10 flex flex-row">
      <div className="my-2 mx-4 size-10 border rounded-2xl border-white bg-white px-2 py-4 text-black items-center flex justify-center">
        <IoBugOutline />
      </div>
      <div className="my-2 mx-4 size-10 border rounded-2xl border-white bg-white px-2 py-4 text-black items-center flex justify-center">
        <IoBugOutline />
      </div>
      <div className="my-2 mx-4 size-10 border rounded-2xl border-white bg-white px-2 py-4 text-black items-center flex justify-center">
        <IoBugOutline />
      </div>
    </div>
  );
};

const QuizPage: React.FC<QuizPageProps> = ({ question_id }) => {
  const [Question, setQuestion] = useState<QuestionFolder | null>(null);
  const { selectedMode, setSelectedMode } = useQuizMode();

  const fetchQuestion = async () => {
    try {
      const res = await api.get(`/packages/get_question_folder/${question_id}`);
      setQuestion(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchQuestion();
  }, [question_id]);

  return Question ? (
    <>
      {/* Header */}
      <div className="flex flex-col items-center mx-5 space-y-2">
        <QuizOverviewHeader question={Question} />
        <div className="self-end">
          <QuizViewToggle />
        </div>
      </div>

      {/* Main Panels */}
      <PanelGroup direction="horizontal" className="overflow-hidden relative">
        {selectedMode === "student" && (
          <LeftSplitPanel>
            <SolutionPanel question_id={question_id} />
          </LeftSplitPanel>
        )}

        {selectedMode === "developer" && (
          <LeftSplitPanel>
            <DeveloperMode question_id={question_id} />
          </LeftSplitPanel>
        )}
        {/* Panel for Quiz View */}

        <Panel
          className={`${panelStyles}`}
          defaultSize={70}
          minSize={20}
          id="quiz_panel"
          order={2}
        >
          {/* <QuizPanelToolBar /> */}
          <QuizPanel folder_id={question_id} />
        </Panel>
      </PanelGroup>
    </>
  ) : (
    <div className="p-4 text-center text-gray-500">Loading...</div>
  );
};
export default QuizPage;
