import time
import jwt
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/auth", tags=["Authentication & Google OAuth"])



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
    """Authenticates a user via Google GIS credential or email payload."""
    email = payload.email
    name = payload.name
    avatar_url = payload.avatarUrl

    # If a JWT ID credential was sent, decode the payload
    if payload.credential and not email:
        try:
            # Unverified decode for extracting profile claims
            decoded = jwt.decode(payload.credential, options={"verify_signature": False})
            email = decoded.get("email")
            name = name or decoded.get("name")
            avatar_url = avatar_url or decoded.get("picture")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid Google credential: {e}")

    if not email:
        raise HTTPException(status_code=400, detail="Google authentication did not provide an email address.")

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

    allowed_tracks = {
        "frontend_developer": ("Frontend Developer Intern", "Mobile Application Development"),
        "backend_developer": ("Backend Developer Intern", "Mobile Application Development"),
        "devops_developer": ("DevOps Developer Intern", "DevOps")
    }

    if payload.requestedRole not in allowed_tracks:
        raise HTTPException(status_code=400, detail="Invalid role. Must be frontend_developer, backend_developer, or devops_developer.")

    pos_title, default_team = allowed_tracks[payload.requestedRole]
    now_ms = int(time.time() * 1000)
    roll_no = f"FX-APP-{int(time.time()) % 10000}"

    new_user = models.User(
        name=payload.name,
        email=clean_email,
        rollNumber=roll_no,
        team=payload.team or default_team,
        role=payload.requestedRole,
        requestedRole=payload.requestedRole,
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
            link="/admin",
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
