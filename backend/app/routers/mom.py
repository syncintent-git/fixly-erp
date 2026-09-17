import os
import time
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from supabase import create_client, Client

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/mom", tags=["Minutes of Meeting"])
moms_router = APIRouter(prefix="/api/moms", tags=["Minutes of Meeting"])

# --- SUPABASE INITIALIZATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "moms"

UPLOAD_DIR = "uploads/mom"
os.makedirs(UPLOAD_DIR, exist_ok=True)

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None

def get_all_moms_db(db: Session):
    return db.query(models.MoM).order_by(models.MoM.date.desc(), models.MoM.id.desc()).all()

@router.get("/", response_model=List[schemas.MoMResponse])
@router.get("", response_model=List[schemas.MoMResponse])
@router.get("/all", response_model=List[schemas.MoMResponse])
@moms_router.get("/", response_model=List[schemas.MoMResponse])
@moms_router.get("", response_model=List[schemas.MoMResponse])
@moms_router.get("/all", response_model=List[schemas.MoMResponse])
def get_moms(db: Session = Depends(get_db)):
    """Fetch all MoMs, ordered by newest first"""
    return get_all_moms_db(db)

def create_mom_record(
    date: str,
    agenda: str,
    title: str,
    team: str,
    attendees: str,
    content: str,
    created_by: str,
    file: Optional[UploadFile],
    db: Session
) -> models.MoM:
    file_path = None
    file_name = None

    if file and file.filename:
        file_name = file.filename
        if supabase:
            unique_filename = f"{int(time.time())}_{file.filename.replace(' ', '_')}"
            file_bytes = file.file.read()
            supabase.storage.from_(BUCKET_NAME).upload(
                path=unique_filename,
                file=file_bytes,
                file_options={"content-type": file.content_type}
            )
            file_path = unique_filename
        else:
            timestamp = int(time.time())
            safe_filename = f"{timestamp}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, safe_filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

    new_mom = models.MoM(
        title=title or agenda,
        team=team or "General",
        date=date,
        agenda=agenda,
        attendees=attendees or "",
        content=content or "",
        created_by=created_by or "Coordinator",
        file_name=file_name,
        file_path=file_path
    )
    db.add(new_mom)
    db.commit()
    db.refresh(new_mom)
    return new_mom

@router.post("/create", response_model=schemas.MoMResponse)
@moms_router.post("/create", response_model=schemas.MoMResponse)
@router.post("/upload", response_model=schemas.MoMResponse)
@moms_router.post("/upload", response_model=schemas.MoMResponse)
def upload_or_create_mom(
    date: str = Form(...),
    agenda: Optional[str] = Form(""),
    title: Optional[str] = Form(""),
    team: Optional[str] = Form("General"),
    attendees: Optional[str] = Form(""),
    content: Optional[str] = Form(""),
    created_by: Optional[str] = Form(None),
    author_name: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Creates a new MoM with optional document attachment."""
    meeting_title = title or agenda or "Meeting"
    meeting_agenda = agenda or title or "Discussion"
    creator = author_name or created_by or "Coordinator"
    return create_mom_record(
        date=date,
        agenda=meeting_agenda,
        title=meeting_title,
        team=team or "General",
        attendees=attendees or "",
        content=content or "",
        created_by=creator,
        file=file,
        db=db
    )

@router.post("/text", response_model=schemas.MoMResponse)
@moms_router.post("/text", response_model=schemas.MoMResponse)
def create_text_mom(mom: schemas.MoMCreateText, db: Session = Depends(get_db)):
    """Create a new MoM using manual text entry via JSON"""
    new_mom = models.MoM(
        title=mom.title or mom.agenda,
        team=mom.team or "General",
        date=mom.date,
        agenda=mom.agenda,
        attendees=mom.attendees or "",
        content=mom.content or "",
        created_by=mom.created_by or "Coordinator"
    )
    db.add(new_mom)
    db.commit()
    db.refresh(new_mom)
    return new_mom

def get_mom_file_response(mom_id: int, db: Session):
    mom = db.query(models.MoM).filter(models.MoM.id == mom_id).first()
    if not mom or not mom.file_path:
        raise HTTPException(status_code=404, detail="File record not found in database")
    
    if supabase:
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(mom.file_path)
        return RedirectResponse(url=public_url)
    else:
        if not os.path.exists(mom.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(
            path=mom.file_path, 
            filename=mom.file_name,
            content_disposition_type="inline" 
        )

@router.get("/download/{mom_id}")
@router.get("/view/{mom_id}")
@moms_router.get("/download/{mom_id}")
@moms_router.get("/view/{mom_id}")
def view_mom_file(mom_id: int, db: Session = Depends(get_db)):
    """View or download an uploaded MoM file"""
    return get_mom_file_response(mom_id, db)

def delete_mom_record(mom_id: int, db: Session):
    mom = db.query(models.MoM).filter(models.MoM.id == mom_id).first()
    if not mom:
        raise HTTPException(status_code=404, detail="MoM not found")
    
    if mom.file_path:
        if supabase:
            try:
                supabase.storage.from_(BUCKET_NAME).remove([mom.file_path])
            except Exception as e:
                print(f"[NOTICE] Failed to delete file from Supabase: {e}")
        else:
            if os.path.exists(mom.file_path):
                os.remove(mom.file_path)
        
    db.delete(mom)
    db.commit()
    return {"message": "MoM deleted successfully"}

@router.delete("/{mom_id}")
@router.delete("/delete/{mom_id}")
@moms_router.delete("/{mom_id}")
@moms_router.delete("/delete/{mom_id}")
def delete_mom(mom_id: int, db: Session = Depends(get_db)):
    """Delete an MoM record and its file"""
    return delete_mom_record(mom_id, db)
