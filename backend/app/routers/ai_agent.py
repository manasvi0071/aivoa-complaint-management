from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Complaint
from app.utils.parser import extract_text_from_file
from app.agents.graph import complaint_graph
from app.schemas import AIAnalysisResult

router = APIRouter(prefix="/ai", tags=["AI Agent"])


@router.post("/analyze-upload", response_model=AIAnalysisResult)
async def analyze_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    raw_text = extract_text_from_file(file.filename, file_bytes)

    existing = db.query(Complaint).order_by(Complaint.id.desc()).limit(50).all()
    existing_dicts = [
        {
            "id": c.id,
            "product_name": c.product_name,
            "batch_number": c.batch_number,
            "description": c.description,
        }
        for c in existing
    ]

    result_state = complaint_graph.invoke({
        "raw_text": raw_text,
        "existing_complaints": existing_dicts,
    })

    return AIAnalysisResult(
        extracted=result_state.get("extracted", {}),
        risk_level=result_state.get("risk_level", "Minor"),
        risk_justification=result_state.get("risk_justification", ""),
        root_cause=result_state.get("root_cause", ""),
        capa_recommendation=result_state.get("capa_recommendation", ""),
        ai_summary=result_state.get("ai_summary", ""),
        completeness_status=result_state.get("completeness_status", "Incomplete"),
        missing_fields=result_state.get("missing_fields", []),
        is_duplicate=result_state.get("is_duplicate", False),
        duplicate_of_id=result_state.get("duplicate_of_id"),
    )


@router.post("/analyze-text", response_model=AIAnalysisResult)
async def analyze_text(text: str, db: Session = Depends(get_db)):
    existing = db.query(Complaint).order_by(Complaint.id.desc()).limit(50).all()
    existing_dicts = [
        {
            "id": c.id,
            "product_name": c.product_name,
            "batch_number": c.batch_number,
            "description": c.description,
        }
        for c in existing
    ]

    result_state = complaint_graph.invoke({
        "raw_text": text,
        "existing_complaints": existing_dicts,
    })

    return AIAnalysisResult(
        extracted=result_state.get("extracted", {}),
        risk_level=result_state.get("risk_level", "Minor"),
        risk_justification=result_state.get("risk_justification", ""),
        root_cause=result_state.get("root_cause", ""),
        capa_recommendation=result_state.get("capa_recommendation", ""),
        ai_summary=result_state.get("ai_summary", ""),
        completeness_status=result_state.get("completeness_status", "Incomplete"),
        missing_fields=result_state.get("missing_fields", []),
        is_duplicate=result_state.get("is_duplicate", False),
        duplicate_of_id=result_state.get("duplicate_of_id"),
    )