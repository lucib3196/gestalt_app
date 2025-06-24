"use client";
import React from "react";
import QuizContainer from "@/components/QuizContainer";
import { LanguageProvider } from "@/context/DeveloperLanguageContext";
import { useParams } from "next/navigation";
import DeveloperMode from "@/components/DeveloperMode";

const Page: React.FC = () => {
    const { slug } = useParams();
    console.log(slug);

    if (!slug) {
        return <div>Invalid or missing slug.</div>;
    }

    const slugStr = Array.isArray(slug) ? slug[0] : slug;
    const [title, id] = decodeURIComponent(slugStr).split("_");

    return (
        <LanguageProvider>
            <DeveloperMode question_id={id}/>
            <QuizContainer folder_id={id} />
        </LanguageProvider>
    );
};

export default Page;
