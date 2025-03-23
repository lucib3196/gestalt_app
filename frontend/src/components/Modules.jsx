import React, { useEffect, useState } from "react";
import api from "../api.js";
import './Modules.css';

const ModuleItem = ({ module }) => {
    const review_status = module.reviewed ? "Reviewed" : "Not Reviewed";
  
  
    return (
    <tr key={module.id} >
    <td className="module_col module_title">{module.title}</td>
    <td className="module_col module_topic">{module.topic}</td>
    <td className="module_col module_subtopics">{module.subtopic}</td>
    <td className="module_col difficulty">{module.difficulty}</td>
    <td className="module_col created_by">{module.created_by}</td>
    <td className="reviewed module_col">{review_status}</td>
    </tr>
  );
};


const ModuleTable = () => {
    // Default state an empty list of modules
    const [modules, setModules] = useState([]);

    const fetchModules = async () => {

      try {
        const response = await api.get("/modules");
        console.log(response.data);
        setModules(response.data);
      } catch (error) {
        console.error("Error fetching modules", error);
      }
    }
    useEffect(() => {
        fetchModules();
      }, []);

      return (
        <div className="container module_page">
            <h2 className="text-center">
                Module Table
            </h2>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Topic</th>
                        <th>Subtopic</th>
                        <th>Difficulty</th>
                        <th>Created By</th>
                        <th>Peer Reviewed</th>
                    </tr>
                </thead>
                <tbody className="table-group-divider module-body">
                    {modules.map((module) => (
                        <ModuleItem key={module.id} module={module} />
                    ))}
                </tbody>
            </table>
        </div>
      )
    }
export default ModuleTable;