import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas
from typing import List, Optional

router = APIRouter(prefix="/api/teams", tags=["Teams"])

def team_to_response(team: models.Team, db: Session) -> dict:
    count = db.query(models.User).filter(models.User.team == team.name).count()
    return {
        "id": team.id,
        "name": team.name,
        "description": team.description or "",
        "leadId": team.lead_id,
        "leadName": team.lead_name or "",
        "isLeadership": bool(getattr(team, "is_leadership", False)),
        "memberCount": count
    }

@router.get("", response_model=List[schemas.TeamResponse])
@router.get("/", response_model=List[schemas.TeamResponse])
def get_teams(
    include_leadership: Optional[bool] = None,
    for_onboarding: bool = False,
    user_role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Fetches teams. Hides leadership teams from interns and public onboarding."""
    query = db.query(models.Team)
    
    # Hide leadership teams for onboarding or intern roles
    is_intern_role = user_role and user_role.lower() in [
        "frontend_developer", "backend_developer", "devops_developer", "intern", "student", "user"
    ]
    if for_onboarding or include_leadership is False or is_intern_role:
        query = query.filter(models.Team.is_leadership == False)
        
    teams = query.order_by(models.Team.is_leadership.asc(), models.Team.name.asc()).all()
    return [team_to_response(t, db) for t in teams]

@router.get("/{team_id}")
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Fetches a specific team along with assigned member users."""
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    members = db.query(models.User).filter(models.User.team == team.name).all()
    res = team_to_response(team, db)
    res["members"] = [schemas.UserResponse.model_validate(m) for m in members]
    return res

def verify_team_editor(user_id: Optional[int], db: Session):
    """Verifies that the user has permission to modify teams (Leadership except view-only)."""
    if not user_id:
        return  # Allow if no user_id context passed (e.g. initial setup), checked on frontend
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not recognized.")
    role = (user.role or "").lower()
    # View-only roles cannot edit
    if role in ["cdc", "mentor", "viewer", "cfo", "cmo"]:
        raise HTTPException(status_code=403, detail="View-only reviewers cannot create or modify teams.")
    # Must be leadership/admin
    if role not in ["admin", "ceo", "cto", "coo"]:
        raise HTTPException(status_code=403, detail="Only leadership administrators can manage teams.")

@router.post("", response_model=schemas.TeamResponse)
@router.post("/", response_model=schemas.TeamResponse)
def create_team(team_data: schemas.TeamCreate, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Creates a new team / department."""
    verify_team_editor(user_id, db)
    cleaned_name = team_data.name.strip()
    if not cleaned_name:
        raise HTTPException(status_code=400, detail="Team name cannot be empty")
        
    existing = db.query(models.Team).filter(models.Team.name.ilike(cleaned_name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="A team with this name already exists")
    
    lead_name = team_data.leadName or ""
    if team_data.leadId and not lead_name:
        lead_user = db.query(models.User).filter(models.User.id == team_data.leadId).first()
        if lead_user:
            lead_name = lead_user.name

    new_team = models.Team(
        name=cleaned_name,
        description=team_data.description or "",
        lead_id=team_data.leadId,
        lead_name=lead_name,
        is_leadership=bool(team_data.isLeadership),
        createdAt=int(time.time() * 1000)
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    return team_to_response(new_team, db)

@router.put("/{team_id}", response_model=schemas.TeamResponse)
def update_team(team_id: int, team_update: schemas.TeamUpdate, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Updates team details, and cascades name changes to all assigned users."""
    verify_team_editor(user_id, db)
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    old_name = db_team.name

    if team_update.name is not None and team_update.name.strip():
        new_name = team_update.name.strip()
        if new_name.lower() != old_name.lower():
            existing = db.query(models.Team).filter(models.Team.name.ilike(new_name), models.Team.id != team_id).first()
            if existing:
                raise HTTPException(status_code=400, detail="Another team with this name already exists")
            
            # Cascade rename to all users assigned to this team
            db.query(models.User).filter(models.User.team == old_name).update({models.User.team: new_name})
            db_team.name = new_name

    if team_update.description is not None:
        db_team.description = team_update.description

    if team_update.isLeadership is not None:
        db_team.is_leadership = team_update.isLeadership

    if team_update.leadId is not None:
        db_team.lead_id = team_update.leadId
        lead_user = db.query(models.User).filter(models.User.id == team_update.leadId).first()
        db_team.lead_name = lead_user.name if lead_user else ""
    elif team_update.leadName is not None:
        db_team.lead_name = team_update.leadName

    db.commit()
    db.refresh(db_team)
    return team_to_response(db_team, db)

@router.delete("/{team_id}")
def delete_team(team_id: int, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Deletes a team and sets all assigned users to unassigned."""
    verify_team_editor(user_id, db)
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # 1. Update all users assigned to this team to be unassigned ("")
    db.query(models.User).filter(models.User.team == db_team.name).update({models.User.team: ""})
    
    team_name = db_team.name
    db.delete(db_team)
    db.commit()
    return {"message": f"Team '{team_name}' deleted successfully", "id": team_id}


