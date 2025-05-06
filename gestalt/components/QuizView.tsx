import { useEffect, useState } from "react";
import api from "@/api";
import { useLanguage } from "@/app/hooks/LanguageContext";
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
import DeveloperMode from "@/components/DeveloperMode";
import { LanguageProvider } from "@/app/hooks/LanguageContext";

type QuizViewProps = {
  folder_id: number;
};
const QuizView: React.FC<QuizViewProps> = ({ folder_id }) => {
  const [quizHTML, setQuizHTML] = useState("");
  const [quizAnswer, setQuizAnswer] = useState<Record<string, string> | null>(
    null
  );
  const { selectedLanguage } = useLanguage();

  //Fetch question data this needs to be changed to account for which code
  // Either js or py

  const fetchData = async () => {
    const payload = {
      server_type: selectedLanguage,
    };
    try {
      const response = await api.post(
        `/quiz/adaptive_quiz/get_quiz/${folder_id}`,
        payload
      );
      setQuizHTML(response.data);
    } catch (err) {
      console.error("Error loading quiz:", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, [folder_id, selectedLanguage]);

  //   Handle Submit Currently just shows the answer
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    console.log(data);

    try {
      const response = await api.post("/quiz/adaptive_quiz/grade_quiz", data, {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      });
      console.log(response.data);
      setQuizAnswer(response.data);
    } catch (error) {
      console.error("There was an error", error);
    }
  };

  return (
    <div className="px-4 py-6">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div
          className="prose max-w-full"
          dangerouslySetInnerHTML={{ __html: quizHTML }}
        />

        <div className="flex gap-4">
          <button
            type="submit"
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Submit
          </button>
          <button
            type="button"
            onClick={() => fetchData()}
            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            New Variant
          </button>
        </div>
      </form>

      <div className="mt-6">
        <h2 className="text-lg font-semibold">Answer</h2>
        {quizAnswer ? (
          <ul className="mt-2 space-y-1">
            {Object.entries(quizAnswer).map(([key, value]) => (
              <li key={key} className="text-sm">
                <strong>{key}</strong>: {value}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-gray-500">Loading...</p>
        )}
      </div>
    </div>
  );
};

type ReviewComponentProps = {
  reviewed: boolean | undefined;
};
type QuizPageProps = {
  question_id: number|string;
};
const QuizPage: React.FC<QuizPageProps> = ({ question_id }) => {
  const [devMode, setDevMode] = useState(false);
  const [Question, setQuestion] = useState<QuestionFolder | null>(null);

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
    console.log("Review status", reviewed);
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

  console.log(Question);

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

export default QuizPage;
