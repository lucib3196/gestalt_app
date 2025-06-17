import Table from "@/components/Table";
import React from "react";
import { useRouter } from "next/navigation";
import { useFetch } from "./QuestionTables";
import Loading from "./Loading";
import { createTableData } from "./QuestionTables";
import { ColumnConfig } from "./QuestionTables";
import { Question } from "@/.next/types/types";


const questionColumns: ColumnConfig<Question>[] = [
    { key: "id", header: "ID" },
    {
        key: "title",
        header: "Question Title",
        classes: {
            row: "underline text-blue-600 hover:text-blue-800 cursor-pointer",
        },
    },
    { key: "topic", header: "Topics" },
    { key: "tags", header: "Tags" },
    { key: "relevant_courses", header: "Relevant Courses" },
    // { key: "pre_reqs", header: "Pre-Reqs" }, // Deprecated for now
    { key: "created_by", header: "Created By" },
    { key: "is_adaptive", header: "Adaptive" },
    { key: "ai_generated", header: "AI Generated" },
    { key: "reviewed", header: "Reviewed" },
    { key: "reviewers", header: "Reviewers" },
];



export const AllQuestions: React.FC<{ skip?: number; limit?: number }> = ({
    skip = 0,
    limit = 100,
}) => {
    const endpoint = `/packages/get_allquestions/${skip}/${limit}`;
    const { data: questions, loading } = useFetch<Question[]>(endpoint, []);
    const router = useRouter();

    if (loading) return <Loading />;

    const { headers, rows } = createTableData<Question>(
        questionColumns,
        questions,
        (key, q) => {
            if (key === 'title') {
                const slug = `${encodeURIComponent(q.title)}_${q.id}`;
                router.push(`/problem/${slug}`);
                console.log(slug)
            }
        }
    );

    return (
        <section className="p-6 bg-white rounded-lg shadow">
            <h2 className="text-2xl font-semibold mb-4">All Questions</h2>
            <Table caption="All Questions" header={headers} data={rows} />
        </section>
    );
};