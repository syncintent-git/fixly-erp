import time
import jwt
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from supabase import create_client, Client
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/auth", tags=["Authentication & Google OAuth"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_user_permissions(user: models.User):
    role = (user.role or "").lower()
    return {
        "canAccessAdmin": role in ["admin", "ceo", "cto", "mentor", "cdc", "coo", "cfo", "cmo", "viewer"],
        "isViewOnly": role in ["cdc", "mentor", "viewer", "cfo", "cmo"],
        "canManageScrum": role in ["scrum_head", "admin", "ceo", "cto", "coo"],
        "isIntern": role in ["frontend_developer", "backend_developer", "devops_developer", "intern", "student", "user"]
    }

@router.post("/google")
def google_auth(payload: schemas.GoogleAuthRequest, db: Session = Depends(get_db)):
    """Authenticates a user via Supabase Access Token."""
    email = payload.email
    name = payload.name
    avatar_url = payload.avatarUrl

    if payload.credential:
        # Supabase access_token provided
        if not supabase:
            raise HTTPException(status_code=500, detail="Supabase client not configured on server.")
        
        try:
            # Verify token with Supabase Auth
            user_response = supabase.auth.get_user(payload.credential)
            if not user_response or not user_response.user:
                raise HTTPException(status_code=401, detail="Invalid or expired Supabase token.")
            
            sb_user = user_response.user
            email = sb_user.email
            # Extract metadata if available
            metadata = sb_user.user_metadata or {}
            name = name or metadata.get("full_name") or metadata.get("name")
            avatar_url = avatar_url or metadata.get("avatar_url") or metadata.get("picture")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Supabase credential: {e}")

    if not email:
        raise HTTPException(status_code=400, detail="Authentication did not provide an email address.")

    clean_email = email.strip().lower()

    # Check if user already exists in DB
    user = db.query(models.User).filter(models.User.email.ilike(clean_email)).first()

    # 1. User exists in database
    if user:
        if user.accountStatus == "PENDING_APPROVAL":
            return {
                "status": "PENDING_APPROVAL",
                "message": "Your registration has been submitted and is awaiting Admin approval.",
                "user": schemas.UserResponse.model_validate(user),
                "permissions": get_user_permissions(user)
            }
        elif user.accountStatus == "REJECTED":
            raise HTTPException(status_code=403, detail="Your account access request has been rejected by the administrator.")

        # Active user login
        return {
            "status": "SUCCESS",
            "message": "Login successful",
            "user": schemas.UserResponse.model_validate(user),
            "permissions": get_user_permissions(user)
        }



    # 3. Brand new user signing up via Google: Prompt for track onboarding
    return {
        "status": "ONBOARDING_REQUIRED",
        "message": "Please select your developer track to complete registration.",
        "email": clean_email,
        "name": name or clean_email.split("@")[0].title()
    }

@router.post("/onboard-role")
def onboard_intern_role(payload: schemas.OnboardRoleRequest, db: Session = Depends(get_db)):
    """Registers a new intern applicant with requested track and marks status PENDING_APPROVAL."""
    clean_email = payload.email.strip().lower()
    
    # Check if user already exists
    existing = db.query(models.User).filter(models.User.email.ilike(clean_email)).first()
    if existing:
        if existing.accountStatus == "PENDING_APPROVAL":
            return {
                "status": "PENDING_APPROVAL",
                "message": "Your registration is currently awaiting Admin approval.",
                "user": schemas.UserResponse.model_validate(existing),
                "permissions": get_user_permissions(existing)
            }
        return {
            "status": "SUCCESS",
            "message": "Account already active.",
            "user": schemas.UserResponse.model_validate(existing),
            "permissions": get_user_permissions(existing)
        }

    # Check if team is specified and valid from database
    assigned_team = ""
    if payload.team:
        db_team = db.query(models.Team).filter(models.Team.name.ilike(payload.team.strip())).first()
        if db_team:
            assigned_team = db_team.name

    # Determine position title dynamically
    role_titles = {
        "frontend_developer": "Frontend Developer Intern",
        "backend_developer": "Backend Developer Intern",
        "devops_developer": "DevOps Developer Intern",
        "intern": "Engineering Intern",
        "scrum_head": "Scrum Head"
    }
    
    clean_role = (payload.requestedRole or "intern").strip().lower()
    pos_title = role_titles.get(clean_role, clean_role.replace("_", " ").title())
    if assigned_team and "Intern" in pos_title:
        pos_title = f"{pos_title} ({assigned_team})"

    now_ms = int(time.time() * 1000)
    # Generate unique application identifier
    user_count = db.query(models.User).count()
    roll_no = f"FX-{user_count + 1001}"

    new_user = models.User(
        name=payload.name.strip(),
        email=clean_email,
        rollNumber=roll_no,
        team=assigned_team,
        role=clean_role,
        requestedRole=clean_role,
        positionTitle=pos_title,
        accountStatus="PENDING_APPROVAL", # Admin must approve before access
        createdAt=now_ms
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Add notification for Admin / CEO / CTO
    admin_users = db.query(models.User).filter(models.User.role.in_(["admin", "ceo", "cto"])).all()
    for admin in admin_users:
        db.add(models.Notification(
            recipientId=admin.id,
            senderId=new_user.id,
            senderName=new_user.name,
            title="New User Registration Approval",
            message=f"{new_user.name} ({clean_email}) requested access as {pos_title}.",
            link="/admin/access-requests",
            isRead=False,
            createdAt=now_ms
        ))
    db.commit()

    return {
        "status": "PENDING_APPROVAL",
        "message": "Your application has been received and submitted for Administrator approval. Once approved, you will have immediate access.",
        "user": schemas.UserResponse.model_validate(new_user),
        "permissions": get_user_permissions(new_user)
    }

@router.post("/demo")
def demo_login(payload: schemas.DemoAuthRequest, db: Session = Depends(get_db)):
    """Instant 1-click role switcher for evaluating each role experience."""
    user = None
    if payload.email:
        user = db.query(models.User).filter(models.User.email == payload.email).first()

    if not user:
        user = db.query(models.User).filter(models.User.role == payload.role.lower()).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"Demo user for role '{payload.role}' not found.")

    return {
        "status": "SUCCESS",
        "message": f"Signed in as {user.name} ({user.positionTitle})",
        "user": schemas.UserResponse.model_validate(user),
        "permissions": get_user_permissions(user)
    }

@router.get("/me")
def get_current_user_profile(email: Optional[str] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Returns profile and permission flags for a given user."""
    query = db.query(models.User)
    if user_id:
        user = query.filter(models.User.id == user_id).first()
    elif email:
        user = query.filter(models.User.email == email.strip().lower()).first()
    else:
        raise HTTPException(status_code=400, detail="Must provide email or user_id.")

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {
        "user": schemas.UserResponse.model_validate(user),
        "permissions": get_user_permissions(user)
    }
