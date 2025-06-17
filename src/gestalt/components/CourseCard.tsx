import clsx from "clsx";
import React from "react";
import { FaRegCirclePlay } from "react-icons/fa6";
import { MdOutlineStar } from "react-icons/md";

type CourseCardProps = {
    course_name: string;
    course_data: number;
    additional_description?: string;
    bgColor: string;
    isPinned?: boolean;
};

const CourseCard: React.FC<CourseCardProps> = ({
    course_name,
    course_data,
    additional_description,
    bgColor = "bg-black",
    isPinned = false
}) => {
    return (
        <div className="relative flex flex-col size-80  rounded-2xl bg-white border border-gray-200 shadow-lg overflow-hidden transition-transform hover:scale-101 hover:shadow-2xl">
            {/* Card Header */}
            <div className={`flex flex-col ${bgColor} p-6 text-center gap-y-3 h-3/4`}>
                <div>
                    {isPinned && (
                        <MdOutlineStar
                            className="absolute top-0 right-0"
                            size={40}
                            color="#facc15" // Tailwind yellow-400 hex
                            fill="#facc15"
                        />
                    )}
                    {additional_description && (
                        <h2 className="text-sm text-blue-100 font-medium">{additional_description}</h2>
                    )}
                </div>

                <h3 className="font-bold text-2xl text-white">{course_name} </h3>
            </div>
            {/* Card Bottom */}
            <div className="flex flex-row grow items-center justify-between px-6 py-4 bg-gray-50 ">
                <span className="text-gray-600 text-base">Number of Questions</span>
                <span className="text-blue-600 font-bold text-lg">{course_data}</span>
                <button>
                    <FaRegCirclePlay size={35} />
                </button>
            </div>
        </div>
    );
};


export default CourseCard