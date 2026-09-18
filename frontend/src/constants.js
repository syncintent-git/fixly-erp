/**
 * Application Constants & Single Source of Truth
 */

export const APP_VERSION = 'v2.4.0'
export const APP_NAME = 'Fixly Office'
export const APP_FULL_NAME = 'Fixly Enterprise Office'
export const APP_COPYRIGHT = '© 2026 Fixly Services · Powered by SyncIntent'

export const ROLE_TITLES = {
  ceo: 'Chief Executive Officer',
  cto: 'Chief Technology Officer',
  coo: 'Chief Operating Officer',
  cfo: 'Chief Financial Officer',
  cmo: 'Chief Marketing Officer',
  cdc: 'CDC Head',
  mentor: 'Program Head / Mentor',
  scrum_head: 'Scrum Head',
  frontend_developer: 'Frontend Intern',
  backend_developer: 'Backend Intern',
  devops_developer: 'DevOps Intern',
  admin: 'System Administrator',
  viewer: 'Executive Viewer',
  intern: 'Intern'
}

export const formatRoleTitle = (role, customTitle = null) => {
  if (customTitle && customTitle.trim()) return customTitle.trim()
  if (!role) return 'Guest'
  const r = role.toLowerCase().trim()
  if (ROLE_TITLES[r]) return ROLE_TITLES[r]
  return role.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

export const INTERN_TRACKS = [
  { 
    id: 'frontend_developer', 
    title: 'Frontend Developer Intern', 
    description: 'Vue 3, Tailwind CSS, UI/UX Components'
  },
  { 
    id: 'backend_developer', 
    title: 'Backend Developer Intern', 
    description: 'FastAPI, Python, SQLAlchemy, REST APIs'
  },
  { 
    id: 'devops_developer', 
    title: 'DevOps Developer Intern', 
    description: 'CI/CD, Docker, Cloud Deployments, Health Monitoring'
  }
]

export const ROLE_PERMISSIONS = {
  ADMIN_ROLES: ['admin', 'ceo', 'cto', 'mentor', 'cdc', 'coo', 'cfo', 'cmo', 'viewer'],
  VIEW_ONLY_ROLES: ['cdc', 'mentor', 'viewer', 'cfo', 'cmo'],
  SCRUM_MANAGE_ROLES: ['scrum_head', 'admin', 'ceo', 'cto', 'coo'],
  INTERN_ROLES: ['frontend_developer', 'backend_developer', 'devops_developer', 'intern', 'student', 'user']
}
