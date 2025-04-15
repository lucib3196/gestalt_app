import React from "react";

type LoadingComponentProps = {
  message?: string;
};

const LoadingComponent: React.FC<LoadingComponentProps> = ({
  message = "Loading...",
}) => {
  return (
    <div className="text-center p4">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">{message}</span>
      </div>
    </div>
  );
};
export default LoadingComponent;
