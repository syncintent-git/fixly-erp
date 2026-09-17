import time
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/scrum", tags=["Scrum, Sprints & Intern Tasks"])

# --- HELPER FUNCTIONS ---

def generate_sprint_id(db: Session) -> str:
    count = db.query(models.Sprint).count() + 1
    return f"SP-{count:03d}"

def generate_story_id(db: Session) -> str:
    count = db.query(models.Story).count() + 1
    return f"ST-{count:03d}"

def generate_task_id(db: Session) -> str:
    count = db.query(models.Task).count() + 1
    return f"TASK-{count:03d}"

def compute_sprint_metrics(sprint: models.Sprint, db: Session):
    tasks = db.query(models.Task).filter(models.Task.sprintId == sprint.id).all()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status in ["APPROVED", "COMPLETED", "DONE"])
    in_progress = sum(1 for t in tasks if t.status == "IN_PROGRESS")
    todo = sum(1 for t in tasks if t.status == "TODO")
    done = sum(1 for t in tasks if t.status == "DONE")
    pending = sum(1 for t in tasks if t.status == "PENDING_APPROVAL")
    pct = round((completed / total * 100), 1) if total > 0 else 0.0

    return {
        "totalTasks": total,
        "completedTasks": completed,
        "inProgressTasks": in_progress,
        "todoTasks": todo,
        "pendingApprovalTasks": pending,
        "progressPercentage": pct
    }

def log_activity(db: Session, entity_type: str, entity_id: str, action: str, user_id: Optional[int], user_name: Optional[str], details: str):
    activity = models.ActivityLog(
        entityType=entity_type,
        entityId=str(entity_id),
        action=action,
        userId=user_id,
        userName=user_name,
        details=details,
        timestamp=int(time.time() * 1000)
    )
    db.add(activity)

# ==========================================
# 1. SPRINT ENDPOINTS (14-Day Default Cycle)
# ==========================================

@router.get("/sprints", response_model=List[schemas.SprintResponse])
def get_all_sprints(db: Session = Depends(get_db)):
    """Lists all sprints with completion metrics."""
    sprints = db.query(models.Sprint).order_by(models.Sprint.createdAt.desc()).all()
    result = []
    for s in sprints:
        metrics = compute_sprint_metrics(s, db)
        s_dict = schemas.SprintResponse.model_validate(s).model_dump()
        s_dict.update(metrics)
        result.append(schemas.SprintResponse(**s_dict))
    return result

@router.post("/sprints", response_model=schemas.SprintResponse)
def create_sprint(sprint_in: schemas.SprintCreate, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Creates a new sprint. Default duration is 14 days (2 weeks)."""
    now_ms = int(time.time() * 1000)
    duration = sprint_in.durationDays or 14

    # Calculate end date if not explicitly supplied
    start_dt = datetime.strptime(sprint_in.startDate, "%Y-%m-%d")
    end_date = sprint_in.endDate or (start_dt + timedelta(days=duration)).strftime("%Y-%m-%d")

    scrum_head_name = "Rahul Sharma"
    if sprint_in.scrumHeadId:
        head_user = db.query(models.User).filter(models.User.id == sprint_in.scrumHeadId).first()
        if head_user:
            scrum_head_name = head_user.name

    new_sprint = models.Sprint(
        sprintId=generate_sprint_id(db),
        name=sprint_in.name,
        durationDays=duration,
        startDate=sprint_in.startDate,
        endDate=end_date,
        scrumHeadId=sprint_in.scrumHeadId,
        scrumHeadName=scrum_head_name,
        status="ACTIVE",
        goals=sprint_in.goals,
        createdAt=now_ms
    )
    db.add(new_sprint)
    db.commit()
    db.refresh(new_sprint)

    log_activity(db, "SPRINT", new_sprint.sprintId, "CREATED", user_id, scrum_head_name, f"Created {duration}-day sprint '{new_sprint.name}' ({new_sprint.startDate} to {new_sprint.endDate})")
    db.commit()

    metrics = compute_sprint_metrics(new_sprint, db)
    s_dict = schemas.SprintResponse.model_validate(new_sprint).model_dump()
    s_dict.update(metrics)
    return schemas.SprintResponse(**s_dict)

@router.get("/sprints/active", response_model=Optional[schemas.SprintResponse])
def get_active_sprint(db: Session = Depends(get_db)):
    """Returns the current active sprint (or most recent)."""
    sprint = db.query(models.Sprint).filter(models.Sprint.status == "ACTIVE").order_by(models.Sprint.createdAt.desc()).first()
    if not sprint:
        sprint = db.query(models.Sprint).order_by(models.Sprint.createdAt.desc()).first()
    if not sprint:
        return None
    metrics = compute_sprint_metrics(sprint, db)
    s_dict = schemas.SprintResponse.model_validate(sprint).model_dump()
    s_dict.update(metrics)
    return schemas.SprintResponse(**s_dict)

@router.get("/sprints/{sprint_id}", response_model=schemas.SprintResponse)
def get_sprint_by_id(sprint_id: int, db: Session = Depends(get_db)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    metrics = compute_sprint_metrics(sprint, db)
    s_dict = schemas.SprintResponse.model_validate(sprint).model_dump()
    s_dict.update(metrics)
    return schemas.SprintResponse(**s_dict)

@router.put("/sprints/{sprint_id}", response_model=schemas.SprintResponse)
def update_sprint(sprint_id: int, update_in: schemas.SprintUpdate, db: Session = Depends(get_db)):
    sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")

    if update_in.name is not None: sprint.name = update_in.name
    if update_in.durationDays is not None: sprint.durationDays = update_in.durationDays
    if update_in.startDate is not None: sprint.startDate = update_in.startDate
    if update_in.endDate is not None: sprint.endDate = update_in.endDate
    if update_in.goals is not None: sprint.goals = update_in.goals
    if update_in.scrumHeadId is not None:
        sprint.scrumHeadId = update_in.scrumHeadId
        head_user = db.query(models.User).filter(models.User.id == update_in.scrumHeadId).first()
        if head_user: sprint.scrumHeadName = head_user.name
    if update_in.status is not None:
        sprint.status = update_in.status
        if update_in.status == "COMPLETED":
            sprint.closedAt = int(time.time() * 1000)

    db.commit()
    db.refresh(sprint)

    metrics = compute_sprint_metrics(sprint, db)
    s_dict = schemas.SprintResponse.model_validate(sprint).model_dump()
    s_dict.update(metrics)
    return schemas.SprintResponse(**s_dict)

@router.post("/sprints/{sprint_id}/rollover")
def rollover_unfinished_tasks(sprint_id: int, target_sprint_id: int, db: Session = Depends(get_db)):
    """Carries forward incomplete tasks (TODO, IN_PROGRESS) to a new target sprint."""
    source_sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    target_sprint = db.query(models.Sprint).filter(models.Sprint.id == target_sprint_id).first()

    if not source_sprint or not target_sprint:
        raise HTTPException(status_code=404, detail="Source or target sprint not found")

    unfinished_tasks = db.query(models.Task).filter(
        models.Task.sprintId == sprint_id,
        models.Task.status.in_(["TODO", "IN_PROGRESS"])
    ).all()

    for task in unfinished_tasks:
        task.sprintId = target_sprint_id
        task.updatedAt = int(time.time() * 1000)

    source_sprint.status = "COMPLETED"
    source_sprint.closedAt = int(time.time() * 1000)
    db.commit()

    log_activity(db, "SPRINT", source_sprint.sprintId, "ROLLOVER", None, "System", f"Rolled over {len(unfinished_tasks)} unfinished tasks from {source_sprint.name} to {target_sprint.name}")
    db.commit()

    return {
        "message": f"Successfully rolled over {len(unfinished_tasks)} tasks to {target_sprint.name}",
        "tasksRolledOver": len(unfinished_tasks)
    }

# ==========================================
# 2. STORY ENDPOINTS
# ==========================================

@router.get("/stories", response_model=List[schemas.StoryResponse])
def get_stories(sprint_id: Optional[int] = None, assigned_to_id: Optional[int] = None, status: Optional[str] = None, db: Session = Depends(get_db)):
    """Lists stories with task count indicators."""
    query = db.query(models.Story)
    if sprint_id: query = query.filter(models.Story.sprintId == sprint_id)
    if assigned_to_id: query = query.filter(models.Story.assignedToId == assigned_to_id)
    if status: query = query.filter(models.Story.status == status)

    stories = query.order_by(models.Story.createdAt.desc()).all()
    result = []
    for st in stories:
        tasks = db.query(models.Task).filter(models.Task.storyId == st.id).all()
        task_count = len(tasks)
        comp_count = sum(1 for t in tasks if t.status in ["APPROVED", "COMPLETED", "DONE"])
        st_dict = schemas.StoryResponse.model_validate(st).model_dump()
        st_dict["taskCount"] = task_count
        st_dict["completedTaskCount"] = comp_count
        result.append(schemas.StoryResponse(**st_dict))
    return result

@router.post("/stories", response_model=schemas.StoryResponse)
def create_story(story_in: schemas.StoryCreate, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Creates a user story with auto-generated ID (e.g. ST-001)."""
    now_ms = int(time.time() * 1000)
    today_str = datetime.now().strftime("%Y-%m-%d")

    assigned_name = None
    if story_in.assignedToId:
        assignee = db.query(models.User).filter(models.User.id == story_in.assignedToId).first()
        if assignee: assigned_name = assignee.name

    new_story = models.Story(
        storyId=generate_story_id(db),
        sprintId=story_in.sprintId,
        title=story_in.title,
        description=story_in.description,
        priority=story_in.priority or "MEDIUM",
        assignedToId=story_in.assignedToId,
        assignedToName=assigned_name,
        createdById=user_id,
        status="TODO",
        createdDate=today_str,
        dueDate=story_in.dueDate,
        createdAt=now_ms
    )
    db.add(new_story)
    db.commit()
    db.refresh(new_story)

    log_activity(db, "STORY", new_story.storyId, "CREATED", user_id, assigned_name, f"Created story {new_story.storyId}: '{new_story.title}'")
    db.commit()

    st_dict = schemas.StoryResponse.model_validate(new_story).model_dump()
    st_dict["taskCount"] = 0
    st_dict["completedTaskCount"] = 0
    return schemas.StoryResponse(**st_dict)

@router.put("/stories/{story_id}", response_model=schemas.StoryResponse)
def update_story(story_id: int, update_in: schemas.StoryUpdate, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    if update_in.title is not None: story.title = update_in.title
    if update_in.description is not None: story.description = update_in.description
    if update_in.priority is not None: story.priority = update_in.priority
    if update_in.status is not None: story.status = update_in.status
    if update_in.dueDate is not None: story.dueDate = update_in.dueDate
    if update_in.sprintId is not None: story.sprintId = update_in.sprintId
    if update_in.assignedToId is not None:
        story.assignedToId = update_in.assignedToId
        assignee = db.query(models.User).filter(models.User.id == update_in.assignedToId).first()
        if assignee: story.assignedToName = assignee.name

    db.commit()
    db.refresh(story)

    tasks = db.query(models.Task).filter(models.Task.storyId == story.id).all()
    st_dict = schemas.StoryResponse.model_validate(story).model_dump()
    st_dict["taskCount"] = len(tasks)
    st_dict["completedTaskCount"] = sum(1 for t in tasks if t.status in ["APPROVED", "COMPLETED", "DONE"])
    return schemas.StoryResponse(**st_dict)

@router.delete("/stories/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    # Delete child tasks
    db.query(models.Task).filter(models.Task.storyId == story_id).delete()
    db.delete(story)
    db.commit()
    return {"message": f"Story {story.storyId} and its tasks deleted successfully"}

# ==========================================
# 3. TASK ENDPOINTS & APPROVAL PIPELINE
# ==========================================

@router.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    sprint_id: Optional[int] = None,
    story_id: Optional[int] = None,
    assigned_to_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lists tasks with optional filters (sprint, story, assignee, status)."""
    query = db.query(models.Task)
    if sprint_id: query = query.filter(models.Task.sprintId == sprint_id)
    if story_id: query = query.filter(models.Task.storyId == story_id)
    if assigned_to_id: query = query.filter(models.Task.assignedToId == assigned_to_id)
    if status: query = query.filter(models.Task.status == status)

    tasks = query.order_by(models.Task.createdAt.desc()).all()
    result = []
    for t in tasks:
        t_dict = schemas.TaskResponse.model_validate(t).model_dump()
        story = db.query(models.Story).filter(models.Story.id == t.storyId).first()
        if story:
            t_dict["storyTitle"] = story.title
            t_dict["storyPriority"] = story.priority
        result.append(schemas.TaskResponse(**t_dict))
    return result

@router.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task_in: schemas.TaskCreate, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Creates a task under a story with auto-generated ID (TASK-001)."""
    story = db.query(models.Story).filter(models.Story.id == task_in.storyId).first()
    if not story:
        raise HTTPException(status_code=404, detail="Parent story not found")

    now_ms = int(time.time() * 1000)
    assigned_name = None
    if task_in.assignedToId:
        assignee = db.query(models.User).filter(models.User.id == task_in.assignedToId).first()
        if assignee: assigned_name = assignee.name

    new_task = models.Task(
        taskId=generate_task_id(db),
        storyId=task_in.storyId,
        sprintId=story.sprintId,
        title=task_in.title,
        description=task_in.description,
        assignedToId=task_in.assignedToId,
        assignedToName=assigned_name,
        createdById=user_id,
        status="TODO",
        createdAt=now_ms,
        updatedAt=now_ms
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Notify intern if assigned
    if task_in.assignedToId:
        db.add(models.Notification(
            recipientId=task_in.assignedToId,
            senderId=user_id,
            senderName="Scrum Head",
            title=f"New Task Assigned: {new_task.taskId}",
            message=f"You have been assigned to '{new_task.title}' under story {story.storyId}.",
            link="/intern",
            isRead=False,
            createdAt=now_ms
        ))
        log_activity(db, "TASK", new_task.taskId, "ASSIGNED", user_id, assigned_name, f"Assigned {new_task.taskId} to {assigned_name}")
        db.commit()

    t_dict = schemas.TaskResponse.model_validate(new_task).model_dump()
    t_dict["storyTitle"] = story.title
    t_dict["storyPriority"] = story.priority
    return schemas.TaskResponse(**t_dict)

@router.put("/tasks/{task_id}/status", response_model=schemas.TaskResponse)
def update_task_status(task_id: int, status_in: schemas.TaskStatusUpdate, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Advances task status (e.g. TODO -> IN_PROGRESS -> DONE)."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.status
    task.status = status_in.status
    task.updatedAt = int(time.time() * 1000)
    db.commit()
    db.refresh(task)

    log_activity(db, "TASK", task.taskId, "STATUS_CHANGE", user_id, task.assignedToName, f"Changed status of {task.taskId} from {old_status} to {task.status}")
    db.commit()

    story = db.query(models.Story).filter(models.Story.id == task.storyId).first()
    t_dict = schemas.TaskResponse.model_validate(task).model_dump()
    if story:
        t_dict["storyTitle"] = story.title
        t_dict["storyPriority"] = story.priority
    return schemas.TaskResponse(**t_dict)

@router.post("/tasks/{task_id}/submit", response_model=schemas.TaskResponse)
def submit_task_for_approval(task_id: int, submit_in: schemas.TaskSubmit, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Intern marks work complete and submits for review (sets PENDING_APPROVAL)."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    now_ms = int(time.time() * 1000)
    task.status = "PENDING_APPROVAL"
    task.submissionNotes = submit_in.submissionNotes
    task.submissionLink = submit_in.submissionLink
    task.updatedAt = now_ms
    db.commit()
    db.refresh(task)

    # Notify Admins and Scrum Head
    reviewers = db.query(models.User).filter(models.User.role.in_(["admin", "ceo", "cto", "scrum_head"])).all()
    for rev in reviewers:
        db.add(models.Notification(
            recipientId=rev.id,
            senderId=user_id,
            senderName=task.assignedToName,
            title=f"Work Submitted for Approval: {task.taskId}",
            message=f"{task.assignedToName} submitted '{task.title}' for review.",
            link="/admin",
            isRead=False,
            createdAt=now_ms
        ))

    log_activity(db, "TASK", task.taskId, "SUBMITTED", user_id, task.assignedToName, f"Submitted {task.taskId} for approval with notes: {submit_in.submissionNotes}")
    db.commit()

    story = db.query(models.Story).filter(models.Story.id == task.storyId).first()
    t_dict = schemas.TaskResponse.model_validate(task).model_dump()
    if story:
        t_dict["storyTitle"] = story.title
        t_dict["storyPriority"] = story.priority
    return schemas.TaskResponse(**t_dict)

@router.post("/tasks/{task_id}/review", response_model=schemas.TaskResponse)
def review_task(task_id: int, review_in: schemas.TaskReview, reviewer_id: int, db: Session = Depends(get_db)):
    """Reviewer (Admin, Scrum Head) approves or rejects task. If rejected, returns to IN_PROGRESS with feedback."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    reviewer = db.query(models.User).filter(models.User.id == reviewer_id).first()
    reviewer_name = reviewer.name if reviewer else "Administrator"

    # Block View-Only users (CDC, Mentor, Viewer, CFO, CMO) and interns from approving or rejecting
    allowed_reviewers = ["admin", "ceo", "cto", "coo", "scrum_head"]
    if reviewer and reviewer.role not in allowed_reviewers:
        raise HTTPException(status_code=403, detail="Reviewer accounts and interns have view-only privileges and cannot perform approval actions.")

    now_ms = int(time.time() * 1000)
    decision = review_in.decision.upper()

    if decision == "APPROVED":
        task.status = "APPROVED"
        task.reviewNotes = review_in.feedback or "Approved"
        task.reviewedById = reviewer_id
        task.reviewedByName = reviewer_name
        task.reviewedAt = now_ms
        task.updatedAt = now_ms

        # Record approval
        db.add(models.Approval(
            taskId=task.id,
            reviewerId=reviewer_id,
            reviewerName=reviewer_name,
            decision="APPROVED",
            feedback=review_in.feedback,
            timestamp=now_ms
        ))

        # Notify author
        if task.assignedToId:
            db.add(models.Notification(
                recipientId=task.assignedToId,
                senderId=reviewer_id,
                senderName=reviewer_name,
                title=f"Task Approved: {task.taskId}",
                message=f"Your work on '{task.title}' was approved by {reviewer_name}!",
                link="/intern",
                isRead=False,
                createdAt=now_ms
            ))

        log_activity(db, "TASK", task.taskId, "APPROVED", reviewer_id, reviewer_name, f"Approved {task.taskId}. Feedback: {review_in.feedback}")

    elif decision == "REJECTED":
        task.status = "IN_PROGRESS" # Returns directly to In Progress so intern can resolve feedback
        task.reviewNotes = review_in.feedback or "Rework requested"
        task.reviewedById = reviewer_id
        task.reviewedByName = reviewer_name
        task.reviewedAt = now_ms
        task.updatedAt = now_ms

        # Record rejection
        db.add(models.Approval(
            taskId=task.id,
            reviewerId=reviewer_id,
            reviewerName=reviewer_name,
            decision="REJECTED",
            feedback=review_in.feedback,
            timestamp=now_ms
        ))

        # Alert intern with rework instructions
        if task.assignedToId:
            db.add(models.Notification(
                recipientId=task.assignedToId,
                senderId=reviewer_id,
                senderName=reviewer_name,
                title=f"Changes Requested: {task.taskId}",
                message=f"{reviewer_name} requested rework: '{review_in.feedback}'. Task returned to In Progress.",
                link="/intern",
                isRead=False,
                createdAt=now_ms
            ))

        log_activity(db, "TASK", task.taskId, "REJECTED", reviewer_id, reviewer_name, f"Rejected {task.taskId} with feedback: {review_in.feedback}")
    else:
        raise HTTPException(status_code=400, detail="Decision must be APPROVED or REJECTED")

    db.commit()
    db.refresh(task)

    story = db.query(models.Story).filter(models.Story.id == task.storyId).first()
    t_dict = schemas.TaskResponse.model_validate(task).model_dump()
    if story:
        t_dict["storyTitle"] = story.title
        t_dict["storyPriority"] = story.priority
    return schemas.TaskResponse(**t_dict)

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task_details(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_in.title is not None: task.title = task_in.title
    if task_in.description is not None: task.description = task_in.description
    if task_in.status is not None: task.status = task_in.status
    if task_in.assignedToId is not None:
        task.assignedToId = task_in.assignedToId
        assignee = db.query(models.User).filter(models.User.id == task_in.assignedToId).first()
        if assignee: task.assignedToName = assignee.name

    task.updatedAt = int(time.time() * 1000)
    db.commit()
    db.refresh(task)

    story = db.query(models.Story).filter(models.Story.id == task.storyId).first()
    t_dict = schemas.TaskResponse.model_validate(task).model_dump()
    if story:
        t_dict["storyTitle"] = story.title
        t_dict["storyPriority"] = story.priority
    return schemas.TaskResponse(**t_dict)

# ==========================================
# 4. USER ACCOUNT APPROVAL ENDPOINTS
# ==========================================

@router.get("/pending-users", response_model=List[schemas.UserResponse])
def get_pending_user_registrations(db: Session = Depends(get_db)):
    """Fetches users awaiting Admin approval (e.g. new intern sign-ups)."""
    return db.query(models.User).filter(models.User.accountStatus == "PENDING_APPROVAL").order_by(models.User.createdAt.desc()).all()

@router.post("/users/{user_id}/approve", response_model=schemas.UserResponse)
def approve_user_account(user_id: int, approve_in: schemas.UserApproveRequest, reviewer_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Admin/CEO/CTO approves a pending intern account, enabling workspace login."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.accountStatus = "ACTIVE"
    if approve_in.role: user.role = approve_in.role
    if approve_in.team: user.team = approve_in.team
    if approve_in.positionTitle: user.positionTitle = approve_in.positionTitle
    elif not user.positionTitle and user.role:
        user.positionTitle = f"{user.role.replace('_', ' ').title()} Intern"

    now_ms = int(time.time() * 1000)
    # Notify the user
    db.add(models.Notification(
        recipientId=user.id,
        senderId=reviewer_id,
        senderName="System Administration",
        title="Account Approved",
        message="Your account registration has been approved! You now have full access to your assigned 14-day sprint tasks.",
        link="/intern",
        isRead=False,
        createdAt=now_ms
    ))

    log_activity(db, "USER", str(user.id), "APPROVED", reviewer_id, "Administrator", f"Approved user account for {user.name} ({user.email}) as {user.positionTitle}")
    db.commit()
    db.refresh(user)
    return user

@router.post("/users/{user_id}/reject")
def reject_user_account(user_id: int, reviewer_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Rejects a user registration."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.accountStatus = "REJECTED"
    log_activity(db, "USER", str(user.id), "REJECTED", reviewer_id, "Administrator", f"Rejected user account for {user.name} ({user.email})")
    db.commit()
    return {"message": f"Account for {user.name} was rejected."}

# ==========================================
# 5. NOTIFICATIONS & AUDIT TRAIL ENDPOINTS
# ==========================================

@router.get("/notifications", response_model=List[schemas.NotificationResponse])
def get_user_notifications(recipient_id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = recipient_id or user_id
    if not target_id:
        return []
    return db.query(models.Notification).filter(models.Notification.recipientId == target_id).order_by(models.Notification.createdAt.desc()).limit(40).all()

@router.put("/notifications/{notif_id}/read")
def mark_notification_read(notif_id: int, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notif_id).first()
    if notif:
        notif.isRead = True
        db.commit()
    return {"status": "success"}

@router.put("/notifications/read-all")
def mark_all_notifications_read(recipient_id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    target_id = recipient_id or user_id
    if target_id:
        db.query(models.Notification).filter(models.Notification.recipientId == target_id).update(
            {models.Notification.isRead: True}, 
            synchronize_session=False
        )
        db.commit()
    return {"status": "success"}

@router.get("/audit-logs", response_model=List[schemas.ActivityLogResponse])
def get_audit_trail(entity_type: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(models.ActivityLog)
    if entity_type: query = query.filter(models.ActivityLog.entityType == entity_type)
    logs = query.order_by(models.ActivityLog.timestamp.desc()).limit(limit).all()
    result = []
    for l in logs:
        d = schemas.ActivityLogResponse.model_validate(l).model_dump()
        d["createdAt"] = l.timestamp
        d["actorName"] = l.userName or "System"
        result.append(schemas.ActivityLogResponse(**d))
    return result
