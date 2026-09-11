import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchComplaints } from "../store/complaintSlice";

const riskClass = (level) => {
  if (level === "Critical") return "critical";
  if (level === "Major") return "major";
  return "minor";
};

export default function ComplaintList() {
  const dispatch = useDispatch();
  const complaints = useSelector((s) => s.complaint.complaints);

  useEffect(() => {
    dispatch(fetchComplaints());
  }, [dispatch]);

  return (
    <div className="panel">
      <h2>Recent Complaints ({complaints.length})</h2>
      {complaints.length === 0 && (
        <p className="empty-state">No complaints logged yet — upload a document above to begin.</p>
      )}
      {complaints.map((c) => (
        <div className="complaint-row" key={c.id}>
          <span className="complaint-meta">
            #{c.id} — {c.product_name}
            <span className="batch">Batch {c.batch_number}</span>
          </span>
          {c.risk_level && (
            <div className={`risk-indicator ${riskClass(c.risk_level)}`} style={{ padding: "2px 0 2px 10px" }}>
              <span className="risk-label" style={{ fontSize: 13 }}>{c.risk_level}</span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}