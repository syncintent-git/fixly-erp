from sqlalchemy import Column, Integer, String, BigInteger, JSON, Boolean, Text
from .database import Base

# 1. The Accounts Table (Users & Role-Based Access)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)
    rollNumber = Column(String, unique=True, index=True, nullable=True)
    team = Column(String, default="")
    # Roles: admin, ceo, cto, coo, cfo, cmo, mentor, cdc, scrum_head, frontend_developer, backend_developer, devops_developer, intern, viewer, student
    role = Column(String, default="intern") 
    positionTitle = Column("position_title", String, default="")
    accountStatus = Column("account_status", String, default="ACTIVE") # ACTIVE, PENDING_APPROVAL, REJECTED
    requestedRole = Column("requested_role", String, nullable=True)
    googleId = Column("google_id", String, nullable=True)
    avatarUrl = Column("avatar_url", String, nullable=True)
    createdAt = Column(BigInteger)
    password = Column(String, nullable=True)

# 2. Scrum Sprint Table (Default 14-day / 2-week cycle)
class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    sprintId = Column("sprint_id", String, unique=True, index=True) # e.g. "SP-001" or "Sprint 07"
    name = Column(String) # e.g. "Sprint 07"
    durationDays = Column("duration_days", Integer, default=14) # Standard 2-week cycle
    startDate = Column("start_date", String) # YYYY-MM-DD
    endDate = Column("end_date", String) # YYYY-MM-DD
    scrumHeadId = Column("scrum_head_id", Integer, nullable=True)
    scrumHeadName = Column("scrum_head_name", String, nullable=True)
    status = Column(String, default="ACTIVE") # PLANNED, ACTIVE, COMPLETED, ARCHIVED
    goals = Column(Text, nullable=True)
    createdAt = Column("created_at", BigInteger)
    closedAt = Column("closed_at", BigInteger, nullable=True)

# 3. User Story Table (Hierarchy: Sprint -> Story -> Task)
class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    storyId = Column("story_id", String, unique=True, index=True) # e.g. "ST-101"
    sprintId = Column("sprint_id", Integer, nullable=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    priority = Column(String, default="MEDIUM") # LOW, MEDIUM, HIGH, URGENT
    assignedToId = Column("assigned_to_id", Integer, nullable=True)
    assignedToName = Column("assigned_to_name", String, nullable=True)
    createdById = Column("created_by_id", Integer, nullable=True)
    status = Column(String, default="TODO") # TODO, IN_PROGRESS, DONE, COMPLETED
    createdDate = Column("created_date", String)
    dueDate = Column("due_date", String, nullable=True)
    createdAt = Column("created_at", BigInteger)

# 4. Actionable Task / Intern Work Item
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    taskId = Column("task_id", String, unique=True, index=True) # e.g. "TASK-101"
    storyId = Column("story_id", Integer, index=True)
    sprintId = Column("sprint_id", Integer, nullable=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    assignedToId = Column("assigned_to_id", Integer, nullable=True)
    assignedToName = Column("assigned_to_name", String, nullable=True)
    createdById = Column("created_by_id", Integer, nullable=True)
    # Workflow: TODO -> IN_PROGRESS -> DONE -> PENDING_APPROVAL -> APPROVED (or REJECTED -> IN_PROGRESS) -> COMPLETED
    status = Column(String, default="TODO")
    submissionNotes = Column("submission_notes", Text, nullable=True)
    submissionLink = Column("submission_link", String, nullable=True)
    reviewNotes = Column("review_notes", Text, nullable=True)
    reviewedById = Column("reviewed_by_id", Integer, nullable=True)
    reviewedByName = Column("reviewed_by_name", String, nullable=True)
    reviewedAt = Column("reviewed_at", BigInteger, nullable=True)
    createdAt = Column("created_at", BigInteger)
    updatedAt = Column("updated_at", BigInteger)

# 5. Review & Approval Audit Record
class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    taskId = Column("task_id", Integer, index=True)
    reviewerId = Column("reviewer_id", Integer)
    reviewerName = Column("reviewer_name", String)
    decision = Column(String) # APPROVED, REJECTED
    feedback = Column(Text, nullable=True)
    timestamp = Column(BigInteger)

# 6. Audit Trail / Activity Log
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    entityType = Column("entity_type", String) # SPRINT, STORY, TASK, USER
    entityId = Column("entity_id", String)
    action = Column(String) # CREATED, ASSIGNED, STATUS_CHANGE, SUBMITTED, APPROVED, REJECTED
    userId = Column("user_id", Integer, nullable=True)
    userName = Column("user_name", String, nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(BigInteger)

# 7. In-App Notifications
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipientId = Column("recipient_id", Integer, index=True)
    senderId = Column("sender_id", Integer, nullable=True)
    senderName = Column("sender_name", String, nullable=True)
    title = Column(String)
    message = Column(Text)
    link = Column(String, nullable=True)
    isRead = Column("is_read", Boolean, default=False)
    createdAt = Column("created_at", BigInteger)

# 8. The Daily Updates Table (Existing)
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    name = Column(String)
    rollNumber = Column(String)
    team = Column(String)
    hours = Column(JSON)
    todayLog = Column(String)
    tomorrowGoal = Column(String)
    date = Column(String)
    timestamp = Column(BigInteger)
    suggestionType = Column("suggestiontype", String, nullable=True)
    suggestionDescription = Column("suggestiondescription", String, nullable=True)
    suggestionDeadline = Column("suggestiondeadline", String, nullable=True)
    suggestionStatus = Column("suggestionstatus", String, default="Pending")
    attendanceMode = Column("attendance_mode", String, default="office", nullable=True)

# 9. The Holidays Table (Existing)
class Holiday(Base):
    __tablename__ = "holidays"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)
    name = Column(String)

# 10. Minutes of Meeting Table (Existing)
class MoM(Base):
    __tablename__ = "moms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="", nullable=True)
    team = Column(String, default="", nullable=True)
    date = Column(String)
    agenda = Column(String)
    attendees = Column(String, nullable=True)
    content = Column(String, nullable=True)
    created_by = Column(String)
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)

    @property
    def author_name(self):
        return self.created_by

# 11. Teams Table (Existing)
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, default="", nullable=True)
    lead_name = Column("lead_name", String, default="", nullable=True)
    lead_id = Column("lead_id", Integer, nullable=True)
    createdAt = Column("created_at", BigInteger, nullable=True)
