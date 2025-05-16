"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import api from "@/api";

import remarkMath from "remark-math";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

interface HeadingProps {
  children: React.ReactNode;
}

// Custom H1
const LectureH1: React.FC<HeadingProps> = ({ children }) => (
  <h1 className="lecture_h1">{children}</h1>
);

// Custom H2
const LectureH2: React.FC<HeadingProps> = ({ children }) => (
  <h2 className="lecture_h2">{children}</h2>
);

const MarkdownRenderer: React.FC<{ content: string }> = ({ content }) => (
  <ReactMarkdown
    remarkPlugins={[remarkMath]}
    rehypePlugins={[rehypeSlug, rehypeAutolinkHeadings, rehypeKatex]}
    components={{
      h1: ({ children, ...props }) => (
        <LectureH1 {...props}>{children}</LectureH1>
      ),
      h2: ({ children, ...props }) => (
        <LectureH2 {...props}>{children}</LectureH2>
      ),
      // add more overrides here…
    }}
  >
    {content}
  </ReactMarkdown>
);

const Page: React.FC = () => {
  const [fileContent, setFileContent] = useState<string>("");
  const { filename } = useParams() as { filename: string };
  const packageId = 25;

  useEffect(() => {
    if (!filename) return;

    const fetchFile = async () => {
      try {
        const { data } = await api.get<{ content: string }>(
          `/packages/get_package/${packageId}/${filename}/get_file`
        );
        setFileContent(data.content);
      } catch (err) {
        console.error("Error fetching file:", err);
      }
    };

    fetchFile();
  }, [filename, packageId]);

  return (
    <section className="flex justify-center my-10 px-4">
      <div className="prose w-full max-w-5xl p-8 bg-white rounded-lg shadow-md border border-gray-200">
        <MarkdownRenderer content={fileContent} />
      </div>
    </section>
  );
};

export default Page;
