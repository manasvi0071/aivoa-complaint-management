from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Complaint
from app.schemas import ComplaintCreate, ComplaintOut

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("/", response_model=ComplaintOut)
def create_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    missing_str = ",".join(complaint.model_dump().get("missing_fields", []) or []) \
        if hasattr(complaint, "missing_fields") else ""

    db_complaint = Complaint(
        **complaint.model_dump(exclude={"missing_fields"}, exclude_unset=True),
    )
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


@router.get("/", response_model=List[ComplaintOut])
def list_complaints(db: Session = Depends(get_db)):
    return db.query(Complaint).order_by(Complaint.id.desc()).all()


@router.get("/{complaint_id}", response_model=ComplaintOut)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    c = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return c


@router.put("/{complaint_id}", response_model=ComplaintOut)
def update_complaint(complaint_id: int, complaint: ComplaintCreate, db: Session = Depends(get_db)):
    c = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Complaint not found")
    for key, value in complaint.model_dump(exclude_unset=True).items():
        setattr(c, key, value)
    db.commit()
    db.refresh(c)
    return c