import React from "react";
type ModalProps = {
  show: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
};

const Modal: React.FC<ModalProps> = ({ show, onClose, children, title }) => {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      // Modal Container
      <div className="bg-white rounded-lg shadow-lg w-full max-w-xl max-h-[90vh] flex flex-col">
        {/* Modal Header */}
        <div className="p-4 border-b">
          <h2 className="text-xl font-semibold">{title}</h2>
        </div>
        {/* Modal Content */}
        <div className="p-4 overflow-y-auto">{children}</div>
        <div className="p-4 border-t sticky bottom-0 bg-white z-10">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-blue-500 text-white rounded"
          >
            Exit
          </button>
        </div>
      </div>
    </div>
  );
};

export default Modal;
