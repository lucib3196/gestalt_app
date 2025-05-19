// ErrorAlert.tsx
import React from "react";

type ErrorAlertProps = {
  title?: string;
  message: string;
};

export const ErrorAlert: React.FC<ErrorAlertProps> = ({
  title = "Something went wrong",
  message,
}) => (
  <div className="border border-red-600 bg-red-50 text-red-800 p-4 rounded-lg shadow-sm">
    <h3 className="font-semibold mb-1">{title}</h3>
    <p className="text-sm">{message}</p>
  </div>
);

export default ErrorAlert;
