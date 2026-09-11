import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { analyzeUpload, analyzeText, createComplaint, listComplaints } from "../api/client";

const emptyForm = {
  product_name: "",
  batch_number: "",
  complainant_name: "",
  complainant_email: "",
  complaint_type: "",
  description: "",
  date_of_complaint: "",
};

export const runAIAnalysisOnFile = createAsyncThunk(
  "complaint/runAIAnalysisOnFile",
  async (file) => {
    const res = await analyzeUpload(file);
    return res.data;
  }
);

export const runAIAnalysisOnText = createAsyncThunk(
  "complaint/runAIAnalysisOnText",
  async (text) => {
    const res = await analyzeText(text);
    return res.data;
  }
);

export const saveComplaint = createAsyncThunk(
  "complaint/saveComplaint",
  async (_, { getState }) => {
    const { form, ai } = getState().complaint;
    const payload = {
      ...form,
      risk_level: ai.risk_level,
      risk_justification: ai.risk_justification,
      root_cause: ai.root_cause,
      capa_recommendation: ai.capa_recommendation,
      ai_summary: ai.ai_summary,
      completeness_status: ai.completeness_status,
      is_duplicate: ai.is_duplicate ? "Yes" : "No",
      duplicate_of_id: ai.duplicate_of_id,
    };
    const res = await createComplaint(payload);
    return res.data;
  }
);

export const fetchComplaints = createAsyncThunk(
  "complaint/fetchComplaints",
  async () => {
    const res = await listComplaints();
    return res.data;
  }
);

const complaintSlice = createSlice({
  name: "complaint",
  initialState: {
    form: emptyForm,
    ai: {
      risk_level: null,
      risk_justification: "",
      root_cause: "",
      capa_recommendation: "",
      ai_summary: "",
      completeness_status: null,
      missing_fields: [],
      is_duplicate: false,
      duplicate_of_id: null,
    },
    complaints: [],
    analyzing: false,
    saving: false,
    error: null,
  },
  reducers: {
    updateFormField: (state, action) => {
      const { field, value } = action.payload;
      state.form[field] = value;
    },
    resetForm: (state) => {
      state.form = emptyForm;
      state.ai = complaintSlice.getInitialState().ai;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(runAIAnalysisOnFile.pending, (state) => {
        state.analyzing = true;
        state.error = null;
      })
      .addCase(runAIAnalysisOnFile.fulfilled, (state, action) => {
        state.analyzing = false;
        applyAIResult(state, action.payload);
      })
      .addCase(runAIAnalysisOnFile.rejected, (state, action) => {
        state.analyzing = false;
        state.error = action.error.message;
      })
      .addCase(runAIAnalysisOnText.pending, (state) => {
        state.analyzing = true;
        state.error = null;
      })
      .addCase(runAIAnalysisOnText.fulfilled, (state, action) => {
        state.analyzing = false;
        applyAIResult(state, action.payload);
      })
      .addCase(runAIAnalysisOnText.rejected, (state, action) => {
        state.analyzing = false;
        state.error = action.error.message;
      })
      .addCase(saveComplaint.pending, (state) => {
        state.saving = true;
      })
      .addCase(saveComplaint.fulfilled, (state) => {
        state.saving = false;
      })
      .addCase(saveComplaint.rejected, (state, action) => {
        state.saving = false;
        state.error = action.error.message;
      })
      .addCase(fetchComplaints.fulfilled, (state, action) => {
        state.complaints = action.payload;
      });
  },
});

function applyAIResult(state, payload) {
  state.form = { ...state.form, ...payload.extracted };
  state.ai = {
    risk_level: payload.risk_level,
    risk_justification: payload.risk_justification,
    root_cause: payload.root_cause,
    capa_recommendation: payload.capa_recommendation,
    ai_summary: payload.ai_summary,
    completeness_status: payload.completeness_status,
    missing_fields: payload.missing_fields,
    is_duplicate: payload.is_duplicate,
    duplicate_of_id: payload.duplicate_of_id,
  };
}

export const { updateFormField, resetForm } = complaintSlice.actions;
export default complaintSlice.reducer;