import api from "../api";
import React, { useEffect, useState } from "react";

// Correct typing for your module
type Module = {
  id: number;              // changed from Int16Array to number
  title: string;
  topic: string;
  reviewed: boolean;
  difficulty: string;
};

function ModuleList() {
  const [modules, setModules] = useState<Module[]>([]);

  const fetchModules = async () => {
    try {
      const response = await api.get<{ modules: Module[] }>("/modules");
      setModules(response.data); // fix here
    } catch (error) {
      console.error("Error fetching Modules", error);
    }
  };

  useEffect(() => {
    fetchModules();
  }, []);

  return (
    <div>
      <h2>Module List</h2>
      <ul>
        {modules.map((module) => (
          <li key={module.id}>
            {module.title} – {module.topic} – Difficulty: {module.difficulty}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ModuleList;
