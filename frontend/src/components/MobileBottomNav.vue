<template>
  <nav 
    aria-label="Mobile Bottom Navigation"
    class="md:hidden fixed bottom-3 left-1/2 -translate-x-1/2 z-40 w-[calc(100%-1.5rem)] max-w-md bg-zinc-900/90 backdrop-blur-xl border border-zinc-800/90 rounded-2xl shadow-2xl shadow-black/80 ring-1 ring-white/5 p-1.5 transition-all duration-300">
    <div class="flex items-center justify-between gap-1">
      
      <!-- Hub 0: Overview Dashboard -->
      <router-link 
        to="/dashboard" 
        :class="[
          'flex-1 flex flex-col items-center justify-center py-2 px-1 rounded-xl transition-all select-none',
          isHubActive('/dashboard') 
            ? 'bg-orange-500 text-black font-extrabold shadow-sm' 
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
        ]">
        <svg class="w-4 h-4 mb-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/>
        </svg>
        <span class="text-[10px] tracking-tight truncate max-w-full">Home</span>
      </router-link>

      <!-- Hub 1: Scrum -->
      <router-link 
        to="/scrum" 
        :class="[
          'flex-1 flex flex-col items-center justify-center py-2 px-1 rounded-xl transition-all select-none',
          isHubActive('/scrum') 
            ? 'bg-orange-500 text-black font-extrabold shadow-sm' 
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
        ]">
        <svg class="w-4 h-4 mb-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
        </svg>
        <span class="text-[10px] tracking-tight truncate max-w-full">Scrum</span>
      </router-link>

      <!-- Hub 2: Workforce -->
      <router-link 
        to="/workforce" 
        :class="[
          'flex-1 flex flex-col items-center justify-center py-2 px-1 rounded-xl transition-all select-none',
          isHubActive('/workforce') 
            ? 'bg-orange-500 text-black font-extrabold shadow-sm' 
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
        ]">
        <svg class="w-4 h-4 mb-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
        </svg>
        <span class="text-[10px] tracking-tight truncate max-w-full">Workforce</span>
      </router-link>

      <!-- Hub 3: Operations -->
      <router-link 
        to="/operations" 
        :class="[
          'flex-1 flex flex-col items-center justify-center py-2 px-1 rounded-xl transition-all select-none',
          isHubActive('/operations') 
            ? 'bg-orange-500 text-black font-extrabold shadow-sm' 
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
        ]">
        <svg class="w-4 h-4 mb-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
        </svg>
        <span class="text-[10px] tracking-tight truncate max-w-full">Ops</span>
      </router-link>

      <!-- Hub 4: Admin / Reviewer (Conditional) -->
      <router-link 
        v-if="authStore.canAccessAdmin"
        to="/admin" 
        :class="[
          'relative flex-1 flex flex-col items-center justify-center py-2 px-1 rounded-xl transition-all select-none',
          isHubActive('/admin') 
            ? 'bg-orange-500 text-black font-extrabold shadow-sm' 
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
        ]">
        <div class="relative">
          <svg class="w-4 h-4 mb-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
          <span 
            v-if="scrumStore.pendingUsers.length > 0"
            :class="[
              'absolute -top-1.5 -right-2 text-[8px] font-mono font-black px-1 rounded-full',
              isHubActive('/admin') ? 'bg-black text-orange-400' : 'bg-orange-500 text-black'
            ]">
            {{ scrumStore.pendingUsers.length }}
          </span>
        </div>
        <span class="text-[10px] tracking-tight truncate max-w-full">{{ authStore.isViewOnly ? 'Review' : 'Admin' }}</span>
      </router-link>

      <!-- Hub 5: Views / Sidebar Drawer Toggle (strictly hidden on any dashboard) -->
      <button 
        v-if="!isDashboard"
        type="button"
        @click="$emit('toggle-drawer')"
        :class="[
          'relative flex-1 flex flex-col items-center justify-center py-2 px-1 rounded-xl transition-all select-none cursor-pointer',
          drawerOpen 
            ? 'bg-zinc-800 text-white font-bold border border-zinc-700' 
            : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
        ]"
        title="Open Sidebar Subtasks">
        <div class="relative">
          <svg class="w-4 h-4 mb-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/>
          </svg>
          <span 
            v-if="pendingBadgeCount > 0"
            class="absolute -top-1.5 -right-2 w-2 h-2 rounded-full bg-orange-500">
          </span>
        </div>
        <span class="text-[10px] tracking-tight truncate max-w-full">Subtasks</span>
      </button>

    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useScrumStore } from '../stores/scrum'

defineProps({
  drawerOpen: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-drawer'])

const route = useRoute()
const authStore = useAuthStore()
const scrumStore = useScrumStore()

const isDashboard = computed(() => {
  return route.path === '/dashboard' || route.path.startsWith('/dashboard/') || route.meta?.section === 'dashboard'
})

const isHubActive = (prefix) => {
  return route.path.startsWith(prefix)
}

const pendingBadgeCount = computed(() => {
  let count = 0
  if (route.path.startsWith('/scrum')) {
    count = scrumStore.tasks.filter(t => t.status === 'PENDING_APPROVAL').length
  } else if (route.path.startsWith('/admin')) {
    count = scrumStore.pendingUsers.length
  }
  return count
})
</script>
