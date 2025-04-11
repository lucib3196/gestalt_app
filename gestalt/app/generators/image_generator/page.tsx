"use client";

import React, { useState } from "react";
import ModGenerators from "@/components/ModGenerators";
import "@/styles/ModGeneratorStyles.css";
import api from "@/api";

const ImageGeneratorConst = {
  name: "Visual Extract",
};

const examples = [
  {
    name: "Textbook Solutions",
    text: "Officially published problems and solutions ensure high accuracy.",
  },
  {
    name: "Handwritten Solutions",
    text: "Personal notes or handwritten solutions will be effectively processed.",
  },
  {
    name: "Lecture Materials",
    text: "Slides or instructional content from lectures can be used to create modules.",
  },
];

const FileUploadForm: React.FC = () => {
  const [folderName, setFolderName] = useState<string>("");
  const [fileList, setFileList] = useState<FileList | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFileList(e.target.files);
  };

  const handleFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFolderName(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!fileList) return;

    const formData = new FormData();
    formData.append("folder_name", folderName);

    for (let i = 0; i < fileList.length; i++) {
      formData.append("files", fileList[i]);
    }

    setLoading(true);

    try {
      const response = await api.post(
        "/code_generator_chains/v1/image_upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Upload successful:", response.data);
    } catch (error) {
      console.error("Error submitting form", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-gen-form">
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <input
        type="text"
        name="folder_name"
        className="form-control mb-2"
        value={folderName}
        onChange={handleFolderChange}
        placeholder="Folder Name"
        required
      />

      <input
        type="file"
        name="files"
        multiple
        onChange={handleFileChange}
        className="form-control mb-3"
      />

      <button
        type="submit"
        className="btn btn-primary"
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload Files"}
      </button>
    </form>
    </div>
  );
};

export default function ImageGenerator() {
  return (
    <ModGenerators
      title={ImageGeneratorConst.name}
      subtitle="Upload your images below to generate personalized modules instantly."
      examples={examples}
      inputComponent={<FileUploadForm />}
    />
  );
}
