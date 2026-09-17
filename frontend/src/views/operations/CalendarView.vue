<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>CORPORATE SCHEDULE</span>
            <span>•</span>
            <span>{{ holidays.length }} Declared Holidays</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Company Calendar & Holidays</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Official declared holidays, corporate breaks, and sprint non-working days.</p>
        </div>

        <div v-if="canManageHolidays" class="shrink-0">
          <button 
            @click="showCreateModal = true"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Declare Holiday</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Upcoming Holiday Highlight Card (if any) -->
    <div v-if="upcomingHoliday" class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 w-full">
      <div class="flex items-center gap-3.5">
        <div class="w-10 h-10 rounded bg-orange-500/10 border border-orange-500/30 text-orange-400 flex items-center justify-center shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
        </div>
        <div>
          <span class="text-[10px] uppercase font-mono text-orange-400 font-bold">Upcoming Holiday</span>
          <h3 class="text-base font-bold text-white mt-0.5">{{ upcomingHoliday.name }}</h3>
          <p class="text-xs text-zinc-400 font-mono">{{ formatHolidayDate(upcomingHoliday.date) }}</p>
        </div>
      </div>

      <div class="bg-zinc-950 px-3.5 py-2 rounded border border-zinc-800 text-center shrink-0">
        <span class="text-[10px] text-zinc-500 uppercase font-mono font-bold">Countdown</span>
        <p class="text-sm font-black text-orange-400 font-mono">{{ getDaysRemaining(upcomingHoliday.date) }}</p>
      </div>
    </div>

    <!-- Holidays List Table -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 space-y-3 w-full">
      <div class="flex items-center justify-between pb-2.5 border-b border-zinc-800">
        <h3 class="text-xs font-bold uppercase text-zinc-300 tracking-wider">Holiday Schedule</h3>
        <span class="text-xs font-mono text-zinc-500">{{ holidays.length }} Dates</span>
      </div>

      <div v-if="holidays.length === 0" class="py-6 text-center text-xs text-zinc-600 italic">
        No declared company holidays scheduled.
      </div>
      <div v-else class="space-y-2">
        <div 
          v-for="h in holidays" 
          :key="h.id"
          class="bg-zinc-950 p-3 rounded border border-zinc-800 flex items-center justify-between gap-4 hover:border-zinc-700 transition-colors">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 flex items-center justify-center shrink-0">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            </div>
            <div>
              <h4 class="text-xs font-semibold text-white">{{ h.name }}</h4>
              <p class="text-[11px] text-zinc-400 font-mono">{{ formatHolidayDate(h.date) }}</p>
            </div>
          </div>

          <div v-if="canManageHolidays" class="shrink-0">
            <button 
              @click="handleDeleteHoliday(h.id)"
              class="text-xs text-zinc-500 hover:text-red-400 font-medium px-2 py-1 transition-colors cursor-pointer">
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Declare Holiday Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-md w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Declare Official Holiday</h3>
          <button @click="showCreateModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Holiday Name</label>
          <input 
            type="text" 
            v-model="newHolidayName" 
            placeholder="e.g. Independence Day"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white focus:border-zinc-500 outline-none"
          />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Date</label>
          <input 
            type="date" 
            v-model="newHolidayDate" 
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer"
          />
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="showCreateModal = false" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="handleSubmitHoliday"
            :disabled="!newHolidayName.trim() || !newHolidayDate"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Save Holiday
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { getApiBase } from '@/config'
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

const authStore = useAuthStore()


const holidays = ref([])
const showCreateModal = ref(false)
const newHolidayName = ref('')
const newHolidayDate = ref('')

const canManageHolidays = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin
})

const upcomingHoliday = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  const future = holidays.value
    .filter(h => h.date >= today)
    .sort((a, b) => new Date(a.date) - new Date(b.date))
  return future.length > 0 ? future[0] : null
})

const formatHolidayDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })
}

const getDaysRemaining = (dateStr) => {
  const target = new Date(dateStr)
  const today = new Date()
  const diffTime = target - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  if (diffDays <= 0) return 'Today'
  if (diffDays === 1) return '1 Day'
  return `${diffDays} Days`
}

const fetchHolidays = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/holidays/all`)
    if (res.ok) {
      holidays.value = await res.json()
    }
  } catch (err) {
    console.error('Error fetching holidays:', err)
  }
}

const handleSubmitHoliday = async () => {
  if (!newHolidayName.value.trim() || !newHolidayDate.value) return

  try {
    const res = await fetch(`${getApiBase()}/api/holidays/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newHolidayName.value.trim(),
        date: newHolidayDate.value
      })
    })
    if (res.ok) {
      newHolidayName.value = ''
      newHolidayDate.value = ''
      showCreateModal.value = false
      await fetchHolidays()
    }
  } catch (err) {
    console.error('Error creating holiday:', err)
  }
}

const handleDeleteHoliday = async (id) => {
  try {
    await fetch(`${getApiBase()}/api/holidays/delete/${id}`, { method: 'DELETE' })
    await fetchHolidays()
  } catch (err) {
    console.error('Error deleting holiday:', err)
  }
}

onMounted(() => {
  fetchHolidays()
})
</script>
