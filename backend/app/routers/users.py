import time
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    clean_roll = user_data.rollNumber.strip().upper() # Forces uppercase instantly
    
    if not clean_roll:
        raise HTTPException(status_code=400, detail="Roll number cannot be empty.")
    
    existing_user = db.query(models.User).filter(models.User.rollNumber == clean_roll).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    new_user = models.User(
        name=user_data.name,
        rollNumber=clean_roll,
        team=user_data.team or "",
        password=user_data.password, # Save the password
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/admin-create-student", response_model=schemas.UserResponse)
def admin_create_student(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    clean_roll = user_data.rollNumber.strip().upper()
    
    if not clean_roll:
        raise HTTPException(status_code=400, detail="Roll number cannot be empty.")
    
    existing_user = db.query(models.User).filter(models.User.rollNumber == clean_roll).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Roll number already registered")
        
    new_user = models.User(
        name=user_data.name,
        rollNumber=clean_roll,
        team=user_data.team or "",
        password=user_data.password,
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=schemas.UserResponse)
def login_user(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    clean_roll = credentials.rollNumber.strip().upper() # Case-insensitive check
    
    user = db.query(models.User).filter(models.User.rollNumber == clean_roll).first()
    
    # Check if user exists AND if the password matches
    valid_pass = user and (user.password == credentials.password)
    if not user or not valid_pass:
        raise HTTPException(status_code=401, detail="Invalid roll number or password.")
        
    return user

@router.post("", response_model=schemas.UserResponse)
@router.post("/", response_model=schemas.UserResponse)
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """Admin creates a new user account with full profile details."""
    clean_email = user_data.email.strip().lower() if user_data.email else None
    clean_roll = user_data.rollNumber.strip().upper() if user_data.rollNumber else None
    
    if clean_email:
        existing_email = db.query(models.User).filter(models.User.email == clean_email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="A user with this email already exists.")
            
    if clean_roll:
        existing_roll = db.query(models.User).filter(models.User.rollNumber == clean_roll).first()
        if existing_roll:
            raise HTTPException(status_code=400, detail="A user with this Employee ID / Roll Number already exists.")
            
    pos_title = user_data.positionTitle
    if not pos_title and user_data.role:
        pos_title = user_data.role.replace('_', ' ').title()
        
    now_ms = int(time.time() * 1000)
    new_user = models.User(
        name=user_data.name.strip(),
        email=clean_email,
        rollNumber=clean_roll,
        team=user_data.team or "",
        role=user_data.role or "intern",
        positionTitle=pos_title or "",
        accountStatus=user_data.accountStatus or "ACTIVE",
        password=user_data.password or os.getenv("DEFAULT_USER_PASSWORD", "Fixly@2026"),
        createdAt=now_ms
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("", response_model=List[schemas.UserResponse])
@router.get("/", response_model=List[schemas.UserResponse])
@router.get("/all", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.id.desc()).all()

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Admin updates user profile details, role, department, status, and credentials."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.name is not None and user_update.name.strip():
        db_user.name = user_update.name.strip()
        
    if user_update.email is not None:
        clean_email = user_update.email.strip().lower() if user_update.email else None
        if clean_email and clean_email != (db_user.email or "").lower():
            existing = db.query(models.User).filter(models.User.email == clean_email, models.User.id != user_id).first()
            if existing:
                raise HTTPException(status_code=400, detail="Another user with this email already exists.")
        db_user.email = clean_email
        
    if user_update.rollNumber is not None:
        clean_roll = user_update.rollNumber.strip().upper() if user_update.rollNumber else None
        if clean_roll and clean_roll != (db_user.rollNumber or "").upper():
            existing = db.query(models.User).filter(models.User.rollNumber == clean_roll, models.User.id != user_id).first()
            if existing:
                raise HTTPException(status_code=400, detail="Another user with this Employee ID / Roll Number already exists.")
        db_user.rollNumber = clean_roll
        
    if user_update.team is not None:
        db_user.team = user_update.team
        
    if user_update.role is not None:
        db_user.role = user_update.role
        
    if user_update.positionTitle is not None:
        db_user.positionTitle = user_update.positionTitle
        
    if user_update.accountStatus is not None:
        db_user.accountStatus = user_update.accountStatus
        
    if user_update.password is not None and user_update.password.strip():
        db_user.password = user_update.password.strip()

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Safely unassign user from active tasks
    db.query(models.Task).filter(models.Task.assignedToId == user_id).update({
        models.Task.assignedToId: None,
        models.Task.assignedToName: None
    })
    # Safely unassign user from stories
    db.query(models.Story).filter(models.Story.assignedToId == user_id).update({
        models.Story.assignedToId: None,
        models.Story.assignedToName: None
    })
    # Remove notifications
    db.query(models.Notification).filter(models.Notification.recipientId == user_id).delete()
    
    # If this user was a team lead, clear lead_id on team
    db.query(models.Team).filter(models.Team.lead_id == user_id).update({
        models.Team.lead_id: None,
        models.Team.lead_name: ""
    })
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully", "id": user_id}

@router.post("/admin-login")
def admin_login(credentials: schemas.AdminLogin):
    """Secure login for the workspace administrator and viewers"""
    
    admin_pass = os.getenv("ADMIN_PASSWORD")
    viewer_pass = os.getenv("VIEWER_PASSWORD")
    
    # 1. Full Admin Login
    if credentials.username.lower() == "admin" and admin_pass and credentials.password == admin_pass:
        return {
            "id": 0,
            "name": "Administrator",
            "rollNumber": "ADMIN",
            "team": "Management",
            "role": "admin",
            "createdAt": int(time.time() * 1000)
        }
        
    # 2. View-Only Executive Login
    elif credentials.username.lower() == "viewer" and viewer_pass and credentials.password == viewer_pass:
        return {
            "id": -1,
            "name": "Executive",
            "rollNumber": "VIEWER",
            "team": "Management",
            "role": "viewer",
            "createdAt": int(time.time() * 1000)
        }
    
    # If the password is wrong for both, kick them out
    raise HTTPException(status_code=401, detail="Invalid admin or viewer credentials")