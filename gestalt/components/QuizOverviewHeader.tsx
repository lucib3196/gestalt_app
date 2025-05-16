// This will be the header and any metadata
// That we want to show to the user
import { QuestionFolder } from "@/.next/types/QuestionFolder";
import { FaTags } from "react-icons/fa";

type QuizOverviewHeaderProps = {
  question: QuestionFolder;
};
type ReviewComponentProps = {
  reviewed: boolean | undefined;
};

const ReviewComponent: React.FC<ReviewComponentProps> = ({ reviewed }) => {
  return (
    <div className="text-sm inline-grid grid-cols-2 gap-4 my-3 mx-2 items-baseline">
      <p className="font-semibold">Reviewed:</p>
      <div
        className={`w-full rounded-full py-2 text-center shadow border font-medium ${
          reviewed ? "bg-green-500 text-white" : "bg-red-500 text-white"
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
    <div className="flex flex-col justify-between items-center mx-auto px-3 py-6">
      {/* Title  */}
      <h1 className="text-gray-800 text-xl font-bold border-b-2 pb-1">
        {question?.title?.split(/(?=[A-Z])/).join(" ") ?? "Loading..."}
      </h1>
      {/* Tags for the Section */}
      <div className="flex flex-row gap-x-3 items-baseline justify-evenly">
        <FaTags />
        {question?.tags.map((value, index) => (
          <span
            key={index}
            className="px-3 py-1 text-sm font-semibold border rounded-full text-gray-700 bg-white shadow"
          >
            {value.split(/(?=[A-Z])/).join(" ")}
          </span>
        ))}
      </div>
      {/* Show the status of the review */}
      <ReviewComponent reviewed={question.reviewed} />
    </div>
  );
};

export default QuizOverviewHeader;
