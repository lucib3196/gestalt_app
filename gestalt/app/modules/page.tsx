"use client";

import React from "react";
import { DataRenderer } from "@/components/DataRenderer";
import Table from "react-bootstrap/Table";
import { Container } from "react-bootstrap";
import { useRouter } from 'next/navigation'

type Module = {
  id: number;
  name: string;
};

const RenderModuleTable = (router: ReturnType<typeof useRouter>) => {
  const table_cols = ["#", "Title"];
  return (modules: Module[], isLoading: boolean) => (
    <Table striped bordered hover responsive>
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
            <td>
              <button
                className="btn btn-link p-0"
                onClick={() => router?.push(`/modules/${module.id}`)}
              >
                {module.name}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

const ModuleList: React.FC = () => {
  const router = useRouter();

  const source = {
    url: "/modules/simple",
  };

  const loadingComponent: React.ReactNode = (
    <div className="text-center p-4">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
    </div>
  );

  const errorComponent: React.ReactNode = (
    <div className="alert alert-danger">Error loading modules</div>
  );

  return (
    <Container fluid className="my-container">
      <h2 className="list-group text-center">Module Table</h2>
      <DataRenderer
        source={source}
        loadingComponent={loadingComponent}
        errorComponent={errorComponent}
      >
        {RenderModuleTable(router)}
      </DataRenderer>
    </Container>
  );
};

export default ModuleList;
