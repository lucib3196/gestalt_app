import React from "react";
import { useState, useEffect } from "react";
import type { ModuleSimple } from "~/types/types";
import api from "~/api";
import ModuleTable from "~/components/ModuleTable";
import "~/styles/ModuleTable.css";


function ModulePage() {
  const [modules, setModules] = useState<ModuleSimple[]>([]);

  const fetchModules = async () => {
    try {
      const response = await api.get("/modules/simple");
      setModules(response.data);
    } catch (error) {
      console.log("Error Fetching Modules", error);
    }
  };

  useEffect(() => {
    fetchModules(), [];
  });

  return (
    <div className="table-container">
        <ModuleTable modules={modules} />
    </div>
  )
  
}

export default ModulePage;
