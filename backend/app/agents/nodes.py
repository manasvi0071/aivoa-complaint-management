import json
import re
from typing import TypedDict, Optional, List
from app.agents.llm import fast_llm, reasoning_llm


class ComplaintState(TypedDict, total=False):
    raw_text: str
    extracted: dict
    completeness_status: str
    missing_fields: List[str]
    risk_level: str
    risk_justification: str
    root_cause: str
    capa_recommendation: str
    ai_summary: str
    is_duplicate: bool
    duplicate_of_id: Optional[int]
    existing_complaints: List[dict]   # passed in from the DB for dup check


def _safe_json_parse(raw: str) -> dict:
    """Strip markdown fences and parse JSON safely."""
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(cleaned)
    except Exception:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                return {}
        return {}


# --- Node 1: Field Extraction ---
def extract_fields_node(state: ComplaintState) -> ComplaintState:
    prompt = f"""You are a pharmaceutical QMS assistant. Extract the following fields from this
customer complaint text. Respond ONLY with valid JSON, no preamble, no markdown.

Fields: product_name, batch_number, complainant_name, complainant_email,
complaint_type (one of: Quality Defect, Packaging, Adverse Event, Delivery, Documentation, Other),
description (concise summary of the issue), date_of_complaint (if mentioned, else empty string).

Complaint text:
\"\"\"{state['raw_text']}\"\"\"

JSON:"""
    response = fast_llm.invoke(prompt)
    extracted = _safe_json_parse(response.content)
    state["extracted"] = extracted
    return state


# --- Node 2: Completeness Checker ---
def completeness_check_node(state: ComplaintState) -> ComplaintState:
    required = ["product_name", "batch_number", "complainant_name", "description"]
    extracted = state.get("extracted", {})
    missing = [f for f in required if not extracted.get(f)]

    state["missing_fields"] = missing
    state["completeness_status"] = "Complete" if not missing else "Incomplete"
    return state


# --- Node 3: Duplicate Detection ---
def duplicate_check_node(state: ComplaintState) -> ComplaintState:
    extracted = state.get("extracted", {})
    existing = state.get("existing_complaints", [])

    if not existing:
        state["is_duplicate"] = False
        state["duplicate_of_id"] = None
        return state

    existing_summary = "\n".join(
        f"ID {c['id']}: product={c.get('product_name')}, batch={c.get('batch_number')}, "
        f"desc={c.get('description', '')[:200]}"
        for c in existing
    )

    prompt = f"""You are checking for duplicate pharmaceutical complaints.

New complaint: product={extracted.get('product_name')}, batch={extracted.get('batch_number')},
description={extracted.get('description')}

Existing complaints:
{existing_summary}

Is the new complaint a duplicate of any existing one (same product, batch, and issue)?
Respond ONLY with JSON: {{"is_duplicate": true/false, "duplicate_of_id": <id or null>}}"""

    response = fast_llm.invoke(prompt)
    result = _safe_json_parse(response.content)
    state["is_duplicate"] = result.get("is_duplicate", False)
    state["duplicate_of_id"] = result.get("duplicate_of_id")
    return state


# --- Node 4: Risk Classification ---
def risk_classification_node(state: ComplaintState) -> ComplaintState:
    extracted = state.get("extracted", {})
    prompt = f"""You are a pharmaceutical QMS risk assessor (API/FDF manufacturing context).
Classify this complaint's risk level based on patient safety impact, regulatory impact,
and product quality impact.

Complaint: {json.dumps(extracted)}

Respond ONLY with JSON:
{{"risk_level": "Critical" | "Major" | "Minor", "risk_justification": "<2-3 sentence justification>"}}

Guidance:
- Critical: adverse events, potential patient harm, sterility/contamination issues
- Major: quality defect affecting product efficacy but no immediate harm
- Minor: packaging, labeling, delivery, documentation issues"""

    response = fast_llm.invoke(prompt)
    result = _safe_json_parse(response.content)
    state["risk_level"] = result.get("risk_level", "Minor")
    state["risk_justification"] = result.get("risk_justification", "")
    return state


# --- Node 5: Root Cause + CAPA Recommendation ---
def root_cause_capa_node(state: ComplaintState) -> ComplaintState:
    extracted = state.get("extracted", {})
    prompt = f"""You are a pharmaceutical QMS expert. For the complaint below, suggest a likely
root cause and a CAPA (Corrective and Preventive Action) recommendation, following standard
API/FDF manufacturing QMS practices.

Complaint: {json.dumps(extracted)}
Risk level: {state.get('risk_level')}

Respond ONLY with JSON:
{{"root_cause": "<likely root cause, 2-3 sentences>", "capa_recommendation": "<concrete CAPA steps, 3-4 sentences>"}}"""

    response = reasoning_llm.invoke(prompt)
    result = _safe_json_parse(response.content)
    state["root_cause"] = result.get("root_cause", "")
    state["capa_recommendation"] = result.get("capa_recommendation", "")
    return state


# --- Node 6: Summary ---
def summary_node(state: ComplaintState) -> ComplaintState:
    extracted = state.get("extracted", {})
    prompt = f"""Summarize this pharmaceutical complaint in 2-3 sentences for a QMS dashboard.
Complaint: {json.dumps(extracted)}
Risk: {state.get('risk_level')}

Respond with plain text only, no JSON, no preamble."""

    response = fast_llm.invoke(prompt)
    state["ai_summary"] = response.content.strip()
    return state