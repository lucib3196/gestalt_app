import api from "../api";
import  { useEffect, useState } from "react";

// Correct typing for your module
type Module = {
  id: number;
  title: string;
  topic: string;
  reviewed: boolean;
  difficulty: string;
  classes: string[];
};

function ModuleList() {
  const [modules, setModules] = useState<Module[]>([]);

  const fetchModules = async () => {
    try {
      const response = await api.get("/modules");
      setModules(response.data);
    } catch (error) {
      console.error("Error fetching Modules", error);
    }
  };

  useEffect(() => {
    fetchModules();
  }, []);

  const table_cols = [
    "#",
    "Title",
    "Topics",
    "Difficulty",
    "Classes",
    "Reviewed",
  ];

  return (
    <div>
      <h2 className="list-group">Module List</h2>
      <table className="table">
        <thead>
          <tr>
            {table_cols.map((col, index) => (
              <th scope="col" key={index}>
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {modules.map((module) => (
            <tr key={module.id}>
              <th scope="row">{module.id}</th>
              <td>{module.title}</td>
              <td>{module.topic}</td>
              <td>{module.difficulty}</td>
              <td>{module.classes}</td>
              <td>{module.reviewed ? "True" : "False"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ModuleList;
