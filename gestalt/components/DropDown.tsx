import { useEffect, useState } from "react";
import { FileNameMap } from "@/utils";

const DropDown: React.FC<DropDownProps> = ({ options, onChange }) => {
  const [selectedFile, setSelectedFile] = useState("");

  // Define the default value by using the first file in the list
  useEffect(() => {
    if (options.length > 0 && !selectedFile) {
      const defaultOption = options[0].displayName;

      setSelectedFile(defaultOption);
      onChange?.(defaultOption); //Return the files object
    }
  }, [options]);

  const handleDropDownChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setSelectedFile(event.target.value);
    onChange?.(event.target.value);
  };

  const prepareOptions = () => {
    return options.map((option) => (
      <option
        key={option.displayName}
        value={option.displayName}
        className="text-blue-950 text-sm font-medium text-center"
      >
        {option.displayName}
      </option>
    ));
  };
  
  return (
    <select
      className="border-2 border-indigo-600 rounded-md px-3 py-2 text-blue-950 font-medium text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-1 transition"
      onChange={handleDropDownChange}
      value={selectedFile}
    >
      {prepareOptions()}
    </select>
  );
};

export default DropDown;
