# Fixly Services ERP · Agile Scrum & Workforce Platform

<div align="center">
  <img src="media/logo-w-text.png" alt="Fixly ERP Logo" width="320" />
  <p><strong>Enterprise Resource Planning, 14-Day Agile Scrum Cycles & Workforce Governance Suite</strong></p>
  <p><em>Powered by SyncIntent</em></p>
</div>

---

## Table of Contents
1. [Overview](#overview)
2. [Key Capabilities & Modules](#key-capabilities--modules)
3. [Role-Based Access Control (RBAC)](#role-based-access-control-rbac)
4. [Repository Structure](#repository-structure)
5. [Tech Stack](#tech-stack)
6. [Getting Started Locally](#getting-started-locally)
   - [Prerequisites](#prerequisites)
   - [Backend Setup (FastAPI)](#backend-setup-fastapi)
   - [Frontend Setup (Vue 3 + Vite)](#frontend-setup-vue-3--vite)
7. [API Endpoints Reference](#api-endpoints-reference)
8. [Evaluation Demo Accounts](#evaluation-demo-accounts)
9. [Design & UI Principles](#design--ui-principles)
10. [License & Attribution](#license--attribution)

---

## Overview

**Fixly ERP** is a full-stack enterprise platform purpose-built for agile project execution, workforce accountability, administrative governance, and executive oversight. Originally created for project tracking, Fixly ERP has expanded into a unified operating system supporting:

- **14-Day Agile Sprints**: End-to-end Scrum lifecycle from user stories to kanban task boards and peer QA reviews.
- **Workforce & Daily Accountability**: Daily work logs, automated attendance compliance tracking, and department achievement feeds.
- **Corporate Operations**: Minutes of Meeting (MoM) management, continuous improvement proposals, and corporate calendars.
- **Executive & Administrative Governance**: One-click onboarding approvals, comprehensive user & team management, immutable audit trails, and executive PDF reporting.
- **Role-Adaptive Command Center**: A balanced, high-signal dashboard (`/dashboard`) that customizes its KPIs, quick actions, and focus widgets based on the logged-in user's organizational role.

---

## Key Capabilities & Modules

### 1. Role Command Center (`/dashboard`)
- **Zero Sidebar Clutter**: Opens into a spacious, full-width interface designed to provide immediate clarity without cognitive overload.
- **Role-Adaptive Experience**:
  - **Interns / Developers**: Displays active assigned sprint tasks with 1-click status transitions (`Start Work`, `Submit Work`), attendance check-in status, and Sprint milestone progress.
  - **Scrum Head**: Highlights the urgent review queue (`PENDING_APPROVAL` tasks), sprint velocity breakdown, and team workload distribution.
  - **System Administrator**: Surfaces pending access requests with 1-click approval actions, real-time security audit events, and administration shortcuts.
  - **Executive & Reviewers**: Visualizes cross-department work delivery, attendance compliance rates, and 1-click executive PDF report downloads.

### 2. Scrum & Agile Delivery Hub (`/scrum`)
- **Active Sprint Board (`/scrum/active-sprint`)**: Multi-column Kanban board (`To Do`, `In Progress`, `Pending Approval`, `Approved / Done`) with story points, priority tags, and assignee filtering.
- **User Stories Backlog (`/scrum/stories`)**: Structured product backlog linking acceptance criteria to actionable engineering tasks.
- **Sprint Planner (`/scrum/sprints`)**: 14-day sprint planning cadence with velocity analytics and milestone archives.
- **Task Review Queue (`/scrum/reviews`)**: Dedicated inspection portal for Scrum Leads and QA to verify deliverables before marking work complete.
- **Intern Workload Matrix (`/scrum/team`)**: Live workload tracking to prevent team bottlenecks and ensure balanced task distribution.

### 3. Workforce Hub (`/workforce`)
- **Daily Work Log (`/workforce/daily-log`)**: Structured daily reporting linking work directly to active sprint tasks and quantifiable metrics.
- **Attendance & Records (`/workforce/attendance`)**: Monthly visual attendance calendar with compliance percentages and historical inspection.
- **Department Feed (`/workforce/feed`)**: Real-time cross-functional stream celebrating team completions, deployments, and updates.

### 4. Operations Hub (`/operations`)
- **Minutes of Meeting (`/operations/mom`)**: Formal meeting notes with rich-text transcription, agenda items, and assigned action deliverables.
- **Improvement Proposals (`/operations/proposals`)**: Innovation sandbox where team members propose process optimizations with peer upvoting.
- **Company Calendar (`/operations/calendar`)**: Institutional schedule containing sprint dates, holidays, and milestones.

### 5. Administrative & Governance Hub (`/admin`)
- **Identity & Access Requests (`/admin/access-requests`)**: Self-service onboarding approval queue with one-click role provisioning.
- **Users & Teams Management (`/admin/users`)**: Complete CRUD operations for personnel records, department assignments, and access levels.
- **System Audit Trail (`/admin/audit`)**: Security event log capturing logins, status transitions, role changes, and administrative actions.
- **Executive Reports (`/admin/reports`)**: On-demand generation of executive PDF summaries with attendance and sprint velocity charts.

---

## Role-Based Access Control (RBAC)

The application supports multiple distinct role archetypes with tailored permissions:

| Archetype | Roles | Key Privileges |
| :--- | :--- | :--- |
| **System Administrator** | `admin` | Full system control: user CRUD, team configuration, access approvals, audit logs, and reports. |
| **Executive Leadership** | `ceo`, `cto`, `coo`, `cfo`, `cmo` | High-level organizational oversight, department velocity review, attendance auditing, and reports. |
| **Academic / Institutional Reviewers** | `cdc`, `mentor`, `viewer` | Read-only inspection across all sprints, logs, meeting minutes, and proposals. Approval actions restricted. |
| **Scrum Head** | `scrum_head` | Sprint lifecycle management, backlog grooming, task assignment, review queue approvals, workload balancing. |
| **Engineering Interns** | `frontend_developer`, `backend_developer`, `devops_developer` | Active sprint task execution, status submission, daily work logging, and department feed interactions. |

---

## Repository Structure

```text
fixly-erp/project-tracker/
├── backend/                             # FastAPI Backend Service
│   ├── app/
│   │   ├── main.py                      # Application bootstrap, CORS & router registration
│   │   ├── database.py                  # SQLAlchemy engine & session management
│   │   ├── models.py                    # Relational database models (Users, Sprints, Tasks, etc.)
│   │   ├── schemas.py                   # Pydantic request/response validation schemas
│   │   ├── seed_data.py                 # Initial seed dataset (leadership, Sprint 07, default teams)
│   │   └── routers/
│   │       ├── auth.py                  # Google OAuth, onboarding, and 1-click evaluation access
│   │       ├── scrum.py                 # Sprints, stories, tasks, review queue & workload endpoints
│   │       ├── users.py                 # User CRUD, role assignments & team management
│   │       ├── teams.py                 # Department and team management endpoints
│   │       ├── logs.py                  # Daily logs & attendance recording
│   │       ├── mom.py                   # Minutes of Meeting & improvement proposals
│   │       └── holidays.py              # Calendar schedule & holiday endpoints
│   ├── requirements.txt                 # Python dependencies
│   ├── sql_app.db                       # Local SQLite database (pre-seeded)
│   └── tests/                           # API validation and CRUD test scripts
│
├── frontend/                            # Vue 3 Single Page Application (SPA)
│   ├── public/
│   │   ├── favicon.svg                  # Fixly SVG icon
│   │   ├── logo.png                     # Fixly shield mark
│   │   └── logo-w-text.png              # Extended Fixly brand asset
│   ├── src/
│   │   ├── App.vue                      # Root Vue component
│   │   ├── main.js                      # App initialization with Pinia & Vue Router
│   │   ├── style.css                    # Tailwind CSS 4 directives & global design tokens
│   │   ├── layouts/
│   │   │   └── MainLayout.vue           # Global layout shell (Navbar, Footer, dynamic aside, responsive drawer)
│   │   ├── components/
│   │   │   ├── ScrumNavbar.vue          # Global brand header, hub navigation, role switcher & alerts
│   │   │   ├── SidebarNav.vue           # Contextual sub-navigation sidebar for detailed hubs
│   │   │   ├── MobileBottomNav.vue      # Floating bottom navigation pill for mobile devices
│   │   │   ├── MobileDrawerNav.vue      # Responsive slide-over drawer menu
│   │   │   └── AppFooter.vue            # Subtle persistent footer across all authenticated views
│   │   ├── stores/
│   │   │   ├── auth.js                  # Pinia store for authentication, RBAC & user session
│   │   │   └── scrum.js                 # Pinia store for sprints, tasks, review queues & notifications
│   │   ├── router/
│   │   │   └── index.js                 # Vue Router configuration with RBAC navigation guards
│   │   └── views/
│   │       ├── DashboardView.vue        # Full-width role-adaptive command center
│   │       ├── LoginView.vue            # Multi-mode login portal (Google, 1-click roles, credentials)
│   │       ├── scrum/                   # Agile & Scrum sub-views (ActiveSprint, Backlog, Reviews, Team)
│   │       ├── workforce/               # Workforce sub-views (DailyLog, Attendance, Feed)
│   │       ├── operations/              # Operations sub-views (MoM, Proposals, Calendar)
│   │       └── admin/                   # Admin sub-views (AccessRequests, Users, Audit, Reports)
│   ├── package.json                     # Frontend dependencies and build scripts
│   ├── vite.config.js                   # Vite bundler configuration
│   └── tailwind.config.js               # Tailwind CSS theme extension
│
├── media/                               # Original brand media assets
│   ├── logo.png                         # Fixly shield logo
│   └── logo-w-text.png                  # Fixly shield with typography
│
└── README.md                            # Comprehensive project documentation
```

---

## Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Database / ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) with SQLite (local development) and PostgreSQL / Supabase compatibility
- **Server**: [Uvicorn](https://www.uvicorn.org/) ASGI server
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Security**: Passlib (Bcrypt) password hashing, CORS middleware

### Frontend
- **Framework**: [Vue 3](https://vuejs.org/) (Composition API with `<script setup>`)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **State Management**: [Pinia](https://pinia.vuejs.org/)
- **Routing**: [Vue Router 4](https://router.vuejs.org/) with dynamic RBAC navigation guards
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/) with curated Dark & Orange enterprise theme
- **Rich Text & Reports**: [VueQuill](https://vueup.github.io/vue-quill/) & [jsPDF](https://github.com/parallax/jsPDF)

---

## Getting Started Locally

### Prerequisites
- **Node.js**: v18.0 or higher
- **Python**: v3.10 or higher
- **Git**

---

### Backend Setup (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   *The database (`sql_app.db`) will initialize automatically with Sprint 07, preconfigured teams, and leadership accounts on first boot.*

5. Verify backend health:
   - Interactive Swagger API docs: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/`

---

### Frontend Setup (Vue 3 + Vite)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure environment variables (optional, defaults to `http://localhost:8000`):
   Create or verify `.env` in `frontend/`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. Start the Vite development server:
   ```bash
   npm run dev
   ```

5. Open the application in your browser:
   ```text
   http://localhost:5173
   ```

---

## API Endpoints Reference

Interactive documentation is available at `http://localhost:8000/docs`. Key endpoint groupings include:

| Domain | Route | Method | Description |
| :--- | :--- | :--- | :--- |
| **Auth** | `/api/auth/google` | `POST` | Process Google sign-in payload and resolve user role |
| **Auth** | `/api/auth/demo` | `POST` | Instant one-click demo login for evaluation |
| **Auth** | `/api/auth/onboard-role` | `POST` | Submit self-service onboarding request for approval |
| **Auth** | `/api/auth/pending-approvals` | `GET` | Retrieve pending user access requests (Admin only) |
| **Auth** | `/api/auth/approve-user/{user_id}` | `POST` | Approve pending user and assign active status |
| **Scrum** | `/api/scrum/sprints/active` | `GET` | Fetch active 14-day sprint and metrics |
| **Scrum** | `/api/scrum/tasks` | `GET` / `POST` | List and create sprint tasks |
| **Scrum** | `/api/scrum/tasks/{id}/status` | `PUT` | Transition task status (`TODO`, `IN_PROGRESS`, `PENDING_APPROVAL`, `DONE`) |
| **Scrum** | `/api/scrum/tasks/{id}/approve` | `POST` | Approve deliverable from QA review queue |
| **Scrum** | `/api/scrum/workload` | `GET` | Calculate workload and task distribution across members |
| **Workforce** | `/api/logs/` | `GET` / `POST` | Fetch and submit daily work logs |
| **Workforce** | `/api/logs/attendance` | `GET` | Fetch team attendance compliance matrix |
| **Operations** | `/api/mom/` | `GET` / `POST` | Manage Minutes of Meeting |
| **Operations** | `/api/mom/proposals` | `GET` / `POST` | Submit and vote on improvement proposals |
| **Admin** | `/api/users/` | `GET` / `POST` | Full user CRUD management |
| **Admin** | `/api/teams/` | `GET` / `POST` | Team and department management |
| **Admin** | `/api/scrum/audit-logs` | `GET` | Retrieve system security and operation event log |

---

## Evaluation Demo Accounts

To test the role-adaptive experience, the login screen (`/login`) provides **1-Click Role Access** buttons:

| Name | Role Key | Title | Focus View |
| :--- | :--- | :--- | :--- |
| **Abhijeet** | `ceo` | Chief Executive Officer | Workforce Deliverables & Delivery Index |
| **Karthik** | `cto` | Chief Technology Officer | Engineering Metrics & System Stability |
| **Nishanth** | `coo` | Chief Operating Officer | Operations, MoM & Department Cadence |
| **Dhanya** | `cfo` | Chief Financial Officer | Executive Review & Oversight |
| **Anju Vaishnavi** | `cmo` | Chief Marketing Officer | Cross-Team Feed & Deliverables |
| **Scrum Head** | `scrum_head` | Lead Scrum Head | Urgent Review Queue & Sprint Velocity |
| **Alex Carter** | `frontend_developer` | Frontend Developer Intern | Active Sprint Tasks & Today's Attendance |
| **Priya Patel** | `backend_developer` | Backend Developer Intern | Active Sprint Tasks & Today's Attendance |
| **David Kim** | `devops_developer` | DevOps Developer Intern | Active Sprint Tasks & Today's Attendance |
| **Rohit Sir** | `mentor` | Program Head / Mentor | Academic Reviewer Mode (Read-Only) |
| **CDC Head** | `cdc` | Career Development Center | Academic Reviewer Mode (Read-Only) |
| **System Admin** | `admin` | System Administrator | Access Requests, User Management & Audit |

---

## Design & UI Principles

1. **Curated Palette**:
   - Backgrounds: Deep graphite and obsidian (`#09090b` / `zinc-950`, `#18181b` / `zinc-900`).
   - Accents: Vibrant Fixly orange (`#f97316` / `orange-500`) for primary actions and active indicators.
   - Typography: Clean sans-serif pairings with monospace accents for task IDs (`SPR-07-01`), dates, and metrics.
2. **Dynamic Responsiveness**:
   - Desktop screens benefit from contextual aside sidebars on detailed subtask pages.
   - All dashboard views (`/dashboard`) remain completely free of sidebars, spanning full-width for maximum clarity.
   - Mobile users enjoy touch-friendly bottom pill navigation and slide-over navigation drawers.
3. **Subtle Enterprise Footer**:
   - Every view features a clean, single-line footer: `© 2026 Fixly Services · Powered by SyncIntent`.

---

## License & Attribution

```text
© 2026 Fixly Services. All rights reserved.
Powered by SyncIntent.
```
