import { clsx } from "clsx";

type ClickHandler = React.MouseEventHandler;

export type TableCell = {
  value: any;
  onClick?: ClickHandler;
  className?: string;
};

export type TableHeader = {
  label: string;
  className?: string;
};

export type TableProps = {
  caption?: string;
  header: TableHeader[];
  data: TableCell[][];
};

const Table: React.FC<TableProps> = ({ caption, header, data }) => {
  const handleCaption = () => {
    if (caption) {
      return <caption className="caption-top">{caption}</caption>;
    } else return;
  };
  const handleHeader = () => {
    return (
      <thead>
        <tr>
          {header.map((col, index) => (
            <th
              key={index}
              className={clsx(
                "border border-gray-300 px-4 py-2 text-left font-medium",
                col.className
              )}
            >
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
    );
  };

  const handleBody = () => {
    return (
      <tbody>
        {data.map((row, r) => (
          <tr key={r} className={r % 2 ? "bg-gray-50" : undefined}>
            {row.map((cell, c) => (
              <td
                key={c}
                className={clsx(
                  "border border-gray-300 px-4 py-2",
                  cell.className
                )}
                onClick={cell.onClick}
              >
                {cell.value}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    );
  };

  return (
    <div className={clsx("relative overflow-x-auto ")}>
      <table
        className={clsx(
          "w-full table-auto",
          "border border-gray-400 border-spacing-2"
        )}
      >
        {handleCaption()}
        {handleHeader()}
        {handleBody()}
      </table>
    </div>
  );
};

export default Table;
