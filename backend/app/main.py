from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .routers import logs, users, holidays, mom, teams, auth, scrum
from .database import engine, Base, SessionLocal, get_db
from .models import Team
from .seed_data import migrate_sqlite_columns, seed_scrum_data

# Ensure all database tables exist
Base.metadata.create_all(bind=engine)

# Run non-destructive column migrations for SQLite
migrate_sqlite_columns(engine)

# Pre-populate default teams and Scrum seed data
db = SessionLocal()
try:
    if db.query(Team).count() == 0:
        default_teams = ["Mobile Application Development Team", "DevOps Team"]
        for team_name in default_teams:
            db.add(Team(name=team_name))
        db.commit()
    
    # Initialize leadership accounts
    seed_scrum_data(db)
except Exception as e:
    print(f"[WARNING] Database initialization notice: {e}")
finally:
    db.close()

app = FastAPI(title="Fixly Office & Scrum API")

allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "*")
origins = [origin.strip() for origin in allowed_origins_env.split(",")] if allowed_origins_env else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(scrum.router)
app.include_router(logs.router)
app.include_router(users.router)
app.include_router(holidays.router)
app.include_router(mom.router)
app.include_router(mom.moms_router)
app.include_router(teams.router)

@app.get("/")
def health_check():
    return {"status": "Fixly Office & Scrum API is running securely!"}

@app.get("/keep-alive")
def keep_alive():
    return {"status": "I am awake!"}