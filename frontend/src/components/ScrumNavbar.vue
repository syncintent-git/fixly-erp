<template>
  <header class="bg-zinc-950 text-white sticky top-0 z-50 border-b border-zinc-800">
    <div class="w-full px-4 sm:px-6 py-2.5 flex items-center justify-between gap-2 sm:gap-4">
      
      <!-- Brand & Title (with mobile hamburger) -->
      <div class="flex items-center space-x-2 sm:space-x-3">
        <!-- Mobile Sidebar Hamburger Toggle (strictly hidden on any dashboard) -->
        <button 
          v-if="!isDashboard"
          @click="$emit('toggle-sidebar')" 
          type="button"
          class="md:hidden p-1.5 -ml-1 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-900 border border-zinc-800/80 transition-colors cursor-pointer"
          title="Open Navigation Menu"
          aria-label="Toggle navigation drawer">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>

        <router-link to="/dashboard" class="flex items-center gap-2 sm:gap-2.5 group">
          <img 
            src="/logo-w-text.png" 
            alt="Fixly Office" 
            class="h-7 sm:h-8 w-auto object-contain transition-transform group-hover:scale-[1.02] duration-200" 
          />
          <span class="text-[10px] font-mono uppercase tracking-wider text-orange-400 bg-orange-500/10 px-1.5 py-0.5 rounded border border-orange-500/30 font-bold self-center">Office</span>
        </router-link>
      </div>

      <!-- Consolidated Top Navigation Hubs (Orange & Black Theme) -->
      <nav class="hidden md:flex items-center space-x-1 bg-zinc-900 p-1 rounded border border-zinc-800 text-xs font-medium">
        
        <!-- Hub 0: Overview Dashboard -->
        <router-link 
          to="/dashboard" 
          :class="[
            'px-3 py-1.5 rounded transition-all flex items-center gap-1.5',
            $route.path === '/dashboard' 
              ? 'bg-orange-500 text-black font-bold shadow-sm' 
              : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
          ]">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"/></svg>
          <span>Dashboard</span>
        </router-link>
        
        <!-- Hub 1: Scrum & Sprints -->
        <router-link 
          to="/scrum" 
          :class="[
            'px-3 py-1.5 rounded transition-all flex items-center gap-1.5',
            $route.path.startsWith('/scrum') 
              ? 'bg-orange-500 text-black font-bold shadow-sm' 
              : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
          ]">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
          <span>Scrum Hub</span>
        </router-link>

        <!-- Hub 2: Workforce -->
        <router-link 
          to="/workforce" 
          :class="[
            'px-3 py-1.5 rounded transition-all flex items-center gap-1.5',
            $route.path.startsWith('/workforce') 
              ? 'bg-orange-500 text-black font-bold shadow-sm' 
              : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
          ]">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          <span>Workforce</span>
        </router-link>

        <!-- Hub 3: Operations -->
        <router-link 
          to="/operations" 
          :class="[
            'px-3 py-1.5 rounded transition-all flex items-center gap-1.5',
            $route.path.startsWith('/operations') 
              ? 'bg-orange-500 text-black font-bold shadow-sm' 
              : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
          ]">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
          <span>Operations</span>
        </router-link>

        <!-- Hub 4: Admin / Reviewer Console -->
        <router-link 
          v-if="authStore.canAccessAdmin"
          to="/admin" 
          :class="[
            'px-3 py-1.5 rounded transition-all flex items-center gap-1.5',
            $route.path.startsWith('/admin') 
              ? 'bg-orange-500 text-black font-bold shadow-sm' 
              : 'text-zinc-300 hover:text-white hover:bg-zinc-800'
          ]">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          <span>{{ authStore.isViewOnly ? 'Reviewer' : 'Admin' }}</span>
          <span 
            v-if="scrumStore.pendingUsers.length > 0" 
            :class="[
              'text-[10px] font-bold px-2 py-0.5 rounded-full font-mono min-w-[18px] text-center leading-none inline-flex items-center justify-center shadow-sm',
              $route.path.startsWith('/admin') ? 'badge-pill-dark' : 'bg-orange-500 text-black'
            ]">
            {{ scrumStore.pendingUsers.length }}
          </span>
        </router-link>
      </nav>

      <!-- Right Actions (Clean User Header Info, Switch Role, Notifications, Logout) -->
      <div class="flex items-center space-x-3">
        
        <!-- Clean User Identity Block -->
        <div class="hidden sm:flex flex-col text-right">
          <span class="text-xs font-bold text-white">{{ authStore.user?.name || 'User' }}</span>
          <span class="text-[10px] text-orange-400 font-mono">{{ roleDisplayTitle }}</span>
        </div>


        <!-- In-App Notifications Bell -->
        <div class="relative" ref="notifPanelRef">
          <button 
            @click.stop="toggleNotifications"
            class="relative p-2 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-white border border-zinc-800 hover:border-orange-500/40 transition-colors cursor-pointer"
            title="Notifications">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
            <span v-if="scrumStore.unreadNotificationCount > 0" class="absolute -top-1.5 -right-1.5 min-w-[18px] h-[18px] px-1 bg-orange-500 text-black rounded-full text-[10px] font-bold font-mono flex items-center justify-center shadow-md leading-none">
              {{ scrumStore.unreadNotificationCount > 99 ? '99+' : scrumStore.unreadNotificationCount }}
            </span>
          </button>

          <!-- Notifications Popover -->
          <div v-if="showNotifPanel" 
            class="absolute right-0 mt-2 w-80 sm:w-96 max-w-[calc(100vw-2rem)] bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl p-3 z-50">
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-zinc-800">
              <span class="text-xs font-bold text-white flex items-center gap-1.5">
                <span>Notifications</span>
                <span v-if="scrumStore.unreadNotificationCount > 0" class="bg-orange-500 text-black text-[10px] font-bold px-2 py-0.5 rounded-full font-mono leading-none">
                  {{ scrumStore.unreadNotificationCount }}
                </span>
              </span>
              <div class="flex items-center gap-2">
                <button 
                  v-if="scrumStore.unreadNotificationCount > 0" 
                  @click.stop="markAllRead" 
                  class="text-[10px] text-orange-400 hover:text-orange-300 hover:underline cursor-pointer">
                  Mark all read
                </button>
                <button 
                  @click.stop="showNotifPanel = false"
                  class="text-zinc-500 hover:text-zinc-300 p-0.5 rounded transition-colors cursor-pointer"
                  title="Close notifications">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
              </div>
            </div>

            <div class="max-h-72 overflow-y-auto space-y-1.5 divide-y divide-zinc-800/40">
              <div v-if="scrumStore.notifications.length === 0" class="py-6 text-center text-xs text-zinc-500 flex flex-col items-center gap-1">
                <svg class="w-7 h-7 text-zinc-600 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/></svg>
                <p>No notifications.</p>
                <p class="text-[10px] text-zinc-600">You're completely up to date.</p>
              </div>
              <div 
                v-for="notif in scrumStore.notifications" 
                :key="notif.id"
                @click="onNotificationClick(notif)"
                :class="[
                  'pt-2 pb-1.5 px-2 rounded-lg transition-colors cursor-pointer text-xs flex items-start gap-2 border',
                  notif.isRead 
                    ? 'opacity-65 bg-zinc-950/40 border-transparent hover:opacity-100 hover:bg-zinc-800/40' 
                    : 'bg-zinc-850 hover:bg-zinc-800 border-orange-500/20 shadow-sm'
                ]">
                <span 
                  :class="['w-2 h-2 rounded-full mt-1 shrink-0', notif.isRead ? 'bg-zinc-600' : 'bg-orange-500 ring-2 ring-orange-500/30']">
                </span>
                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between gap-2">
                    <p :class="['text-xs leading-snug', notif.isRead ? 'text-zinc-300 font-medium' : 'text-white font-bold']">
                      {{ notif.title }}
                    </p>
                    <span class="text-[9px] text-zinc-500 shrink-0 font-mono">{{ formatTime(notif.createdAt) }}</span>
                  </div>
                  <p class="text-[11px] text-zinc-400 mt-0.5 leading-relaxed">{{ notif.message }}</p>
                  <div v-if="notif.link" class="mt-1 flex items-center gap-1 text-[10px] text-orange-400 font-medium">
                    <span>View &rarr;</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Theme Toggle (Light / Dark) -->
        <button 
          @click="themeStore.toggleTheme"
          :title="themeStore.isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
          type="button"
          class="p-2 rounded bg-zinc-900 hover:bg-zinc-800 text-zinc-300 hover:text-white border border-zinc-800 hover:border-orange-500/40 transition-colors cursor-pointer flex items-center justify-center"
          aria-label="Toggle theme">
          <svg v-if="themeStore.isDark" class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          <svg v-else class="w-4 h-4 text-zinc-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </button>

        <!-- Sign Out Button -->
        <button 
          @click="handleLogout"
          class="text-zinc-400 hover:text-white hover:bg-zinc-900 px-2.5 py-1.5 rounded border border-zinc-800 transition-colors text-xs font-medium cursor-pointer flex items-center gap-1.5">
          <span class="hidden sm:inline">Sign Out</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
        </button>

      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useScrumStore } from '../stores/scrum'
import { useThemeStore } from '../stores/theme'
import { formatRoleTitle } from '../constants'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const scrumStore = useScrumStore()
const themeStore = useThemeStore()

const isDashboard = computed(() => {
  return route.path === '/dashboard' || route.path.startsWith('/dashboard/') || route.meta?.section === 'dashboard'
})

defineEmits(['toggle-sidebar'])

const showNotifPanel = ref(false)
const notifPanelRef = ref(null)
let pollTimer = null

const roleDisplayTitle = computed(() => {
  const u = authStore.user
  if (!u) return 'Guest'
  return formatRoleTitle(u.role, u.positionTitle)
})

const toggleNotifications = () => {
  showNotifPanel.value = !showNotifPanel.value
  if (showNotifPanel.value) {
    if (authStore.user?.id) {
      scrumStore.fetchNotifications(authStore.user.id)
    }
  }
}

const handleClickOutside = (e) => {
  if (showNotifPanel.value && notifPanelRef.value && !notifPanelRef.value.contains(e.target)) {
    showNotifPanel.value = false
  }
}

const markAllRead = async () => {
  if (authStore.user?.id) {
    await scrumStore.markAllNotificationsRead(authStore.user.id)
  }
}

const onNotificationClick = async (notif) => {
  if (!notif.isRead) {
    await scrumStore.markNotificationRead(notif.id)
  }
  showNotifPanel.value = false
  if (notif.link) {
    router.push(notif.link)
  }
}

const formatTime = (ts) => {
  if (!ts) return ''
  const timestamp = ts < 1e12 ? ts * 1000 : ts
  const diff = Date.now() - timestamp
  if (diff < 0) return 'Just now'
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'Just now'
  if (mins < 60) return `${mins}m ago`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours}h ago`
  return new Date(timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  if (authStore.user?.id) {
    scrumStore.fetchNotifications(authStore.user.id)
  }
  scrumStore.fetchPendingUsers()
  document.addEventListener('click', handleClickOutside)
  pollTimer = setInterval(() => {
    if (authStore.user?.id) {
      scrumStore.fetchNotifications(authStore.user.id)
    }
  }, 20000)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  if (pollTimer) clearInterval(pollTimer)
})

watch(() => authStore.user?.id, (newId) => {
  if (newId) {
    scrumStore.fetchNotifications(newId)
  }
})
</script>
