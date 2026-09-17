<template>
  <div class="min-h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-zinc-700 selection:text-white flex flex-col w-full">
    
    <!-- Top Consolidated Global Navbar (Desktop & Mobile) -->
    <ScrumNavbar @toggle-sidebar="mobileDrawerOpen = !mobileDrawerOpen" />

    <!-- Reviewer Oversight Mode Alert for CDC / Program Head / Mentor -->
    <div v-if="authStore.isViewOnly" class="bg-zinc-900/90 border-b border-zinc-800 px-4 sm:px-6 py-2 text-xs text-zinc-300">
      <div class="w-full flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded bg-amber-400 shrink-0"></span>
          <p>
            <strong class="text-zinc-100">Reviewer Mode:</strong> Logged in as <span class="text-white font-medium">{{ authStore.user?.positionTitle || 'CDC / Program Head' }}</span>. Full view privileges across sprints, attendance records, audit logs, and proposals. Approval actions are restricted to administrators.
          </p>
        </div>
        <span class="bg-zinc-800 text-zinc-300 border border-zinc-700 text-[10px] font-bold uppercase px-2 py-0.5 rounded shrink-0">
          View Only
        </span>
      </div>
    </div>

    <!-- Mobile Horizontal Subtask Quick-Strip (Single-tap switching between sub-pages on mobile, strictly hidden on any dashboard) -->
    <div v-if="!isDashboard" class="md:hidden bg-zinc-900/60 border-b border-zinc-800/80 px-3 py-2 overflow-x-auto no-scrollbar flex items-center gap-1.5 shrink-0">
      <router-link
        v-for="sub in currentSubroutes"
        :key="sub.to"
        :to="sub.to"
        :class="[
          'px-2.5 py-1 rounded-lg text-xs whitespace-nowrap flex items-center gap-1.5 transition-all shrink-0',
          isActive(sub.to)
            ? 'bg-zinc-800 text-white font-bold border border-orange-500/50 shadow-sm'
            : 'text-zinc-400 hover:text-zinc-200 bg-zinc-950/40 border border-zinc-800/60'
        ]">
        <span v-if="isActive(sub.to)" class="w-1.5 h-1.5 rounded-full bg-orange-500 shrink-0"></span>
        <span>{{ sub.shortLabel || sub.label }}</span>
        <span 
          v-if="sub.badge && sub.badge > 0" 
          class="text-[9px] font-mono px-1 py-0.1 rounded bg-orange-500 text-black font-black">
          {{ sub.badge }}
        </span>
      </router-link>
    </div>

    <!-- Main Section Shell with Full-Width Content (Sidebar strictly excluded on any dashboard) -->
    <div class="flex-1 flex w-full">
      
      <!-- Left Dynamic Sidebar (Desktop: always visible on md+ screens, strictly hidden on any dashboard) -->
      <aside 
        v-if="!isDashboard" 
        :class="[
          'hidden md:block shrink-0 transition-all duration-300 relative sticky top-[49px] h-[calc(100vh-49px)] z-30',
          isSidebarPinned ? 'w-64' : 'w-16'
        ]">
        <SidebarNav 
          :is-pinned="isSidebarPinned" 
          @toggle-pin="toggleSidebarPin" 
        />
      </aside>

      <!-- Mobile Slide-Over Drawer Nav (Strictly disabled on any dashboard) -->
      <MobileDrawerNav 
        v-if="!isDashboard"
        :is-open="mobileDrawerOpen && !isDashboard" 
        @close="mobileDrawerOpen = false" 
      />

      <!-- Subtask / Dashboard Content Area: Spans 100% of remaining width (full width on dashboard) -->
      <main class="flex-1 min-w-0 p-3 sm:p-4 md:p-6 pb-28 md:pb-6 w-full flex flex-col justify-between">
        <div :class="[isDashboard ? 'max-w-7xl mx-auto w-full' : 'w-full', 'flex-1']">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
        
        <!-- Global Persistent Footer -->
        <AppFooter />
      </main>

    </div>

    <!-- Mobile Bottom Pill Navigation (Floats above content on mobile, hidden on desktop) -->
    <MobileBottomNav 
      :drawer-open="mobileDrawerOpen" 
      @toggle-drawer="mobileDrawerOpen = !mobileDrawerOpen" 
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useScrumStore } from '../stores/scrum'
import ScrumNavbar from '../components/ScrumNavbar.vue'
import SidebarNav from '../components/SidebarNav.vue'
import MobileBottomNav from '../components/MobileBottomNav.vue'
import MobileDrawerNav from '../components/MobileDrawerNav.vue'
import AppFooter from '../components/AppFooter.vue'

const route = useRoute()
const authStore = useAuthStore()
const scrumStore = useScrumStore()

const mobileDrawerOpen = ref(false)

// Desktop Sidebar Pin State (persisted in localStorage, default false / contracted)
const isSidebarPinned = ref(localStorage.getItem('fixly_sidebar_pinned') === 'true')

const toggleSidebarPin = () => {
  isSidebarPinned.value = !isSidebarPinned.value
  localStorage.setItem('fixly_sidebar_pinned', String(isSidebarPinned.value))
}

// Global keyboard shortcut: Ctrl+B / Cmd+B to toggle sidebar pin
const handleKeyDown = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key?.toLowerCase() === 'b') {
    const tag = e.target?.tagName?.toLowerCase()
    if (tag !== 'input' && tag !== 'textarea') {
      e.preventDefault()
      toggleSidebarPin()
    }
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

const isActive = (path) => {
  return route.path === path
}

const currentSection = computed(() => {
  if (route.path.startsWith('/dashboard')) return 'dashboard'
  if (route.path.startsWith('/scrum')) return 'scrum'
  if (route.path.startsWith('/workforce')) return 'workforce'
  if (route.path.startsWith('/operations')) return 'operations'
  if (route.path.startsWith('/admin')) return 'admin'
  return 'dashboard'
})

const isDashboard = computed(() => {
  return route.path === '/dashboard' || 
         route.path.startsWith('/dashboard/') || 
         route.meta?.section === 'dashboard' || 
         route.meta?.noSidebar === true ||
         currentSection.value === 'dashboard'
})

const pendingApprovalsCount = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'PENDING_APPROVAL').length
})

const pendingUsersCount = computed(() => {
  return scrumStore.pendingUsers.length
})

const currentSubroutes = computed(() => {
  switch (currentSection.value) {
    case 'dashboard':
      return [
        { to: '/dashboard', label: 'Role Overview', shortLabel: 'Overview' },
        { to: '/scrum/active-sprint', label: 'Active Sprint Board', shortLabel: 'Sprint' },
        { to: '/workforce/daily-log', label: 'Daily Work Log', shortLabel: 'Daily Log' }
      ]
    case 'scrum': {
      const items = [
        { to: '/scrum/active-sprint', label: 'Active Sprint & Board', shortLabel: 'Active Sprint' },
        { to: '/scrum/stories', label: 'User Stories Backlog', shortLabel: 'Stories' },
        { to: '/scrum/sprints', label: 'Sprint Planner & History', shortLabel: 'Sprints' }
      ]
      if (authStore.canManageScrum || authStore.canAccessAdmin) {
        items.push(
          { to: '/scrum/reviews', label: 'Task Review Queue', shortLabel: 'Review Queue', badge: pendingApprovalsCount.value },
          { to: '/scrum/team', label: 'Intern Workload Matrix', shortLabel: 'Workload' }
        )
      }
      return items
    }
    case 'workforce':
      return [
        { to: '/workforce/daily-log', label: 'Daily Work Log', shortLabel: 'Daily Log' },
        { to: '/workforce/attendance', label: 'Attendance & Records', shortLabel: 'Attendance' },
        { to: '/workforce/feed', label: 'Department Feed', shortLabel: 'Company Feed' }
      ]
    case 'operations':
      return [
        { to: '/operations/mom', label: 'Meeting Minutes (MoM)', shortLabel: 'MoM' },
        { to: '/operations/proposals', label: 'Improvement Proposals', shortLabel: 'Proposals' },
        { to: '/operations/calendar', label: 'Company Calendar', shortLabel: 'Calendar' }
      ]
    case 'admin':
      return [
        { to: '/admin/access-requests', label: 'Access Requests', shortLabel: 'Requests', badge: pendingUsersCount.value },
        { to: '/admin/users', label: 'Users & Teams', shortLabel: 'Personnel' },
        { to: '/admin/audit', label: 'Audit Trail', shortLabel: 'Audit' },
        { to: '/admin/reports', label: 'Executive Reports', shortLabel: 'Reports' }
      ]
    default:
      return []
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
