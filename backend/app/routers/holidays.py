# backend/app/routers/holidays.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/holidays", tags=["Holidays"])

@router.get("", response_model=List[schemas.HolidayResponse])
@router.get("/", response_model=List[schemas.HolidayResponse])
@router.get("/all", response_model=List[schemas.HolidayResponse])
def get_holidays(db: Session = Depends(get_db)):
    """Fetch all declared holidays"""
    return db.query(models.Holiday).order_by(models.Holiday.date.desc()).all()

@router.post("", response_model=schemas.HolidayResponse)
@router.post("/", response_model=schemas.HolidayResponse)
@router.post("/create", response_model=schemas.HolidayResponse)
def create_holiday(holiday: schemas.HolidayCreate, db: Session = Depends(get_db)):
    """Declare a new holiday"""
    existing = db.query(models.Holiday).filter(models.Holiday.date == holiday.date).first()
    if existing:
        raise HTTPException(status_code=400, detail="A holiday is already declared on this date.")
    
    new_holiday = models.Holiday(date=holiday.date, name=holiday.name)
    db.add(new_holiday)
    db.commit()
    db.refresh(new_holiday)
    return new_holiday

@router.delete("/{holiday_id}")
@router.delete("/delete/{holiday_id}")
def delete_holiday(holiday_id: int, db: Session = Depends(get_db)):
    """Delete a holiday"""
    db_holiday = db.query(models.Holiday).filter(models.Holiday.id == holiday_id).first()
    if not db_holiday:
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    db.delete(db_holiday)
    db.commit()
    return {"message": "Holiday removed successfully"}