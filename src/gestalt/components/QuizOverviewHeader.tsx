// This will be the header and any metadata
// That we want to show to the user
import { QuestionFolder } from "@/.next/types/QuestionFolder";
import { Question } from "@/.next/types/types";
import { FaTags } from "react-icons/fa";

type QuizOverviewHeaderProps = {
  question: QuestionFolder | Question;
};
type ReviewComponentProps = {
  reviewed: boolean | undefined;
};

const ReviewComponent: React.FC<ReviewComponentProps> = ({ reviewed }) => {
  return (
    <div className="text-sm inline-grid grid-cols-2 gap-4 my-3 mx-2 items-baseline">
      <p className="font-semibold">Reviewed:</p>
      <div
        className={`w-full rounded-full py-2 text-center shadow border font-medium ${reviewed ? "bg-green-500 text-white" : "bg-red-500 text-white"
          }`}
      >
        {reviewed ? "True" : "False"}
      </div>
    </div>
  );
};
const QuizOverviewHeader: React.FC<QuizOverviewHeaderProps> = ({
  question,
}) => {
  return (
    // Main Container
    <div className="flex flex-col justify-center items-center mx-auto px-6 py-8 w-full max-w-3xl gap-y-6">
      {/* Title  */}
      <h1 className="text-gray-900 text-4xl font-extrabold border-b-2 border-gray-200 pb-2 w-full text-center tracking-tight">
        {question?.title?.split(/(?=[A-Z])/).join(" ") ?? "Loading..."}
      </h1>
      {/* Tags for the Section */}
      <div className="flex flex-wrap gap-3 items-center justify-center w-full">
        <span className="flex items-center gap-2 text-gray-600 font-medium">
          <FaTags className="text-lg" />
          <span>Topics:</span>
        </span>
        {question?.topic.map((value, index) => (
          <span
            key={index}
            className="px-4 py-1 text-sm font-semibold border border-gray-300 rounded-full text-gray-700 bg-gray-100 shadow-sm hover:bg-gray-200 transition"
          >
            {value.split(/(?=[A-Z])/).join(" ")}
          </span>
        ))}
        <ReviewComponent reviewed={question.reviewed} />
      </div>
    </div>
  );
};

export default QuizOverviewHeader;
