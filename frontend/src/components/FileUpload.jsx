import React, { useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { runAIAnalysisOnFile } from "../store/complaintSlice";

export default function FileUpload() {
  const dispatch = useDispatch();
  const analyzing = useSelector((s) => s.complaint.analyzing);
  const inputRef = useRef();

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) {
      dispatch(runAIAnalysisOnFile(file));
    }
  };

  return (
    <div className="panel">
      <h2>Upload Complaint Document</h2>
      <div className="upload-box" onClick={() => inputRef.current.click()}>
        <div className="upload-icon">⌘</div>
        <p>Click to upload a PDF, email, or scanned image</p>
        <p className="upload-hint">AI Copilot will extract complaint details automatically</p>
        <input
          type="file"
          ref={inputRef}
          style={{ display: "none" }}
          accept=".pdf,.txt,.eml,.png,.jpg,.jpeg"
          onChange={handleFile}
        />
      </div>
      {analyzing && <p className="loading-text">AI Copilot analyzing document</p>}
    </div>
  );
}