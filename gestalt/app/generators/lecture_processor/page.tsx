"use client";
import React, { useState, useRef } from "react";
import ModGenerator from "@/components/ModGeneratorsV2";
import { ToggleOptions } from "@/components/ToggleLanguage";
import api from "@/api";
import { ToastContainer, toast } from "react-toastify";

// Toast Buttons
const handleSuccess = () => {
  toast.success("Generation Successful"),
    {
      position: "top-right",
      autoClose: 3000,
      closeOnClick: true,
    };
};

// Input Form For Generator
const LectureForm: React.FC = () => {
  // Input Parameters
  const [lectureName, setLectureName] = useState<string>("");
  const [courseName, setCourseName] = useState<string>("");
  const [courseId, setCourseId] = useState<string>("");
  const [instructorName, setInstructorName] = useState<string>("");
  const [semester, setSemester] = useState<string>("");
  const [lectureDate, setLectureDate] = useState<string>("");
  const [fileList, setFileList] = useState<FileList | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Additional datqa
  const [processingMethod, setProcessingMethod] = useState("EntireBatch");
  // Const
  const MAXFILESIZE = 20;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;

    const files = Array.from(e.target.files);
    const oversizedFiles = files.filter(
      (file) => file.size > MAXFILESIZE * 1024 * 1024
    );
    if (oversizedFiles.length > 0) {
      alert(
        `Some files are larger than ${MAXFILESIZE} MB and were not accepted.`
      );
      return;
    }
    setFileList(e.target.files);
  };
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleProcessChange = (option: string) => {
    setProcessingMethod(option);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    if (!fileList) return;

    const formData = new FormData();
    formData.append("lecture_title", lectureName);
    formData.append("course_name", courseName);
    formData.append("course_code", courseId);
    formData.append("instructor_name", instructorName);
    formData.append("lecture_date", lectureDate);
    formData.append("semester", semester);

    // Append all files or a single file, based on backend expectation
    for (let i = 0; i < fileList.length; i++) {
      formData.append("file", fileList[i]);
    }

    console.log("Submitting the form ");
    try {
      const response = await api.post("/codegen_v2/process_lecture", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Upload successful:", response.data);
    } catch (error) {
      console.error("Error submitting form", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      className="border-t-2 border-darkShades"
      onSubmit={handleSubmit}
      encType="multipart/form-data"
    >
      <div className="space-y-1 flex flex-col items-center justify-center">
        <div className="mt-3 border-b border-gray-900/10 pb-4 text-center">
          Lecture Metadata
        </div>
        <p className="mt-1 !text-sm/6 !text-gray-600">
          Information about the lecture
        </p>

        {/* Container with all the inputs */}
        <div className="flex flex-row justify-center flex-wrap gap-x-5 gap-y-5">
          {/* Instructor Name */}
          <div className="mt-3 flex flex-col">
            <label
              htmlFor="instructorName"
              className="block text-sm/6 font-medium !text-gray-900"
            >
              Instructor Name
            </label>
            <div className="mt-2">
              <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <input
                  type="text"
                  name="instructorName"
                  id="instructorName"
                  required
                  value={instructorName}
                  onChange={(e) => setInstructorName(e.target.value)}
                  className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  placeholder="Prof Feynman"
                />
              </div>
            </div>
          </div>

          {/* Lecture Name */}
          <div className="mt-3 flex flex-col">
            <label
              htmlFor="lectureName"
              className="block text-sm/6 font-medium !text-gray-900"
            >
              Lecture Name
            </label>
            <div className="mt-2">
              <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <input
                  type="text"
                  name="lectureName"
                  id="lectureName"
                  value={lectureName}
                  required
                  onChange={(e) => setLectureName(e.target.value)}
                  className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  placeholder="Thermodynamics Lecture 1"
                />
              </div>
            </div>
          </div>

          {/* Course Name */}
          <div className="mt-3 flex flex-col">
            <label
              htmlFor="courseName"
              className="block text-sm/6 font-medium !text-gray-900"
            >
              Course Name
            </label>
            <div className="mt-2">
              <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <input
                  type="text"
                  name="courseName"
                  id="courseName"
                  value={courseName}
                  required
                  onChange={(e) => setCourseName(e.target.value)}
                  className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  placeholder="Thermodynamics"
                />
              </div>
            </div>
          </div>

          {/* Course ID */}
          <div className="mt-3 flex flex-col">
            <label
              htmlFor="courseId"
              className="block text-sm/6 font-medium !text-gray-900"
            >
              Course ID
            </label>
            <div className="mt-2">
              <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <input
                  type="text"
                  name="courseId"
                  id="courseId"
                  required
                  value={courseId}
                  onChange={(e) => setCourseId(e.target.value)}
                  className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  placeholder="100A"
                />
              </div>
            </div>
          </div>

          {/* Lecture Date */}
          <div className="mt-3 flex flex-col">
            <label
              htmlFor="lectureDate"
              className="block text-sm/6 font-medium !text-gray-900"
            >
              Lecture Date
            </label>
            <div className="mt-2">
              <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <input
                  type="date"
                  name="lectureDate"
                  id="lectureDate"
                  value={lectureDate}
                  onChange={(e) => setLectureDate(e.target.value)}
                  className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                />
              </div>
            </div>
          </div>

          {/* Semester */}
          <div className="mt-3 flex flex-col">
            <label
              htmlFor="semester"
              className="block text-sm/6 font-medium !text-gray-900"
            >
              Semester
            </label>
            <div className="mt-2">
              <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600">
                <input
                  type="text"
                  name="semester"
                  id="semester"
                  value={semester}
                  onChange={(e) => setSemester(e.target.value)}
                  className="block min-w-0 grow py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6"
                  placeholder="Spring 2025"
                />
              </div>
            </div>
          </div>
        </div>
        {/* Container for the Image Upload */}
        <div className="w-7/10 mt-2">
          <label
            htmlFor="file-upload"
            className="block !text-sm/6 !font-medium !text-gray-900"
          >
            Lecture Material
          </label>
          <div className="flex flex-col my-4">
            <ToggleOptions
              initialVal={processingMethod}
              options={["EntireBatch", "EachFileIndividually"]}
              onClick={handleProcessChange}
              tipMessage={{
                text: "Processing Mode",
                message:
                  "Choose how to process your uploads: process all files together as one unit or handle each file separately.",
              }}
            />
          </div>

          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              setFileList(e.dataTransfer.files);
            }}
            className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10"
          >
            <div className="!text-center flex flex-col justify-center items-center">
              <svg
                className="mx-auto size-12 text-gray-300"
                viewBox="0 0 24 24"
                fill="currentColor"
                aria-hidden="true"
                data-slot="icon"
              >
                <path
                  fillRule="evenodd"
                  d="M1.5 6a2.25 2.25 0 0 1 2.25-2.25h16.5A2.25 2.25 0 0 1 22.5 6v12a2.25 2.25 0 0 1-2.25 2.25H3.75A2.25 2.25 0 0 1 1.5 18V6ZM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0 0 21 18v-1.94l-2.69-2.689a1.5 1.5 0 0 0-2.12 0l-.88.879.97.97a.75.75 0 1 1-1.06 1.06l-5.16-5.159a1.5 1.5 0 0 0-2.12 0L3 16.061Zm10.125-7.81a1.125 1.125 0 1 1 2.25 0 1.125 1.125 0 0 1-2.25 0Z"
                  clipRule="evenodd"
                />
              </svg>
              <div className="mt-4 flex text-sm/6 text-gray-600">
                <label htmlFor="file-upload" className="sr-only"></label>
                <input
                  type="file"
                  name="files"
                  multiple
                  accept="image/*,application/pdf"
                  className="hidden"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  required
                />
                <p className="text-gray-500">
                  <span
                    className="text-indigo-600 font-bold text-lg cursor-pointer"
                    onClick={() => fileInputRef.current?.click()}
                  >
                    Click Here
                  </span>{" "}
                  or drag & drop image files here
                </p>
              </div>
              <p className="text-xs/5 text-gray-600">
                PNG, JPG, PDF up to 20MB
              </p>
              {fileList &&
                Array.from(fileList).map((file, index) => (
                  <p key={index} className="text-sm text-gray-700 mt-1">
                    <span className="font-bold">File Name: </span>
                    {file.name}
                  </p>
                ))}
            </div>
          </div>
        </div>
        <button
          type="submit"
          className="mt-2 !rounded-xl font-bold  text-center bg-indigo-600 text-white px-5 py-3 hover:bg-indigo-800  "
          disabled={loading}
          // onClick={handleSuccess}
        >
          {loading ? "Processing..." : "Upload"}
        </button>
        <ToastContainer />
      </div>
    </form>
  );
};

// Information about the generators
const Examples = [
  {
    exampleName: "PDF Lecture Notes",
    exampleText:
      "Lecture slides, outlines, or notes exported as PDFs are parsed and converted into clean summaries, derivations, and questions.",
  },
  {
    exampleName: "Handwritten Notes",
    exampleText: "Notebook pages, whiteboard captures, or tablet-written notes",
  },
  {
    exampleName: "Lecture Slide Images",
    exampleText:
      "Screenshots of PowerPoint slides, chalkboard photos, or projector captures are processed into modules with summaries, key concepts, and step-by-step solutions.",
  },
];
const LectureModInfo = {
  title: "Lecture Pack",
  subtitle:
    "Upload your lecture materials to convert them into structured, editable learning modules.",
  examples: Examples,
  formComponent: LectureForm,
};
const Page: React.FC = () => {
  return (
    <div className="flex justify-center">
      <ModGenerator {...LectureModInfo} />
    </div>
  );
};

export default Page;
