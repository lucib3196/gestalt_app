import React from "react";
import Modal from "@/components/MyModals";
import { useEffect, useState } from "react";
import "@/styles/MyModals.css";
export default function CodeEditorSettings() {
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <button onClick={() => setShowModal(true)}>Open Settings</button>
      <Modal show={showModal} onClose={() => setShowModal(false)}>
        <div className="modal-header">
          <h1>Code Editor Settings</h1>
        </div>
      </Modal>
    </>
  );
}
