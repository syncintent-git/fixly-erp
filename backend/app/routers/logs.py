import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/logs", tags=["Logs"])

def serialize_log(log: models.Log) -> dict:
    return {
        "id": log.id,
        "userId": log.userId,
        "user_id": log.userId,
        "name": log.name,
        "rollNumber": log.rollNumber or "",
        "team": log.team or "",
        "hours": log.hours or [],
        "todayLog": log.todayLog or "",
        "workDone": log.todayLog or "",
        "tomorrowGoal": log.tomorrowGoal or "",
        "nextDayGoal": log.tomorrowGoal or "",
        "attendanceMode": log.attendanceMode or "office",
        "date": log.date,
        "timestamp": log.timestamp,
        "suggestionType": log.suggestionType,
        "suggestionDescription": log.suggestionDescription,
        "suggestionDeadline": log.suggestionDeadline,
        "suggestionStatus": log.suggestionStatus or "Pending"
    }

@router.get("", response_model=List[schemas.LogResponse])
@router.get("/", response_model=List[schemas.LogResponse])
@router.get("/all", response_model=List[schemas.LogResponse])
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(models.Log).order_by(models.Log.timestamp.desc()).all()
    return [schemas.LogResponse(**serialize_log(l)) for l in logs]

@router.post("", response_model=schemas.LogResponse)
@router.post("/", response_model=schemas.LogResponse)
@router.post("/submit", response_model=schemas.LogResponse)
def create_log(log: schemas.LogCreate, db: Session = Depends(get_db)):
    user_id_val = log.userId if log.userId is not None else log.user_id
    if user_id_val is None:
        user_id_val = 0

    today_val = log.todayLog or log.workDone or ""
    tomorrow_val = log.tomorrowGoal or log.nextDayGoal or ""
    att_mode_val = log.attendanceMode or "office"

    # Check if a log already exists for this user and date; update if exists, otherwise create
    existing_log = None
    if user_id_val and log.date:
        existing_log = db.query(models.Log).filter(
            models.Log.userId == user_id_val,
            models.Log.date == log.date
        ).first()

    if existing_log:
        existing_log.todayLog = today_val
        existing_log.tomorrowGoal = tomorrow_val
        existing_log.attendanceMode = att_mode_val
        existing_log.hours = log.hours or existing_log.hours or []
        if log.team:
            existing_log.team = log.team
        if log.suggestionDescription:
            existing_log.suggestionType = log.suggestionType
            existing_log.suggestionDescription = log.suggestionDescription
            existing_log.suggestionDeadline = log.suggestionDeadline
            existing_log.suggestionStatus = log.suggestionStatus or existing_log.suggestionStatus or "Pending"
        db.commit()
        db.refresh(existing_log)
        return schemas.LogResponse(**serialize_log(existing_log))

    new_log = models.Log(
        userId=user_id_val,
        name=log.name,
        rollNumber=log.rollNumber or "",
        team=log.team or "",
        hours=log.hours or [],
        todayLog=today_val,
        tomorrowGoal=tomorrow_val,
        attendanceMode=att_mode_val,
        date=log.date,
        timestamp=int(time.time() * 1000),
        suggestionType=log.suggestionType,
        suggestionDescription=log.suggestionDescription,
        suggestionDeadline=log.suggestionDeadline,
        suggestionStatus=log.suggestionStatus or "Pending"
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    
    return schemas.LogResponse(**serialize_log(new_log))

@router.put("/{log_id}", response_model=schemas.LogResponse)
@router.put("/update/{log_id}", response_model=schemas.LogResponse)
def update_log(log_id: int, log_update: schemas.LogUpdate, db: Session = Depends(get_db)):
    """Update an existing log for a previous date"""
    db_log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    if log_update.hours is not None:
        db_log.hours = log_update.hours
    if log_update.todayLog or log_update.workDone:
        db_log.todayLog = log_update.todayLog or log_update.workDone
    if log_update.tomorrowGoal or log_update.nextDayGoal:
        db_log.tomorrowGoal = log_update.tomorrowGoal or log_update.nextDayGoal
    if log_update.attendanceMode:
        db_log.attendanceMode = log_update.attendanceMode
    if log_update.team:
        db_log.team = log_update.team
    if log_update.suggestionDescription:
        db_log.suggestionType = log_update.suggestionType
        db_log.suggestionDescription = log_update.suggestionDescription
        db_log.suggestionDeadline = log_update.suggestionDeadline
    
    db.commit()
    db.refresh(db_log)
    return schemas.LogResponse(**serialize_log(db_log))

@router.patch("/{log_id}/suggestion-status", response_model=schemas.LogResponse)
def update_suggestion_status(log_id: int, status_update: schemas.SuggestionStatusUpdate, db: Session = Depends(get_db)):
    """Update the status of a suggestion/feature request"""
    db_log = db.query(models.Log).filter(models.Log.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db_log.suggestionStatus = status_update.status
    db.commit()
    db.refresh(db_log)
    return schemas.LogResponse(**serialize_log(db_log))