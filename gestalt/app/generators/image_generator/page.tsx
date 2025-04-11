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
  const [filesData, setFilesData] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilesData(e.target.files);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!filesData) return;

    const formData = new FormData();
    for (let i = 0; i < filesData.length; i++) {
      formData.append("files", filesData[i]);
    }

    setLoading(true);

    // Do the API Request
    try {
      const response = await api.post("/image_upload/uploadfiles/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log(response.data);
    } catch (error) {
      console.log("Error submitting form");
    } finally {
      setLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <input
        type="file"
        name="filesData"
        multiple
        onChange={handleChange}
        className="form-control"
      />
      <button type="submit" className="btn btn-primary mt-2" disabled={loading}>
        {loading ? "Uploading..." : "Upload Files"}
      </button>
    </form>
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
