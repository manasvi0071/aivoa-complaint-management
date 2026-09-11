import React from "react";
import FileUpload from "./components/FileUpload";
import ComplaintForm from "./components/ComplaintForm";
import AICopilotPanel from "./components/AICopilotPanel";
import ComplaintList from "./components/ComplaintList";

export default function App() {
  return (
    <div className="shell">
      <div className="masthead">
        <div>
          <div className="brand">AIVOA <span>Complaints</span></div>
          <div className="subtitle">Customer Complaint Management — API &amp; FDF Manufacturing</div>
        </div>
        <div className="module-label">QMS Module</div>
      </div>

      <FileUpload />

      <div className="grid">
        <div>
          <ComplaintForm />
          <ComplaintList />
        </div>
        <div>
          <AICopilotPanel />
        </div>
      </div>
    </div>
  );
}