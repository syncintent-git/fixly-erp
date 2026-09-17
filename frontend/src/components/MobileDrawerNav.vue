<template>
  <div v-if="isOpen" class="md:hidden fixed inset-0 z-50 overflow-hidden">
    
    <!-- Backdrop Overlay -->
    <div 
      class="fixed inset-0 bg-black/75 backdrop-blur-sm transition-opacity"
      @click="$emit('close')">
    </div>

    <!-- Slide-Over Drawer Sheet (From Left) -->
    <div class="fixed inset-y-0 left-0 max-w-[85vw] w-72 sm:w-80 bg-zinc-950 border-r border-zinc-800 shadow-2xl z-50 flex flex-col justify-between overflow-y-auto animate-in slide-in-from-left duration-200">
      
      <!-- Top Section -->
      <div class="p-4 space-y-4">
        
        <!-- Header: Fixly Brand & Close Button -->
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800/80">
          <div class="flex items-center gap-2">
            <img src="/logo-w-text.png" alt="Fixly Office" class="h-6 w-auto object-contain" />
            <span class="text-[9px] font-mono uppercase tracking-wider text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded-full border border-orange-500/30 font-bold">Office</span>
          </div>

          <button 
            @click="$emit('close')"
            class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 transition-colors cursor-pointer"
            title="Close menu">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Section Identity Banner -->
        <div class="p-2.5 rounded-lg bg-zinc-900/80 border border-zinc-800/80 flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0">
            <span v-html="sectionMeta.icon"></span>
          </div>
          <div class="overflow-hidden">
            <h2 class="text-xs font-bold uppercase tracking-wider text-white truncate">{{ sectionMeta.title }}</h2>
            <p class="text-[10px] text-zinc-400 truncate">{{ sectionMeta.subtitle }}</p>
          </div>
        </div>

        <!-- Quick Hub Switcher Strip (Allows jumping to other hubs) -->
        <div class="space-y-1.5">
          <div class="text-[10px] font-mono uppercase tracking-wider text-zinc-500 px-1">
            Switch Hub
          </div>

          <!-- Dashboard Quick Hub Button -->
          <button 
            @click="navigateToHub('/dashboard')"
            :class="[
              'w-full p-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-colors text-left border cursor-pointer mb-1.5',
              isCurrentHub('dashboard')
                ? 'bg-orange-500 text-black border-orange-400 font-bold shadow-sm'
                : 'bg-zinc-900/70 text-zinc-300 border-zinc-800 hover:bg-zinc-800 hover:text-white'
            ]">
            <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/></svg>
            <span class="truncate">Role Dashboard (Overview)</span>
          </button>

          <div class="grid grid-cols-2 gap-1.5">
            <button 
              @click="navigateToHub('/scrum')"
              :class="[
                'p-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors text-left border cursor-pointer',
                isCurrentHub('scrum')
                  ? 'bg-orange-500 text-black border-orange-400 font-bold shadow-sm'
                  : 'bg-zinc-900/70 text-zinc-300 border-zinc-800 hover:bg-zinc-800 hover:text-white'
              ]">
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
              <span class="truncate">Scrum</span>
            </button>

            <button 
              @click="navigateToHub('/workforce')"
              :class="[
                'p-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors text-left border cursor-pointer',
                isCurrentHub('workforce')
                  ? 'bg-orange-500 text-black border-orange-400 font-bold shadow-sm'
                  : 'bg-zinc-900/70 text-zinc-300 border-zinc-800 hover:bg-zinc-800 hover:text-white'
              ]">
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              <span class="truncate">Workforce</span>
            </button>

            <button 
              @click="navigateToHub('/operations')"
              :class="[
                'p-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors text-left border cursor-pointer',
                isCurrentHub('operations')
                  ? 'bg-orange-500 text-black border-orange-400 font-bold shadow-sm'
                  : 'bg-zinc-900/70 text-zinc-300 border-zinc-800 hover:bg-zinc-800 hover:text-white'
              ]">
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
              <span class="truncate">Operations</span>
            </button>

            <button 
              v-if="authStore.canAccessAdmin"
              @click="navigateToHub('/admin')"
              :class="[
                'p-2 rounded-lg text-xs font-semibold flex items-center justify-between gap-1.5 transition-colors text-left border cursor-pointer',
                isCurrentHub('admin')
                  ? 'bg-orange-500 text-black border-orange-400 font-bold shadow-sm'
                  : 'bg-zinc-900/70 text-zinc-300 border-zinc-800 hover:bg-zinc-800 hover:text-white'
              ]">
              <div class="flex items-center gap-1.5 truncate">
                <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                <span class="truncate">{{ authStore.isViewOnly ? 'Review' : 'Admin' }}</span>
              </div>
              <span 
                v-if="scrumStore.pendingUsers.length > 0"
                class="text-[9px] font-mono px-1 rounded bg-orange-500 text-black font-black">
                {{ scrumStore.pendingUsers.length }}
              </span>
            </button>
          </div>
        </div>

        <!-- Subtasks List for Current Section -->
        <div class="space-y-1 pt-2">
          <div class="flex items-center justify-between px-1 pb-1">
            <span class="text-[10px] font-mono uppercase tracking-wider text-zinc-500">
              {{ sectionMeta.title }} Subtasks
            </span>
            <span class="text-[10px] font-mono text-zinc-500">{{ currentNavItems.length }} Views</span>
          </div>

          <router-link
            v-for="item in currentNavItems"
            :key="item.to"
            :to="item.to"
            @click="$emit('close')"
            :class="[
              'group flex items-center justify-between px-3 py-2.5 rounded-lg text-xs transition-all',
              isActive(item.to)
                ? 'bg-zinc-900 text-white font-bold border-l-2 border-orange-500 border-t border-r border-b border-zinc-800 shadow-sm'
                : 'text-zinc-400 hover:text-white hover:bg-zinc-900 border border-transparent'
            ]">
            <div class="flex items-center gap-2.5 min-w-0">
              <span 
                class="shrink-0 transition-colors" 
                :class="isActive(item.to) ? 'text-orange-400' : 'text-zinc-500 group-hover:text-zinc-200'"
                v-html="item.icon">
              </span>
              <span class="truncate font-medium">{{ item.label }}</span>
            </div>

            <span 
              v-if="item.badge && item.badge > 0"
              class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500 text-black font-bold min-w-[18px] text-center leading-none inline-flex items-center justify-center shrink-0 shadow-sm">
              {{ item.badge }}
            </span>
          </router-link>
        </div>

      </div>

      <!-- Bottom User Profile & Quick Actions Block -->
      <div class="p-4 border-t border-zinc-800/80 bg-zinc-900/40 space-y-3">
        
        <!-- User identity -->
        <div class="p-2.5 bg-zinc-900 rounded-lg border border-zinc-800">
          <div class="flex items-center justify-between text-xs">
            <span class="text-white font-bold truncate">{{ authStore.user?.name || 'User' }}</span>
            <span class="text-[10px] font-mono text-orange-400 uppercase font-bold">{{ authStore.user?.role || 'Guest' }}</span>
          </div>
          <div class="mt-1 flex items-center justify-between text-[10px] text-zinc-400 font-mono">
            <span>{{ authStore.user?.positionTitle || authStore.user?.team || 'Intern' }}</span>
          </div>
        </div>

        <!-- Role Switcher Expandable -->
        <div class="space-y-1.5">
          <button 
            @click="showRoleList = !showRoleList"
            class="w-full bg-zinc-900 hover:bg-zinc-850 text-zinc-200 hover:text-white px-3 py-2 rounded-lg border border-zinc-800 text-xs font-medium flex items-center justify-between transition-colors cursor-pointer">
            <div class="flex items-center gap-2">
              <svg class="w-3.5 h-3.5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/></svg>
              <span>Switch Evaluation Role</span>
            </div>
            <svg :class="['w-3.5 h-3.5 text-zinc-400 transition-transform', showRoleList ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </button>

          <!-- Dropdown of Roles -->
          <div v-if="showRoleList" class="bg-zinc-900 border border-zinc-800 rounded-lg p-1.5 space-y-1 max-h-52 overflow-y-auto">
            <button 
              v-for="roleItem in DEMO_ROLES" 
              :key="roleItem.role"
              @click="onRoleSelect(roleItem)"
              class="w-full text-left px-2.5 py-1.5 rounded text-xs flex items-center justify-between hover:bg-zinc-800 transition-colors cursor-pointer group">
              <div>
                <p class="font-medium text-zinc-200 group-hover:text-white">{{ roleItem.name }}</p>
                <p class="text-[9px] text-zinc-400">{{ roleItem.title }}</p>
              </div>
              <span class="text-[9px] font-mono px-1 rounded bg-orange-500/10 border border-orange-500/30 text-orange-400 font-bold">
                {{ roleItem.tag }}
              </span>
            </button>
          </div>
        </div>

        <!-- Theme Toggle Button -->
        <button 
          @click="themeStore.toggleTheme"
          type="button"
          class="w-full bg-zinc-900/80 hover:bg-zinc-800 text-zinc-300 hover:text-white px-3 py-2 rounded-lg border border-zinc-800 transition-colors text-xs font-medium cursor-pointer flex items-center justify-between gap-1.5">
          <div class="flex items-center gap-2">
            <svg v-if="themeStore.isDark" class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <span>Theme Mode</span>
          </div>
          <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 border border-zinc-700">
            {{ themeStore.isDark ? 'Dark' : 'Light' }}
          </span>
        </button>

        <!-- Sign Out Button -->
        <button 
          @click="handleLogout"
          class="w-full bg-zinc-900/80 hover:bg-red-950/40 text-zinc-400 hover:text-red-300 hover:border-red-800/40 px-3 py-2 rounded-lg border border-zinc-800 transition-colors text-xs font-medium cursor-pointer flex items-center justify-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
          <span>Sign Out</span>
        </button>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useScrumStore } from '../stores/scrum'
import { useThemeStore } from '../stores/theme'

defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const scrumStore = useScrumStore()
const themeStore = useThemeStore()

const showRoleList = ref(false)

const DEMO_ROLES = [
  { role: 'ceo', name: 'Abhijeet', title: 'Chief Executive Officer', tag: 'Admin' },
  { role: 'cto', name: 'Karthik', title: 'Chief Technology Officer', tag: 'Admin' },
  { role: 'coo', name: 'Nishanth', title: 'Chief Operating Officer', tag: 'Executive' },
  { role: 'cfo', name: 'Dhanya', title: 'Chief Financial Officer', tag: 'Executive' },
  { role: 'cmo', name: 'Anju Vaishnavi', title: 'Chief Marketing Officer', tag: 'Executive' },
  { role: 'cdc', name: 'CDC Head', title: 'Career Development Center', tag: 'Reviewer' },
  { role: 'mentor', name: 'Rohit Sir', title: 'Program Head / Mentor', tag: 'Reviewer' },
  { role: 'scrum_head', name: 'Scrum Lead', title: 'Lead Scrum Head', tag: 'Scrum Lead' },
  { role: 'frontend_developer', name: 'Frontend Intern', title: 'Frontend Developer Intern', tag: 'Intern' },
  { role: 'backend_developer', name: 'Backend Intern', title: 'Backend Developer Intern', tag: 'Intern' },
  { role: 'devops_developer', name: 'DevOps Intern', title: 'DevOps Developer Intern', tag: 'Intern' },
  { role: 'viewer', name: 'Executive Viewer', title: 'Executive Read-Only Reviewer', tag: 'Reviewer' },
  { role: 'admin', name: 'System Admin', title: 'System Administrator', tag: 'Admin' }
]

const currentSection = computed(() => {
  if (route.path.startsWith('/dashboard')) return 'dashboard'
  if (route.path.startsWith('/scrum')) return 'scrum'
  if (route.path.startsWith('/workforce')) return 'workforce'
  if (route.path.startsWith('/operations')) return 'operations'
  if (route.path.startsWith('/admin')) return 'admin'
  return 'dashboard'
})

const isCurrentHub = (hub) => {
  return currentSection.value === hub
}

const isActive = (path) => {
  return route.path === path
}

const navigateToHub = (path) => {
  router.push(path)
  emit('close')
}

const onRoleSelect = async (item) => {
  showRoleList.value = false
  const ok = await authStore.demoLogin(item.role)
  if (ok) {
    router.push('/dashboard')
    if (authStore.user?.id) {
      scrumStore.fetchNotifications(authStore.user.id)
    }
  }
  emit('close')
}

const handleLogout = async () => {
  await authStore.logout()
  emit('close')
  router.push('/login')
}

const pendingApprovalsCount = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'PENDING_APPROVAL').length
})

const pendingUsersCount = computed(() => {
  return scrumStore.pendingUsers.length
})

const sectionMeta = computed(() => {
  switch (currentSection.value) {
    case 'dashboard':
      return {
        title: 'Role Dashboard',
        subtitle: `${authStore.user?.role?.toUpperCase() || 'ROLE'} OVERVIEW`,
        icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/></svg>'
      }
    case 'scrum':
      return {
        title: 'Scrum & Sprints',
        subtitle: '14-Day Agile Cycles',
        icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>'
      }
    case 'workforce':
      return {
        title: 'Workforce Hub',
        subtitle: 'Daily Logs & Attendance',
        icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>'
      }
    case 'operations':
      return {
        title: 'Operations',
        subtitle: 'MoM, Proposals & Calendar',
        icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>'
      }
    case 'admin':
      return {
        title: authStore.isViewOnly ? 'Reviewer Console' : 'Administration',
        subtitle: 'Oversight, Access & Audit',
        icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>'
      }
    default:
      return { title: 'Navigation', subtitle: '', icon: '' }
  }
})

const currentNavItems = computed(() => {
  switch (currentSection.value) {
    case 'dashboard': {
      const items = [
        {
          to: '/dashboard',
          label: 'Role Dashboard Overview',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/></svg>'
        },
        {
          to: '/scrum/active-sprint',
          label: 'Active Sprint Board',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>'
        },
        {
          to: '/workforce/daily-log',
          label: 'Daily Work Log',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>'
        }
      ]
      if (authStore.canManageScrum || authStore.canAccessAdmin) {
        items.push({
          to: '/scrum/reviews',
          label: 'Task Review Queue',
          badge: pendingApprovalsCount.value,
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
        })
      }
      if (authStore.canAccessAdmin) {
        items.push({
          to: '/admin/access-requests',
          label: 'Access Requests',
          badge: pendingUsersCount.value,
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>'
        })
      }
      return items
    }
    case 'scrum': {
      const items = [
        {
          to: '/scrum/active-sprint',
          label: 'Active Sprint & Board',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/></svg>'
        },
        {
          to: '/scrum/stories',
          label: 'User Stories Backlog',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/></svg>'
        },
        {
          to: '/scrum/sprints',
          label: 'Sprint Planner & History',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>'
        }
      ]

      if (authStore.canManageScrum || authStore.canAccessAdmin) {
        items.push(
          {
            to: '/scrum/reviews',
            label: 'Task Review Queue',
            icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
            badge: pendingApprovalsCount.value
          },
          {
            to: '/scrum/team',
            label: 'Intern Workload Matrix',
            icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>'
          }
        )
      }
      return items
    }
    case 'workforce':
      return [
        {
          to: '/workforce/daily-log',
          label: 'Daily Work Log',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>'
        },
        {
          to: '/workforce/attendance',
          label: 'Attendance & Records',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>'
        },
        {
          to: '/workforce/feed',
          label: 'Department Feed',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/></svg>'
        }
      ]
    case 'operations':
      return [
        {
          to: '/operations/mom',
          label: 'Meeting Minutes (MoM)',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'
        },
        {
          to: '/operations/proposals',
          label: 'Improvement Proposals',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>'
        },
        {
          to: '/operations/calendar',
          label: 'Company Calendar',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>'
        }
      ]
    case 'admin':
      return [
        {
          to: '/admin/access-requests',
          label: 'Access Requests',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>',
          badge: pendingUsersCount.value
        },
        {
          to: '/admin/users',
          label: 'Users & Teams',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>'
        },
        {
          to: '/admin/audit',
          label: 'Audit Trail',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
        },
        {
          to: '/admin/reports',
          label: 'Executive Reports',
          icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'
        }
      ]
    default:
      return []
  }
})
</script>
