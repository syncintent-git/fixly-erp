import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import MainLayout from '../layouts/MainLayout.vue'

// Scrum Hub subtasks
import ActiveSprintView from '../views/scrum/ActiveSprintView.vue'
import StoriesView from '../views/scrum/StoriesView.vue'
import SprintPlannerView from '../views/scrum/SprintPlannerView.vue'
import TaskReviewView from '../views/scrum/TaskReviewView.vue'
import TeamWorkloadView from '../views/scrum/TeamWorkloadView.vue'

// Workforce Hub subtasks
import DailyLogView from '../views/workforce/DailyLogView.vue'
import AttendanceView from '../views/workforce/AttendanceView.vue'
import CompanyFeedView from '../views/workforce/CompanyFeedView.vue'

// Operations Hub subtasks
import MomView from '../views/operations/MomView.vue'
import ProposalsView from '../views/operations/ProposalsView.vue'
import CalendarView from '../views/operations/CalendarView.vue'

// Admin Hub subtasks
import AccessRequestsView from '../views/admin/AccessRequestsView.vue'
import UserManagementView from '../views/admin/UserManagementView.vue'
import AuditTrailView from '../views/admin/AuditTrailView.vue'
import ReportsView from '../views/admin/ReportsView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { 
      path: '/', 
      redirect: () => {
        const auth = useAuthStore()
        return (auth.user && !auth.isPendingApproval) ? '/dashboard' : '/login'
      }
    },
    { path: '/login', component: LoginView },

    // 0. Role Command Center Dashboard
    {
      path: '/dashboard',
      component: MainLayout,
      meta: { requiresAuth: true, section: 'dashboard', noSidebar: true },
      children: [
        {
          path: '',
          name: 'role-dashboard',
          component: DashboardView,
          meta: { title: 'Role Command Center', requiresAuth: true, noSidebar: true }
        }
      ]
    },

    // 1. Scrum & Sprints Hub
    {
      path: '/scrum',
      component: MainLayout,
      meta: { requiresAuth: true, section: 'scrum' },
      children: [
        { path: '', redirect: '/scrum/active-sprint' },
        { 
          path: 'active-sprint', 
          name: 'scrum-active-sprint', 
          component: ActiveSprintView, 
          meta: { title: 'Active Sprint & Board', requiresAuth: true } 
        },
        { 
          path: 'stories', 
          name: 'scrum-stories', 
          component: StoriesView, 
          meta: { title: 'User Stories Backlog', requiresAuth: true } 
        },
        { 
          path: 'sprints', 
          name: 'scrum-sprints', 
          component: SprintPlannerView, 
          meta: { title: 'Sprint Planner & History', requiresAuth: true } 
        },
        { 
          path: 'reviews', 
          name: 'scrum-reviews', 
          component: TaskReviewView, 
          meta: { title: 'Task Review Queue', requiresAuth: true } 
        },
        { 
          path: 'team', 
          name: 'scrum-team', 
          component: TeamWorkloadView, 
          meta: { title: 'Intern Workload Matrix', requiresAuth: true } 
        }
      ]
    },

    // 2. Workforce Hub
    {
      path: '/workforce',
      component: MainLayout,
      meta: { requiresAuth: true, section: 'workforce' },
      children: [
        { path: '', redirect: '/workforce/daily-log' },
        { 
          path: 'daily-log', 
          name: 'workforce-daily-log', 
          component: DailyLogView, 
          meta: { title: 'Daily Work Log', requiresAuth: true } 
        },
        { 
          path: 'attendance', 
          name: 'workforce-attendance', 
          component: AttendanceView, 
          meta: { title: 'Attendance & Records', requiresAuth: true } 
        },
        { 
          path: 'feed', 
          name: 'workforce-feed', 
          component: CompanyFeedView, 
          meta: { title: 'Department Feed', requiresAuth: true } 
        }
      ]
    },

    // 3. Operations Hub
    {
      path: '/operations',
      component: MainLayout,
      meta: { requiresAuth: true, section: 'operations' },
      children: [
        { path: '', redirect: '/operations/mom' },
        { 
          path: 'mom', 
          name: 'operations-mom', 
          component: MomView, 
          meta: { title: 'Minutes of Meeting', requiresAuth: true } 
        },
        { 
          path: 'proposals', 
          name: 'operations-proposals', 
          component: ProposalsView, 
          meta: { title: 'Improvement Proposals', requiresAuth: true } 
        },
        { 
          path: 'calendar', 
          name: 'operations-calendar', 
          component: CalendarView, 
          meta: { title: 'Company Calendar', requiresAuth: true } 
        }
      ]
    },

    // 4. Executive & Admin Hub
    {
      path: '/admin',
      component: MainLayout,
      meta: { requiresAuth: true, requiresAdmin: true, section: 'admin' },
      children: [
        { path: '', redirect: '/admin/access-requests' },
        { 
          path: 'access-requests', 
          name: 'admin-access-requests', 
          component: AccessRequestsView, 
          meta: { title: 'Access Requests', requiresAuth: true, requiresAdmin: true } 
        },
        { 
          path: 'users', 
          name: 'admin-users', 
          component: UserManagementView, 
          meta: { title: 'Users & Teams', requiresAuth: true, requiresAdmin: true } 
        },
        { 
          path: 'teams', 
          redirect: '/admin/users?tab=teams' 
        },
        { 
          path: 'audit', 
          name: 'admin-audit', 
          component: AuditTrailView, 
          meta: { title: 'System Audit Trail', requiresAuth: true, requiresAdmin: true } 
        },
        { 
          path: 'reports', 
          name: 'admin-reports', 
          component: ReportsView, 
          meta: { title: 'Executive Reports', requiresAuth: true, requiresAdmin: true } 
        }
      ]
    },

    // Backward Compatibility Redirects
    { path: '/intern', redirect: '/dashboard' }
  ]
})

// Navigation Guard: Protect routes based on authentication and roles
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.user) {
    return next('/login')
  }

  // If user is pending approval, keep them on login screen
  if (auth.user && auth.isPendingApproval && to.path !== '/login') {
    return next('/login')
  }

  // If non-admin tries to access admin routes
  if (to.meta.requiresAdmin && !auth.canAccessAdmin) {
    return next('/dashboard')
  }

  if (to.path === '/login' && auth.user && !auth.isPendingApproval) {
    return next('/dashboard')
  }

  next()
})

export default router