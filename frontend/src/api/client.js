import axios from "axios";

const API_BASE = "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE,
});

export const analyzeUpload = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return apiClient.post("/ai/analyze-upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const analyzeText = (text) =>
  apiClient.post(`/ai/analyze-text?text=${encodeURIComponent(text)}`);

export const createComplaint = (payload) =>
  apiClient.post("/complaints/", payload);

export const listComplaints = () => apiClient.get("/complaints/");