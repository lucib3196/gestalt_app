import clsx from "clsx";
import React from "react";
import { FaRegCirclePlay } from "react-icons/fa6";
import CourseCard from "@/components/CourseCard";



const ExploreHeader = () => {
    return (
        <div className="flex flex-col mx-5 my-10 gap-y-4 ">
            <h2 className=" text-3xl text-gray-500">Welcome to</h2>
            <h1 className="text-5xl font-bold">Gestalt Explore</h1>
        </div>
    );
};


const PinnedCourses = () => {
    return (<div>
        <h1 className="text-3xl mx-10 mb-10">
            My Pinned Courses
            <hr className="border-black w-1/4 mt-5" />
        </h1>
        <div className="flex flex-row gap-x-10 justify-center-safe">
            <CourseCard
                course_data={20}
                course_name="ME 002 Introduction to Mechanical Engineering"
                additional_description="Lower division course."
                bgColor="bg-gradient-to-r from-red-500 to-red-600"
                isPinned={true}
            />
            <CourseCard
                course_name="Heat Transfer"
                additional_description="Thermal processes"
                course_data={8}
                bgColor="bg-gradient-to-r from-pink-600 to-pink-600"
                isPinned={true}
            />

        </div>
    </div>)

}

const ExploreByCourse = () => {
    return (
        <div>
            <h1 className="text-3xl mx-10 mb-10">
                Explore By Course
                <hr className="border-black w-1/4 mt-5" />
            </h1>
            <div className="flex flex-row gap-x-10 justify-center-safe">
                <CourseCard
                    course_data={20}
                    course_name="ME 002 Introduction to Mechanical Engineering"
                    additional_description="Lower division course."
                    bgColor="bg-gradient-to-r from-red-500 to-red-600"
                />
                <CourseCard
                    course_data={10}
                    course_name="ME 010 Statics"
                    additional_description="Lower division course."
                    bgColor="bg-gradient-to-r from-blue-500 to-blue-600"
                />
                <CourseCard
                    course_data={5}
                    course_name="ME 100A Thermodynamics"
                    additional_description="Upper division course."
                    bgColor="bg-gradient-to-r from-yellow-500 to-yellow-600"
                />
                <CourseCard
                    course_data={5}
                    course_name="ME 103 Dynamics"
                    additional_description="Upper division course."
                    bgColor="bg-gradient-to-r from-purple-500 to-purple-600"
                />

            </div>
        </div>)
}


const ExploreByTopic = () => {
    return (
        <div>
            <h1 className="text-3xl mx-10 mb-10">
                Explore By Topic
                <hr className="border-black w-1/4 mt-5" />
            </h1>
            <div className="flex flex-row gap-x-10 justify-center-safe">
                <CourseCard
                    course_name="Statics"
                    additional_description="Force analysis"
                    course_data={7}
                    bgColor="bg-gradient-to-r from-blue-500 to-blue-600"
                />
                <CourseCard
                    course_name="Thermodynamics"
                    additional_description="Energy systems"
                    course_data={6}
                    bgColor="bg-gradient-to-r from-red-500 to-pink-600"
                />
                <CourseCard
                    course_name="Dynamics"
                    additional_description="Motion & kinematics"
                    course_data={9}
                    bgColor="bg-gradient-to-r from-indigo-500 to-indigo-600"
                />

                <CourseCard
                    course_name="Heat Transfer"
                    additional_description="Thermal processes"
                    course_data={8}
                    bgColor="bg-gradient-to-r from-pink-600 to-pink-600"
                />
            </div>
        </div>)
}


export default function Page() {
    return (
        <section className="flex flex-col gap-y-10 mb-10">
            {/* Page Title */}
            <ExploreHeader />
            <PinnedCourses />
            <ExploreByCourse />
            <ExploreByTopic />

        </section>
    );
}
