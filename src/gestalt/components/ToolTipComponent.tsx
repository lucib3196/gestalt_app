import { CiCircleInfo } from "react-icons/ci";



interface TooltipExampleProps {
  text: string;
  message: string;
}
 const TooltipExample: React.FC<TooltipExampleProps> = ({ text, message }) => (
  <div className="relative group inline-flex items-center space-x-1">
    <span className="text-gray-800">{text}</span>
    <CiCircleInfo className="text-blue-500 cursor-pointer" />
    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block bg-gray-800 text-white text-sm px-3 py-1 rounded shadow-lg">
      {message}
    </div>
  </div>
);

export default TooltipExample