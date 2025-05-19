"use client";
import React, { useEffect, useState } from "react";
import { AllPackages, AllQuestions } from "@/components/QuestionTables";
import { ToggleOptions } from "@/components/ToggleLanguage";

const Page: React.FC = () => {
  const [tableView, setTableView] = useState("AllPackages");

  const handleToggle = (option: string) => {
    setTableView(option.replace(" ", ""));
  };

  return (
    <>
      <div className="m-5 relative">
        <ToggleOptions
          initialVal={tableView}
          options={["AllPackages", "AllQuestions"]}
          onClick={handleToggle}
          tipMessage={{
            text: "Toggle Table View",
            message: "Toggle Table View",
          }}
        />
      </div>

      {tableView === "AllPackages" && (
        <div className="m-5">
          <AllPackages />
        </div>
      )}

      {tableView === "AllQuestions" && (
        <div className="m-5">
          <AllQuestions />
        </div>
      )}
    </>
  );
};

export default Page;
