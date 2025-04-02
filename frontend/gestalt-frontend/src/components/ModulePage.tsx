import React from "react";
import api from "../api";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

type Module = {
  id: number;
  name: string;
};

function ModuleList() {
  const [modules, setModules] = useState<Module[]>([]);
  const navigate = useNavigate();

  const fetchModules = async () => {
    try {
      const response = await api.get("/modules/simple");
      setModules(response.data);
    } catch (error) {
      console.error("Error fetching Modules", error);
    }
  };
  
  const handleLink = async (moduleId: number) => {
    try {
      const response = await api.get(`/modules/simple/${moduleId}`);
      console.log(`Generated module ${moduleId}:`, response.data);
      navigate(`/modules/${moduleId}`);
    } catch (error) {
      console.error(`Error generating module ${moduleId}`, error);
    }
  };

  useEffect(() => {
    fetchModules();
  }, []);
  const table_cols = ["#", "Title"];
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
              <td><a onClick={(e)=>{
                e.preventDefault();
                handleLink(module.id)
              }}>{module.name}</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function ModulePage() {
  return (
    <div>
      <ModuleList />
    </div>
  );
}
