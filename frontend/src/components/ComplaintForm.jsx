import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { updateFormField, saveComplaint, resetForm } from "../store/complaintSlice";

const COMPLAINT_TYPES = ["Quality Defect", "Packaging", "Adverse Event", "Delivery", "Documentation", "Other"];

export default function ComplaintForm() {
  const dispatch = useDispatch();
  const form = useSelector((s) => s.complaint.form);
  const saving = useSelector((s) => s.complaint.saving);

  const handleChange = (field) => (e) => {
    dispatch(updateFormField({ field, value: e.target.value }));
  };

  const handleSubmit = async () => {
    await dispatch(saveComplaint());
    dispatch(resetForm());
  };

  return (
    <div className="panel">
      <h2>Log Customer Complaint</h2>

      <div className="form-row">
        <div className="form-group">
          <label>Product Name</label>
          <input value={form.product_name} onChange={handleChange("product_name")} placeholder="e.g. Paracetamol 500mg" />
        </div>
        <div className="form-group">
          <label>Batch Number</label>
          <input value={form.batch_number} onChange={handleChange("batch_number")} placeholder="e.g. PCM2024-118" />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Complainant Name</label>
          <input value={form.complainant_name} onChange={handleChange("complainant_name")} />
        </div>
        <div className="form-group">
          <label>Complainant Email</label>
          <input value={form.complainant_email} onChange={handleChange("complainant_email")} />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Complaint Type</label>
          <select value={form.complaint_type} onChange={handleChange("complaint_type")}>
            <option value="">Select type</option>
            {COMPLAINT_TYPES.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Date of Complaint</label>
          <input type="date" value={form.date_of_complaint} onChange={handleChange("date_of_complaint")} />
        </div>
      </div>

      <div className="form-group">
        <label>Description</label>
        <textarea value={form.description} onChange={handleChange("description")} placeholder="Complaint details..." />
      </div>

      <button onClick={handleSubmit} disabled={saving}>
        {saving ? "Saving..." : "Save Complaint"}
      </button>
    </div>
  );
}