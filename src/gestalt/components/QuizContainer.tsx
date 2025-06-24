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

type RevealButtonProps = {
    targetId: number;
    label: string;
};

const RevealButton: React.FC<RevealButtonProps> = ({ targetId, label }) => {
    const handleClick = () => {
        let target_msg = `[data-level="${targetId}"]`;
        console.log(target_msg);
        const target = document.querySelector(target_msg);
        if (target) {
            target.classList.toggle("hidden-step");
            targetId++;
        }
    };

    return (
        <button
            className="border-DarkShades border-2 px-2 py-4"
            onClick={handleClick}
        >
            {label}
        </button>
    );
};

const QuizContainer: React.FC<QuizContainerProps> = ({ folder_id }) => {
    const [quizHTML, setQuizHTML] = useState<string>("");
    const { selectedLanguage } = useLanguage();
    const [error, setError] = useState<string | null>(null);
    const [quizAnswer, setQuizAnswer] = useState<Record<string, string> | null>(null);
    const [quizData, setQuizData] = useState<Question | null>(null);
    const [solutionHtml, setSolutionHTML] = useState<string | null>(null);
    const [revealedSteps, setRevealedSteps] = useState<number[] | null>(null);

    // Fetch quiz HTML
    const fetchQuiz = async () => {
        setError(null);
        try {
            const response = await api.post(
                `/quiz/adaptive_quiz/get_quiz/${folder_id}`,
                { server_type: selectedLanguage }
            );
            setQuizHTML(response.data.html);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to load quiz");
            toast.error("Failed to load quiz");
        }
    };

    // Fetch quiz metadata
    const fetchQuizData = async () => {
        setError(null);
        try {
            const response = await api.get(
                `/packages/get_question_folder/${folder_id}`
            );
            setQuizData(response.data);
        } catch {
            setError("Failed to get quiz data");
            toast.error("Failed to load quiz data");
        }
    };

    // Fetch solution HTML
    const fetchSolutionHTML = async () => {
        try {
            const response = await api.post(
                `/quiz/adaptive_quiz/get_solution/${folder_id}`,
                { server_type: selectedLanguage }
            );
            setSolutionHTML(response.data);
            console.log("This is the solution")
            console.log(response.data)
        } catch {
            setSolutionHTML(null);
            console.log(solutionHtml);
        }
    };

    // Handle quiz submission
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await api.post("/quiz/adaptive_quiz/grade_quiz", data, {
                headers: { "Content-Type": "application/json" },
                withCredentials: true,
            });
            setQuizAnswer(response.data);
        } catch {
            toast.error("There was an error grading the quiz");
        }
    };

    // Reveal next solution step
    const revealNextStep = () => {
        setRevealedSteps((prev) => {
            const current = prev ?? [];
            const nextStep = current.length + 1;
            console.log("next step", nextStep)
            return [...current, nextStep];
        });
    };

    // Reveal solution steps in DOM
    useEffect(() => {
        console.log(revealedSteps)
        revealedSteps?.forEach(step => {
            const target = document.querySelector(`[data-level="${step}"]`);
            if (target) {
                target.classList.remove("hidden-step");
            }
        });
    }, [revealedSteps, solutionHtml]);

    // Fetch data on mount or when folder/language changes
    useEffect(() => {
        fetchQuiz();
        fetchQuizData();
        fetchSolutionHTML();
        setQuizAnswer(null); // Reset answer on quiz/language change
        setRevealedSteps([]); // Reset revealed steps
    }, [folder_id, selectedLanguage]);

    if (error) {
        return <ErrorAlert title="Error loading quiz" message={error} />;
    }

    return (
        <MathJax>
            <div className="mt-12 flex flex-col justify-center items-center gap-y-5 h-[calc(100%-3rem)] overflow-auto bg-white p-4">
                {quizData && <QuizOverviewHeader question={quizData} />}

                {/* Quiz Form */}
                <form onSubmit={handleSubmit} className="w-full max-w-2xl">
                    <div dangerouslySetInnerHTML={{ __html: quizHTML }} />
                    <div className="flex gap-4 justify-center mt-4">
                        <button
                            type="submit"
                            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                        >
                            Show Answer
                        </button>
                        <button
                            type="button"
                            className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-xl shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                            onClick={revealNextStep}
                        >
                            Hint?
                        </button>
                    </div>
                </form>

                {/* Quiz Answer */}
                <div className="mt-6 flex flex-col justify-center items-center w-full max-w-2xl">
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

                {/* Show Solution Step Button */}


                {/* Solution Steps */}
                {solutionHtml && (revealedSteps?.length ?? 0) > 0 && (
                    <div className="mt-8 w-full  bg-gray-50 rounded-lg p-6 shadow">
                        <h3 className="text-lg font-semibold mb-2 text-indigo-700">Solution</h3>
                        <div dangerouslySetInnerHTML={{ __html: solutionHtml }} />
                    </div>
                )}
            </div>
        </MathJax>
    );
};

export default QuizContainer;
