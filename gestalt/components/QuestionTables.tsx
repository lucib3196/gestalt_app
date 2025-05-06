// src/components/DataTables.tsx

import React, { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import api from "@/api";
import Table, { TableHeader, TableCell } from "@/components/Table";

// ==============================
// Types & Interfaces
// ==============================

interface Package {
  id: number;
  title: string;
}

interface Question {
  id: number;
  title: string;
  topic: string[];
  tags: string[];
  pre_reqs: string[];
  is_adaptive: boolean;
  ai_generated: boolean;
  created_by: string;
  reviewers: string;
  reviewed: boolean;
  package_id: number;
}

interface File {
  id: number;
  name: string;
  content: string;
  save_name: string;
}

interface TableClasses {
  header?: string;
  row?: string;
}

interface ColumnConfig<T> {
  key: keyof T;
  header: string;
  classes?: TableClasses;
}

// ==============================
// Column Definitions
// ==============================

const packageColumns: ColumnConfig<Package>[] = [
  { key: "id", header: "ID" },
  {
    key: "title",
    header: "Package Name",
    classes: {
      row: "underline text-blue-600 hover:text-blue-800 cursor-pointer",
    },
  },
];

const questionColumns: ColumnConfig<Question>[] = [
  { key: "id", header: "ID" },
  {
    key: "title",
    header: "Question Title",
    classes: {
      row: "underline text-blue-600 hover:text-blue-800 cursor-pointer",
    },
  },
  { key: "topic", header: "Topic" },
  { key: "tags", header: "Tags" },
  { key: "pre_reqs", header: "Pre-Reqs" },
  { key: "created_by", header: "Created By" },
  { key: "is_adaptive", header: "Adaptive" },
  { key: "ai_generated", header: "AI Generated" },
  { key: "reviewed", header: "Reviewed" },
  { key: "reviewers", header: "Reviewers" },
];

const fileColumns: ColumnConfig<File>[] = [
  {
    key: "name",
    header: "File Name",
    classes: {
      row: "underline text-blue-600 hover:text-blue-800 cursor-pointer",
    },
  },
];

// ==============================
// Helpers & Hooks
// ==============================

const formatCellValue = (val: any): React.ReactNode => {
  if (typeof val === "boolean") {
    return val ? (
      <span className="inline-block px-2 py-1 bg-green-200 rounded text-sm">
        True
      </span>
    ) : (
      <span className="inline-block px-2 py-1 bg-red-200 rounded text-sm">
        False
      </span>
    );
  }
  if (Array.isArray(val)) return val.join(", ");
  if (val === null || val === undefined)
    return <span className="text-gray-400">None</span>;
  return val.toString();
};

function createTableData<T>(
  columns: ColumnConfig<T>[],
  data: T[],
  onClick?: (key: keyof T, row: T) => void
) {
  const headers: TableHeader[] = columns.map((col) => ({ label: col.header }));
  const rows: TableCell[][] = data.map((row) =>
    columns.map((col) => ({
      value: formatCellValue(row[col.key]),
      className: col.classes?.row,
      onClick: onClick ? () => onClick(col.key, row) : undefined,
    }))
  );
  return { headers, rows };
}

function useFetch<T>(endpoint: string) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<T[]>(endpoint)
      .then((res) => setData(res.data))
      .catch(() => console.error(`Failed to fetch ${endpoint}`))
      .finally(() => setLoading(false));
  }, [endpoint]);

  return { data, loading };
}

const Loading: React.FC = () => (
  <div className="flex items-center justify-center h-32">
    <p className="text-gray-500">Loading…</p>
  </div>
);

// ==============================
// Components
// ==============================

export const AllPackages: React.FC = () => {
  const { data: packages, loading } = useFetch<Package>("/packages/get_all");
  const router = useRouter();

  if (loading) return <Loading />;

  const { headers, rows } = createTableData<Package>(
    packageColumns,
    packages,
    (key, pkg) => {
      if (key === "title") router.push(`/packages/${pkg.id}`);
    }
  );

  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4">All Packages</h2>
      <Table caption="All Packages" header={headers} data={rows} />
    </section>
  );
};

export const AllQuestions: React.FC<{ skip?: number; limit?: number }> = ({
  skip = 0,
  limit = 100,
}) => {
  const endpoint = `/packages/simple/${skip}/${limit}/get_all_folders`;
  const { data: questions, loading } = useFetch<Question>(endpoint);
  const router = useRouter();

  if (loading) return <Loading />;

  const { headers, rows } = createTableData<Question>(
    questionColumns,
    questions,
    (key, q) => {
      if (key === "title") router.push(`/packages/folder/${q.id}`);
    }
  );

  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4">All Questions</h2>
      <Table caption="All Questions" header={headers} data={rows} />
    </section>
  );
};

export const PackageQuestions: React.FC = () => {
  const { package_id } = useParams() as { package_id: string };
  const { data: questions, loading } = useFetch<Question>(
    `/packages/${package_id}/get_all_folders`
  );
  const router = useRouter();

  if (loading) return <Loading />;

  const { headers, rows } = createTableData<Question>(
    questionColumns,
    questions,
    (key, q) => {
      if (key === "title") router.push(`/packages/folder/${q.id}`);
    }
  );

  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4">
        Questions in Package {package_id}
      </h2>
      <Table caption="Package Questions" header={headers} data={rows} />
    </section>
  );
};

export const QuestionFiles: React.FC<{ question_id: string }> = ({
  question_id,
}) => {
  const { data: files, loading } = useFetch<File>(
    `/packages/${question_id}/get_question_files`
  );
  const router = useRouter();

  if (loading) return <Loading />;

  const { headers, rows } = createTableData<File>(
    fileColumns,
    files,
    (key, q) => {
      if (key === "name") router.push(`/code_editor/${q.id}`);
    }
  );

  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <Table caption="Question Files" header={headers} data={rows} />
    </section>
  );
};
