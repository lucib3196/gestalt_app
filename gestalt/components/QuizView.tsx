import { useEffect, useState } from "react";
import api from "@/api";
import { useLanguage } from "@/app/hooks/LanguageContext";

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
        server_type: selectedLanguage
    }
    try {
      const response = await api.post(`/quiz/adaptive_quiz/get_quiz/${folder_id}`,payload);
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

export default QuizView;
