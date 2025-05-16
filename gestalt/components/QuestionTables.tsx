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
  name: string;
  options: string | React.ReactElement;
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
  filename: string;
  content: string;
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

interface PackageContents {
  package: { id: number; name: string };
  questions: Question[];
  files: File[];
}

// ==============================
// Column Definitions
// ==============================

const packageColumns: ColumnConfig<Package>[] = [
  { key: "id", header: "ID" },
  {
    key: "name",
    header: "Package Name",
    classes: {
      row: "underline text-blue-600 hover:text-blue-800 cursor-pointer",
    },
  },
  {
    key: "options",
    header: "Options",
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
    key: "filename",
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
  if (React.isValidElement(val)) {
    return val;
  }
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

function useFetch<T>(endpoint: string, initialData: T) {
  const [data, setData] = useState<T>(initialData);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<T>(endpoint)
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

type OptionsModalProps = {
  method: string;
  requestUrl: string;
  onClick: () => void;
};

const OptionsModal: React.FC<OptionsModalProps> = ({
  method,
  requestUrl,
  onClick,
}) => {
  const handleRequest = async () => {
    try {
      await api.delete(requestUrl);
      console.log("Package deleted successfully");
      onClick(); // Close the modal after successful deletion
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };

  return (
    <div
      className="fixed bottom-0 left-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
      role="dialog"
      aria-labelledby="modal-title"
      aria-modal="true"
    >
      <div className="bg-white p-6 rounded shadow">
        <p id="modal-title" className="font-bold">
          Are you sure you want to delete this package?
        </p>
        <div className="mt-4 flex flex-row justify-evenly gap-4">
          <button
            onClick={onClick}
            className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
          >
            Close
          </button>
          <button
            onClick={handleRequest}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};
export const AllPackages: React.FC = () => {
  // Hard code
  const skip = 0;
  const limit = 100;

  const { data: packages, loading } = useFetch<Package[]>(
    `/packages/get_packages/${skip}/${limit}`,
    []
  );
  const router = useRouter();

  const [showOverlay, setShowOverlay] = useState(false);
  const [currentPackage, setCurrentPackage] = useState<number | string | null>(
    null
  );

  packages.forEach((pkg) => {
    pkg.options = (
      <button
        onClick={() => {
          setCurrentPackage(pkg.id);
          setShowOverlay(true); // Show the overlay when the button is clicked
        }}
        className="rounded-xl px-3 py-2 bg-red-500 font-bold hover:bg-red-800 hover:text-white"
      >
        Delete
      </button>
    );
  });

  if (loading) return <Loading />;

  const { headers, rows } = createTableData<Package>(
    packageColumns,
    packages,
    (key, pkg) => {
      if (key === "name") router.push(`/packages/${pkg.id}`);
    }
  );

  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4">All Packages</h2>
      <Table caption="All Packages" header={headers} data={rows} />
      {showOverlay && (
        <OptionsModal
          method={"delete"}
          requestUrl={`/packages/delete_package/${currentPackage}`}
          onClick={() => setShowOverlay(false)}
        />
      )}
    </section>
  );
};

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
  const { data: questions, loading } = useFetch<Question[]>(
    `/packages/get_package/${package_id}/get_questions`,
    []
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
  const { data: files, loading } = useFetch<File[]>(
    `/packages/${question_id}/get_question_files`,
    []
  );
  const router = useRouter();
  console.log("These are the files", files);

  if (loading) return <Loading />;

  const { headers, rows } = createTableData<File>(
    fileColumns,
    files,
    (key, q) => {
      if (key === "filename") router.push(`/code_editor/${q.id}`);
    }
  );

  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <Table caption="Question Files" header={headers} data={rows} />
    </section>
  );
};

export const PackageContents: React.FC = () => {
  const { package_id } = useParams() as { package_id: string };
  const { data: contents, loading } = useFetch<PackageContents>(
    `/packages/get_package/${package_id}/get_all_contents`,
    {
      package: { id: 0, name: "" },
      questions: [],
      files: [],
    }
  );
  const router = useRouter();
  const questions = contents.questions;
  const files = contents.files;

  console.log(files);

  const { headers: fileHeaders, rows: fileRows } = createTableData<File>(
    fileColumns,
    files,
    (key, q) => {
      if (key === "filename")
        router.push(`/packages/folder/file/${q.filename}`);
    }
  );

  const { headers: questionHeaders, rows: questionRows } =
    createTableData<Question>(questionColumns, questions, (key, q) => {
      if (key === "title") router.push(`/packages/folder/${q.id}`);
    });

  // Unpack the contents and get the values
  return (
    <section className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-semibold mb-4">
        Questions in Package {package_id}
      </h2>
      <Table caption="Question Files" header={fileHeaders} data={fileRows} />
      <Table
        caption="Package Questions"
        header={questionHeaders}
        data={questionRows}
      />
    </section>
  );
};
