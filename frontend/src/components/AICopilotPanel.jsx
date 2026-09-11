import React from "react";
import { useSelector } from "react-redux";

const riskClass = (level) => {
  if (level === "Critical") return "critical";
  if (level === "Major") return "major";
  return "minor";
};

export default function AICopilotPanel() {
  const ai = useSelector((s) => s.complaint.ai);

  if (!ai.risk_level) {
    return (
      <div className="panel">
        <h2>AI Copilot — Risk Assessment</h2>
        <p className="copilot-empty">
          Upload a complaint document to see AI-generated risk analysis, root
          cause, and CAPA recommendations here.
        </p>
      </div>
    );
  }

  return (
    <div className="panel">
      <h2>AI Copilot — Risk Assessment</h2>

      <div className="ai-block">
        <h4>Risk Level</h4>
        <div className={`risk-indicator ${riskClass(ai.risk_level)}`}>
          <span className="risk-label">{ai.risk_level}</span>
        </div>
        <p style={{ marginTop: 10 }}>{ai.risk_justification}</p>
      </div>

      <div className="ai-block">
        <h4>Completeness</h4>
        <span className={`status-tag ${ai.completeness_status === "Complete" ? "complete" : "incomplete"}`}>
          {ai.completeness_status}
        </span>
        {ai.missing_fields?.length > 0 && (
          <p style={{ marginTop: 8, fontSize: 13, color: "#A8433A" }}>
            Missing: {ai.missing_fields.join(", ")}
          </p>
        )}
      </div>

      <div className="ai-block">
        <h4>Duplicate Check</h4>
        {ai.is_duplicate ? (
          <div className="duplicate-flag">Possible duplicate of complaint #{ai.duplicate_of_id}</div>
        ) : (
          <div className="duplicate-clear">No duplicate found</div>
        )}
      </div>

      <div className="ai-block">
        <h4>Root Cause (AI Suggested)</h4>
        <p>{ai.root_cause}</p>
      </div>

      <div className="ai-block">
        <h4>CAPA Recommendation</h4>
        <p>{ai.capa_recommendation}</p>
      </div>

      <div className="ai-block">
        <h4>AI Summary</h4>
        <p>{ai.ai_summary}</p>
      </div>
    </div>
  );
}