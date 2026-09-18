from pydantic import BaseModel
from typing import List, Optional

# --- USER SCHEMAS ---

class UserCreate(BaseModel):
    name: str
    rollNumber: Optional[str] = ""
    email: Optional[str] = ""
    team: Optional[str] = ""
    password: Optional[str] = ""
    role: Optional[str] = "intern"
    positionTitle: Optional[str] = ""
    accountStatus: Optional[str] = "ACTIVE"

class UserLogin(BaseModel):
    rollNumber: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = ""
    rollNumber: Optional[str] = ""
    team: Optional[str] = ""
    role: str
    positionTitle: Optional[str] = ""
    accountStatus: Optional[str] = "ACTIVE"
    requestedRole: Optional[str] = None
    avatarUrl: Optional[str] = None
    
    model_config = {"from_attributes": True} 

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    rollNumber: Optional[str] = None
    team: Optional[str] = None
    role: Optional[str] = None
    positionTitle: Optional[str] = None
    accountStatus: Optional[str] = None
    password: Optional[str] = None

class AdminLogin(BaseModel):
    username: str
    password: str

class GoogleAuthRequest(BaseModel):
    credential: Optional[str] = None # Google JWT ID token
    email: Optional[str] = None
    name: Optional[str] = None
    avatarUrl: Optional[str] = None
    googleId: Optional[str] = None

class DemoAuthRequest(BaseModel):
    role: str
    email: Optional[str] = None

class OnboardRoleRequest(BaseModel):
    name: str
    email: str
    requestedRole: str # frontend_developer, backend_developer, devops_developer
    team: Optional[str] = ""

class UserApproveRequest(BaseModel):
    role: Optional[str] = None
    team: Optional[str] = None
    positionTitle: Optional[str] = None

# --- SCRUM SPRINT SCHEMAS ---

class SprintCreate(BaseModel):
    name: str
    durationDays: Optional[int] = 14 # Standard 2-week sprint duration
    startDate: str # YYYY-MM-DD
    endDate: Optional[str] = None
    scrumHeadId: Optional[int] = None
    goals: Optional[str] = None

class SprintUpdate(BaseModel):
    name: Optional[str] = None
    durationDays: Optional[int] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    scrumHeadId: Optional[int] = None
    status: Optional[str] = None # PLANNED, ACTIVE, COMPLETED, ARCHIVED
    goals: Optional[str] = None

class SprintResponse(BaseModel):
    id: int
    sprintId: str
    name: str
    durationDays: int
    startDate: str
    endDate: str
    scrumHeadId: Optional[int] = None
    scrumHeadName: Optional[str] = None
    status: str
    goals: Optional[str] = None
    createdAt: int
    closedAt: Optional[int] = None
    # Computed metrics
    totalTasks: Optional[int] = 0
    completedTasks: Optional[int] = 0
    inProgressTasks: Optional[int] = 0
    todoTasks: Optional[int] = 0
    pendingApprovalTasks: Optional[int] = 0
    progressPercentage: Optional[float] = 0.0

    model_config = {"from_attributes": True}

# --- USER STORY SCHEMAS ---

class StoryCreate(BaseModel):
    sprintId: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "MEDIUM" # LOW, MEDIUM, HIGH, URGENT
    assignedToId: Optional[int] = None
    dueDate: Optional[str] = None

class StoryUpdate(BaseModel):
    sprintId: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    assignedToId: Optional[int] = None
    status: Optional[str] = None # TODO, IN_PROGRESS, DONE, COMPLETED
    dueDate: Optional[str] = None

class StoryResponse(BaseModel):
    id: int
    storyId: str
    sprintId: Optional[int] = None
    title: str
    description: Optional[str] = None
    priority: str
    assignedToId: Optional[int] = None
    assignedToName: Optional[str] = None
    createdById: Optional[int] = None
    status: str
    createdDate: str
    dueDate: Optional[str] = None
    createdAt: int
    # Computed
    taskCount: Optional[int] = 0
    completedTaskCount: Optional[int] = 0

    model_config = {"from_attributes": True}

# --- TASK SCHEMAS ---

class TaskCreate(BaseModel):
    storyId: int
    title: str
    description: Optional[str] = None
    assignedToId: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignedToId: Optional[int] = None
    status: Optional[str] = None

class TaskStatusUpdate(BaseModel):
    status: str # TODO, IN_PROGRESS, DONE

class TaskSubmit(BaseModel):
    submissionNotes: Optional[str] = ""
    submissionLink: Optional[str] = ""

class TaskReview(BaseModel):
    decision: str # APPROVED, REJECTED
    feedback: Optional[str] = ""

class TaskResponse(BaseModel):
    id: int
    taskId: str
    storyId: int
    sprintId: Optional[int] = None
    title: str
    description: Optional[str] = None
    assignedToId: Optional[int] = None
    assignedToName: Optional[str] = None
    createdById: Optional[int] = None
    status: str
    submissionNotes: Optional[str] = None
    submissionLink: Optional[str] = None
    reviewNotes: Optional[str] = None
    reviewedById: Optional[int] = None
    reviewedByName: Optional[str] = None
    reviewedAt: Optional[int] = None
    createdAt: int
    updatedAt: int
    # Associated Story details
    storyTitle: Optional[str] = None
    storyPriority: Optional[str] = None

    model_config = {"from_attributes": True}

# --- NOTIFICATION & AUDIT LOG SCHEMAS ---

class NotificationResponse(BaseModel):
    id: int
    recipientId: int
    senderId: Optional[int] = None
    senderName: Optional[str] = None
    title: str
    message: str
    link: Optional[str] = None
    isRead: bool
    createdAt: int

    model_config = {"from_attributes": True}

class ActivityLogResponse(BaseModel):
    id: int
    entityType: str
    entityId: str
    action: str
    userId: Optional[int] = None
    userName: Optional[str] = None
    actorName: Optional[str] = None
    details: Optional[str] = None
    timestamp: int
    createdAt: Optional[int] = None

    model_config = {"from_attributes": True}

# --- EXISTING APPLICATION SCHEMAS ---

class LogCreate(BaseModel):
    userId: Optional[int] = None
    user_id: Optional[int] = None
    name: Optional[str] = ""
    rollNumber: Optional[str] = ""
    team: Optional[str] = ""
    hours: List[int] = []
    todayLog: Optional[str] = ""
    workDone: Optional[str] = None
    tomorrowGoal: Optional[str] = ""
    nextDayGoal: Optional[str] = None
    attendanceMode: Optional[str] = "office"
    date: Optional[str] = ""
    suggestionType: Optional[str] = None
    suggestionDescription: Optional[str] = None
    suggestionDeadline: Optional[str] = None
    suggestionStatus: Optional[str] = "Pending"

class LogUpdate(BaseModel):
    userId: Optional[int] = None
    user_id: Optional[int] = None
    name: Optional[str] = None
    rollNumber: Optional[str] = None
    team: Optional[str] = None
    hours: Optional[List[int]] = None
    todayLog: Optional[str] = None
    workDone: Optional[str] = None
    tomorrowGoal: Optional[str] = None
    nextDayGoal: Optional[str] = None
    attendanceMode: Optional[str] = None
    date: Optional[str] = None
    suggestionType: Optional[str] = None
    suggestionDescription: Optional[str] = None
    suggestionDeadline: Optional[str] = None
    suggestionStatus: Optional[str] = None

class LogResponse(BaseModel):
    id: int
    userId: Optional[int] = None
    user_id: Optional[int] = None
    name: str
    rollNumber: Optional[str] = ""
    team: Optional[str] = ""
    hours: List[int] = []
    todayLog: Optional[str] = ""
    workDone: Optional[str] = None
    tomorrowGoal: Optional[str] = ""
    nextDayGoal: Optional[str] = None
    attendanceMode: Optional[str] = "office"
    date: str
    timestamp: int
    suggestionType: Optional[str] = None
    suggestionDescription: Optional[str] = None
    suggestionDeadline: Optional[str] = None
    suggestionStatus: Optional[str] = "Pending"
    
    model_config = {"from_attributes": True}

class SuggestionStatusUpdate(BaseModel):
    status: str

class HolidayCreate(BaseModel):
    date: str
    name: str

class HolidayResponse(BaseModel):
    id: int
    date: str
    name: str

    class Config:
        from_attributes = True

class MoMCreateText(BaseModel):
    title: Optional[str] = ""
    team: Optional[str] = ""
    date: str
    agenda: str
    created_by: str
    attendees: Optional[str] = ""
    content: str
    
class MoMResponse(BaseModel):
    id: int
    title: Optional[str] = ""
    team: Optional[str] = ""
    date: str
    agenda: str
    created_by: str
    author_name: Optional[str] = None
    attendees: Optional[str] = None
    content: Optional[str] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None

    class Config:
        from_attributes = True

class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    leadId: Optional[int] = None
    leadName: Optional[str] = None
    isLeadership: Optional[bool] = False

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    leadId: Optional[int] = None
    leadName: Optional[str] = None
    isLeadership: Optional[bool] = None

class TeamResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    leadId: Optional[int] = None
    leadName: Optional[str] = None
    isLeadership: Optional[bool] = False
    memberCount: Optional[int] = 0

    model_config = {"from_attributes": True}