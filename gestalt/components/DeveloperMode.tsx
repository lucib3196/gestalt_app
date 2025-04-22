import { useEffect, useState } from "react";
import DropDown from "@/components/DropDown";
import { FileNameMap } from "@/utils";
import api from "@/api";
import { Editor } from "@monaco-editor/react";
import ActionButton from "@/components/ActionButton";
import ToggleLanguage from "./ToggleLanguage";
import CodeReview from "./CodeReview";
import { FaSave } from "react-icons/fa";
import { RxUpdate } from "react-icons/rx";

// Types
interface DeveloperModeProps {
  question_id: number;
}

// 🧩 Main Component
const DeveloperMode: React.FC<DeveloperModeProps> = ({ question_id }) => {
  const [files, setFiles] = useState<FileResponse[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [selectedFileContents, setSelectedFileContent] =
    useState<FileResponse | null>(null);
  const [editorContent, setEditorContent] = useState<string>("");

  const fetchFiles = async () => {
    try {
      const response = await api.get(`/packages/simple/${question_id}/files`);
      setFiles(response.data);
    } catch (error) {
      console.error("Error fetching files:", error);
    }
  };

  const options: DropDownOption[] = files.map((file) => ({
    displayName: FileNameMap[file.name].displayName || file.name,
  }));

  const handleDropDownChange = (value: string) => {
    const filename = Object.keys(FileNameMap).find(
      (key) => FileNameMap[key].displayName === value
    );
    filename
      ? setSelectedFile(filename)
      : console.warn(`No matching filename found for: ${value}`);
  };

  useEffect(() => {
    fetchFiles();
  }, [question_id]);

  useEffect(() => {
    const file = files.find((file) => file.name === selectedFile);
    setSelectedFileContent(file ?? null);
    setEditorContent(file?.content ?? "");
  }, [files, selectedFile]);

  return (
    <>
      {/* Header Section */}
      <div className="flex flex-col">
        <div className="text-indigo-700 my-4 text-center text-2xl font-bold">
          Developer Mode
        </div>
        <div className="flex flex-row gap-4 px-2 py-4 items-center">
          <DropDown options={options} onChange={handleDropDownChange} />
          <ToggleLanguage />
          <CodeReview />
        </div>
      </div>

      {/* Code Editor */}
      <Editor
        height="30vh"
        language={
          selectedFileContents
            ? FileNameMap[selectedFileContents.name].language
            : "javascript"
        }
        value={editorContent}
        onChange={(value) => setEditorContent(value ?? "")}
      />

      {/* Action Buttons */}
      <div className="flex gap-2 justify-center  items-baseline m-3">
        <ActionButton
          label="Save"
          icon={<FaSave />}
          onClick={async () => {
            return await api.post("/packages/simple/update_code", {
              content: editorContent,
              question_folder_id: question_id,
              question_file_name: selectedFileContents?.name,
            });
          }}
        />
        <ActionButton
          label="Update"
          icon={<RxUpdate />}
          onClick={async () => {
            //  update logic here
          }}
        />
      </div>
    </>
  );
};

export default DeveloperMode;
