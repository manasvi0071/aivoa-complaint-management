from pydantic import BaseModel
from typing import Optional


class ComplaintBase(BaseModel):
    product_name: Optional[str] = None
    batch_number: Optional[str] = None
    complainant_name: Optional[str] = None
    complainant_email: Optional[str] = None
    complaint_type: Optional[str] = None
    description: Optional[str] = None
    date_of_complaint: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    risk_level: Optional[str] = None
    risk_justification: Optional[str] = None
    root_cause: Optional[str] = None
    capa_recommendation: Optional[str] = None
    ai_summary: Optional[str] = None
    completeness_status: Optional[str] = None
    missing_fields: Optional[str] = None
    is_duplicate: Optional[str] = None
    duplicate_of_id: Optional[int] = None


class ComplaintOut(ComplaintCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


class AIAnalysisResult(BaseModel):
    extracted: ComplaintBase
    risk_level: str
    risk_justification: str
    root_cause: str
    capa_recommendation: str
    ai_summary: str
    completeness_status: str
    missing_fields: list[str]
    is_duplicate: bool
    duplicate_of_id: Optional[int] = None