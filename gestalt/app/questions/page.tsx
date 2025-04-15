"use client";
import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import LoadingComponent from "@/components/LoadingComponent";
import { useRouter } from "next/navigation";
import api from "@/api";

type QuestionFolderResponse = {
  id: number;
  title: string;
  topic: string[];
  tags: string[];
  pre_reqs: string[];
  is_adaptive: boolean;
  ai_generated: boolean;
  created_by: string[];
  reviewed: boolean;
};

type QuestionTableProps = {
  questionData: QuestionFolderResponse[];
};

const QuestionTable: React.FC<QuestionTableProps> = ({ questionData }) => {
  if (questionData.length === 0) {
    return <div>No data available.</div>;
  }

  const headers = Object.keys(
    questionData[0]
  ) as (keyof QuestionFolderResponse)[];

  return (
    <>
      <table className="table table-striped">
        <thead>
          <tr>
            {headers.map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {questionData.map((item, index) => (
            <tr key={index}>
              {headers.map((key) => (
                <td key={key}>{String(item[key])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

const QuestionPage: React.FC = () => {
  const [Question, setQuestions] = useState<QuestionFolderResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  // Currently Pagination is hard coded
  const fetchQuestions = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/packages/simple/0/10/get_all_folders`);
      console.log(response.data);
      setQuestions(response.data);
    } catch (error) {
      console.log("There was an error getting the folders");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  return (
    <div className="container-fluid m-4">
      page
      <QuestionTable questionData={Question} />
    </div>
  );
};

export default QuestionPage;
