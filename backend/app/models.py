from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255))
    batch_number = Column(String(100))
    complainant_name = Column(String(255))
    complainant_email = Column(String(255))
    complaint_type = Column(String(100))          # e.g. Quality, Packaging, Adverse Event
    description = Column(Text)
    date_of_complaint = Column(String(50))

    # AI-generated fields
    risk_level = Column(String(50))                # Critical / Major / Minor
    risk_justification = Column(Text)
    root_cause = Column(Text)
    capa_recommendation = Column(Text)
    ai_summary = Column(Text)
    completeness_status = Column(String(50))       # Complete / Incomplete
    missing_fields = Column(Text)
    is_duplicate = Column(String(10))              # Yes / No
    duplicate_of_id = Column(Integer, nullable=True)

    status = Column(String(50), default="Open")
    raw_source_text = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())