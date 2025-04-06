import type { ModuleSimple } from "~/types/types";
import { Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

interface ModuleTableProps {
  modules: ModuleSimple[];
}

const ModuleTable: React.FC<ModuleTableProps> = ({ modules }) => {
  const navigate = useNavigate();

  if (modules.length === 0) return <p>No modules found.</p>;

  const col_keys: (keyof ModuleSimple)[] = ["id", "name"];
  const col_labels: Record<keyof ModuleSimple, string> = {
    id: "Module ID",
    name: "Module Name",
  };

  const handleClick = (module_id: number) => {
    navigate("/modules/");
  };

  function renderColumns(modules: ModuleSimple[]) {
    return col_keys.map((col) => <th key={col}>{col_labels[col] ?? col}</th>);
  }

  function renderModules(modules: ModuleSimple[]) {
    return modules.map((mod) => (
      <tr key={mod.id}>
        {col_keys.map((col) => (
          <td key={col}>
            <Link to={`${mod.id}`}>{mod[col]}</Link>
          </td>
        ))}
      </tr>
    ));
  }

  return (
    <Table striped bordered hover>
      <thead>
        <tr>{renderColumns(modules)}</tr>
      </thead>
      <tbody>{renderModules(modules)}</tbody>
    </Table>
  );
};

export default ModuleTable;
