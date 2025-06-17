"use client";
import { useState, useEffect } from "react";
import { useLanguage } from "@/context/DeveloperLanguageContext";
import api from "@/api";
import ErrorAlert from "./ErrorMsg";
import { toast } from "react-toastify";
import { MathJax } from "better-react-mathjax";
import { Question } from "@/.next/types/types";
import QuizOverviewHeader from "./QuizOverviewHeader";

type QuizContainerProps = {
    folder_id: number | string;
};

const QuizContainer: React.FC<QuizContainerProps> = ({ folder_id }) => {
    const [quizHTML, setQuizHTML] = useState("");
    const { selectedLanguage } = useLanguage(); //The language that is rendering the quiz python or js
    const [error, setError] = useState<string | null>(null);
    const [quizAnswer, setQuizAnswer] = useState<Record<string, string> | null>(
        null
    );
    const [quizData, setQuizData] = useState<Question | null>(null);
    const fetchQuiz = async () => {
        setError(null);
        const payload = { server_type: selectedLanguage };
        try {
            const response = await api.post(
                `/quiz/adaptive_quiz/get_quiz/${folder_id}`,
                payload
            );
            setQuizHTML(response.data.html);
        } catch (err: any) {
            const msg = err.response?.data?.detail;
            setError(msg);
            toast.error("Failed to load quiz:");
        }
    };

    const fetchQuizData = async () => {
        setError(null);
        try {
            const response = await api.get(
                `/packages/get_question_folder/${folder_id}`
            );
            setQuizData(response.data);
        } catch (err: any) {
            const msg = "Failed to get quiz data";
            setError(msg);
            toast.error("Failed to load quiz:");
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const form = e.target as HTMLFormElement;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await api.post("/quiz/adaptive_quiz/grade_quiz", data, {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            });
            setQuizAnswer(response.data);
        } catch (error) {
            console.error("There was an error", error);
        }
    };

    useEffect(() => {
        fetchQuiz();
        fetchQuizData();
    }, [folder_id, selectedLanguage]);

    if (error) {
        return <ErrorAlert title="Error loading quiz" message={error} />;
    }

    return (
        <>
            <MathJax>
                <div className="mt-12 flex flex-col justify-center items-center gap-y-5 h-[calc(100%-3rem)] overflow-auto bg-white p-4">
                    {quizData && <QuizOverviewHeader question={quizData} />}
                    {/* Question Container with Form */}
                    <form onSubmit={handleSubmit}>
                        <div dangerouslySetInnerHTML={{ __html: quizHTML }} />
                        <div className="flex gap-4 justify-center">
                            <button
                                type="submit"
                                className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                            >
                                Show Answer
                            </button>
                        </div>
                    </form>

                    <div className="mt-6 flex flex-col justify-center items-center">
                        <h2 className="text-xl font-semibold">Check Your Answer</h2>
                        {quizAnswer ? (
                            <ul className="mt-2 space-y-1">
                                {Object.entries(quizAnswer).map(([key, value]) => (
                                    <li key={key} className="text-lg">
                                        <strong>{key}</strong>: {value}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="text-lg text-gray-500"></p>
                        )}
                    </div>
                </div>
            </MathJax>
        </>
    );
};

export default QuizContainer;
