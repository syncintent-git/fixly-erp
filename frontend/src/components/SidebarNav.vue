<template>
  <div 
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    :class="[
      'h-[calc(100vh-49px)] overflow-y-auto overflow-x-hidden flex flex-col justify-between transition-all duration-200 ease-in-out border-r border-zinc-800 bg-zinc-950',
      isPinned 
        ? 'w-64 p-4' 
        : (isHovered 
            ? 'absolute top-0 left-0 w-64 p-4 z-40 shadow-2xl shadow-black/90 bg-zinc-950/98 backdrop-blur-md border-r border-zinc-700/80 ring-1 ring-white/5' 
            : 'w-16 py-3 px-2')
    ]">
    
    <!-- Top Navigation Section -->
    <div class="space-y-4">
      
      <!-- Section Identity Header: Expanded Mode -->
      <div v-if="isExpanded" class="p-3 rounded-lg bg-zinc-900 border border-zinc-800 flex items-center justify-between gap-2 shadow-sm animate-in fade-in duration-200">
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="w-7 h-7 rounded-md bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0">
            <span v-html="sectionMeta.icon"></span>
          </div>
          <div class="overflow-hidden">
            <h2 class="text-xs font-bold uppercase tracking-wider text-white truncate">{{ sectionMeta.title }}</h2>
            <p class="text-[10px] text-zinc-400 truncate">{{ sectionMeta.subtitle }}</p>
          </div>
        </div>

        <!-- Pin / Unpin Button -->
        <button 
          type="button"
          @click.stop="$emit('toggle-pin')"
          :title="isPinned ? 'Unpin sidebar (Contract to mini-rail, Ctrl+B)' : 'Pin sidebar open (Ctrl+B)'"
          :class="[
            'w-7 h-7 rounded-md text-xs transition-all shrink-0 cursor-pointer flex items-center justify-center group',
            isPinned 
              ? 'text-orange-400 bg-orange-500/15 hover:bg-orange-500/25 border border-orange-500/40 shadow-sm' 
              : 'text-zinc-400 hover:text-white bg-zinc-800/80 hover:bg-zinc-700 border border-zinc-700/60'
          ]">
          <svg class="w-3.5 h-3.5 transition-transform group-hover:scale-110" viewBox="0 0 24 24" fill="currentColor">
            <path d="M16 12V4h1V2H7v2h1v8l-2 2v2h5.2v6h1.6v-6H18v-2l-2-2z"/>
          </svg>
        </button>
      </div>

      <!-- Section Identity Header: Contracted Rail Mode -->
      <div v-else class="flex justify-center animate-in fade-in duration-200">
        <div 
          :title="`${sectionMeta.title}: ${sectionMeta.subtitle}`"
          class="w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-800 flex items-center justify-center text-orange-400 shadow-sm cursor-default">
          <span v-html="sectionMeta.icon"></span>
        </div>
      </div>

      <!-- Navigation Links List -->
      <nav class="space-y-1">
        <div v-if="isExpanded" class="px-2 pb-1 text-[10px] font-bold uppercase tracking-wider text-zinc-500 flex items-center justify-between">
          <span>Navigation</span>
          <span v-if="!isPinned" class="text-[9px] text-zinc-600 font-mono font-normal">hover overlay</span>
        </div>
        <div v-else class="h-1"></div>

        <!-- Expanded Nav Links -->
        <template v-if="isExpanded">
          <router-link
            v-for="item in currentNavItems"
            :key="item.to"
            :to="item.to"
            :class="[
              'group flex items-center justify-between px-3 py-2 rounded-lg text-xs transition-all',
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
              <span class="truncate">{{ item.label }}</span>
            </div>

            <!-- Accent Badge in Orange -->
            <span 
              v-if="item.badge && item.badge > 0"
              class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500 text-black font-bold min-w-[18px] text-center leading-none inline-flex items-center justify-center shrink-0 shadow-sm">
              {{ item.badge }}
            </span>
          </router-link>
        </template>

        <!-- Contracted Mini-Rail Nav Links -->
        <template v-else>
          <router-link
            v-for="item in currentNavItems"
            :key="item.to"
            :to="item.to"
            :title="item.label"
            :class="[
              'group relative w-10 h-10 mx-auto rounded-lg flex items-center justify-center transition-all my-1.5',
              isActive(item.to)
                ? 'bg-orange-500/10 text-orange-400 border border-orange-500/40 shadow-sm shadow-orange-500/10 font-bold'
                : 'text-zinc-400 hover:text-white hover:bg-zinc-900 border border-transparent'
            ]">
            <span 
              class="shrink-0 transition-colors" 
              :class="isActive(item.to) ? 'text-orange-400' : 'text-zinc-400 group-hover:text-white'"
              v-html="item.icon">
            </span>

            <!-- Mini Dot / Badge Count -->
            <span 
              v-if="item.badge && item.badge > 0"
              class="absolute -top-1.5 -right-1.5 min-w-[18px] h-[18px] px-1 rounded-full bg-orange-500 text-black text-[10px] font-bold font-mono flex items-center justify-center ring-2 ring-zinc-900 shadow-sm leading-none">
              {{ item.badge }}
            </span>
          </router-link>
        </template>
      </nav>
    </div>

    <!-- Bottom Quick Info Card -->
    <div class="pt-3 border-t border-zinc-800 space-y-2.5">
      <!-- Expanded Bottom Card -->
      <template v-if="isExpanded">
        <div class="p-2.5 bg-zinc-900 rounded-lg border border-zinc-800">
          <div class="flex items-center justify-between text-[10px] font-medium text-zinc-400">
            <span>Active User</span>
            <span class="text-white font-mono font-bold truncate max-w-[100px]">{{ authStore.user?.name || 'User' }}</span>
          </div>
          <div class="mt-1 flex items-center justify-between text-[10px] text-zinc-500 font-mono">
            <span>Department</span>
            <span class="text-orange-400 font-bold">{{ authStore.user?.team || 'General' }}</span>
          </div>
        </div>

        <div class="flex items-center justify-between px-1 text-[10px] text-zinc-500">
          <div class="flex items-center gap-1.5 opacity-70 hover:opacity-100 transition-opacity">
            <img src="/logo.png" alt="Fixly" class="w-3.5 h-3.5 object-contain" />
            <span class="font-semibold text-zinc-400">{{ APP_NAME }}</span>
          </div>
          <span class="font-mono text-[9px] text-zinc-600">{{ APP_VERSION }}</span>
        </div>
      </template>

      <!-- Contracted Bottom Mini-Card -->
      <template v-else>
        <div 
          :title="`${authStore.user?.name || 'User'} • ${authStore.user?.team || 'General'}`"
          class="w-10 h-10 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center mx-auto text-orange-400 font-bold text-xs shadow-inner cursor-default hover:border-orange-500/40 transition-colors">
          {{ userInitials }}
        </div>
        <div class="flex justify-center pt-1" :title="`${APP_NAME} ${APP_VERSION}`">
          <img src="/logo.png" alt="Fixly" class="w-4 h-4 object-contain opacity-70 hover:opacity-100 transition-opacity" />
        </div>
      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useScrumStore } from '../stores/scrum'
import { APP_VERSION, APP_NAME } from '../constants'

const props = defineProps({
  isPinned: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-pin'])

const route = useRoute()
const authStore = useAuthStore()
const scrumStore = useScrumStore()

const isHovered = ref(false)
let hoverTimeout = null

const handleMouseEnter = () => {
  if (hoverTimeout) {
    clearTimeout(hoverTimeout)
    hoverTimeout = null
  }
  isHovered.value = true
}

const handleMouseLeave = () => {
  hoverTimeout = setTimeout(() => {
    isHovered.value = false
  }, 120)
}

const isExpanded = computed(() => props.isPinned || isHovered.value)

const userInitials = computed(() => {
  const name = authStore.user?.name || ''
  if (!name) return 'U'
  const parts = name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const currentSection = computed(() => {
  if (route.path.startsWith('/dashboard')) return 'dashboard'
  if (route.path.startsWith('/scrum')) return 'scrum'
  if (route.path.startsWith('/workforce')) return 'workforce'
  if (route.path.startsWith('/operations')) return 'operations'
  if (route.path.startsWith('/admin')) return 'admin'
  return 'dashboard'
})

const isActive = (path) => {
  return route.path === path
}

const sectionMeta = computed(() => {
  switch (currentSection.value) {
    case 'dashboard':
      return {
        title: 'Command Center',
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

const pendingApprovalsCount = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'PENDING_APPROVAL').length
})

const pendingUsersCount = computed(() => {
  return scrumStore.pendingUsers.length
})

const currentNavItems = computed(() => {
  switch (currentSection.value) {
    case 'dashboard':
      return []
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
