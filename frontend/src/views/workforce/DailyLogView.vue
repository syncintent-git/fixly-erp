<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>DAILY ACCOUNTABILITY</span>
            <span>•</span>
            <span>{{ todayFormatted }}</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Daily Work Log & Attendance</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Submit daily work accomplishments, plan tomorrow's deliverables, and record attendance.</p>
        </div>

        <!-- Days logged badge -->
        <div class="bg-zinc-950 border border-zinc-800 rounded p-3 px-4 shrink-0 flex items-center gap-3">
          <div>
            <span class="text-[10px] text-zinc-500 uppercase font-mono">Total Days Logged</span>
            <p class="text-base font-black text-orange-400 font-mono">{{ myLogs.length }} Days</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Alert / Message -->
    <div v-if="statusMessage" :class="['p-3 rounded text-xs font-medium border', statusError ? 'bg-zinc-900 border-zinc-700 text-red-300' : 'bg-zinc-900 border-zinc-700 text-zinc-200']">
      <span>{{ statusMessage }}</span>
    </div>

    <!-- Yesterday's Goal Reminder Card (if available) -->
    <div v-if="previousGoal" class="bg-zinc-900 border border-zinc-800 rounded-lg p-4 flex items-start gap-3">
      <div class="p-2 bg-zinc-950 rounded text-orange-400 shrink-0 border border-zinc-800">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
      </div>
      <div>
        <h4 class="text-xs font-bold text-zinc-300 uppercase tracking-wider">Yesterday's Planned Goal</h4>
        <p class="text-xs text-zinc-400 mt-0.5 leading-relaxed">{{ previousGoal }}</p>
      </div>
    </div>

    <!-- Main Work Log Form Card -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-zinc-800">
        <div>
          <h2 class="text-sm font-bold text-white">Log Today's Work & Attendance</h2>
          <p class="text-xs text-zinc-400">Record tasks completed and select attendance mode.</p>
        </div>
        
        <!-- Date Selector for past editing -->
        <div class="flex items-center gap-2 bg-zinc-950 border border-zinc-700 px-2.5 py-1 rounded text-xs">
          <span class="text-zinc-500 text-[10px] uppercase font-bold">Log Date:</span>
          <input 
            type="date" 
            v-model="selectedDate" 
            @change="loadLogForSelectedDate"
            class="bg-transparent text-white font-mono outline-none cursor-pointer text-xs"
          />
        </div>
      </div>

      <!-- Attendance Mode Options -->
      <div>
        <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Attendance Mode</label>
        <div class="grid grid-cols-3 gap-2.5">
          <button 
            v-for="mode in ATTENDANCE_MODES"
            :key="mode.id"
            type="button"
            @click="attendanceMode = mode.id"
            :class="[
              'p-2.5 rounded border text-xs font-medium flex flex-col items-center justify-center gap-0.5 transition-colors cursor-pointer',
              attendanceMode === mode.id 
                ? 'bg-orange-500/10 text-orange-400 border-orange-500/40 font-bold shadow-sm' 
                : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700 hover:text-white'
            ]">
            <span>{{ mode.label }}</span>
            <span class="text-[9px] text-zinc-500">{{ mode.desc }}</span>
          </button>
        </div>
      </div>

      <!-- Today's Tasks Completed -->
      <div>
        <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">
          Tasks Completed Today
        </label>
        <textarea 
          v-model="todayWork" 
          rows="4" 
          class="w-full bg-zinc-950 border border-zinc-800 rounded p-3 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none leading-relaxed transition-colors"
          placeholder="Detail specific tasks completed, PRs submitted, bugs resolved, or modules reviewed...">
        </textarea>
      </div>

      <!-- Tomorrow's Goal -->
      <div>
        <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">
          Tomorrow's Goal / Deliverable
        </label>
        <textarea 
          v-model="tomorrowGoal" 
          rows="2" 
          class="w-full bg-zinc-950 border border-zinc-800 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none leading-relaxed transition-colors"
          placeholder="Key deliverables planned for tomorrow...">
        </textarea>
      </div>

      <!-- Submit Button -->
      <div class="pt-2 flex items-center justify-between">
        <span class="text-[11px] text-zinc-500">
          Status: <strong class="text-zinc-300">{{ hasLoggedSelectedDate ? 'Previously Saved' : 'Not yet logged' }}</strong>
        </span>
        <button 
          @click="handleSubmitLog"
          :disabled="isSubmitting || !todayWork.trim()"
          class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-5 py-2.5 rounded transition-colors cursor-pointer disabled:opacity-50 flex items-center gap-2">
          <span>{{ isSubmitting ? 'Saving...' : (hasLoggedSelectedDate ? 'Update Log' : 'Submit Today’s Log') }}</span>
        </button>
      </div>

    </div>

    <!-- Personal Recent History -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full space-y-3">
      <div class="flex items-center justify-between pb-2.5 border-b border-zinc-800">
        <h3 class="text-xs font-bold uppercase text-zinc-300 tracking-wider">Your Recent Logs</h3>
        <span class="text-xs text-zinc-500 font-mono">{{ myLogs.length }} Entries</span>
      </div>

      <div v-if="myLogs.length === 0" class="py-6 text-center text-xs text-zinc-600 italic">
        No logs recorded yet.
      </div>
      <div v-else class="space-y-2.5">
        <div 
          v-for="log in myLogs.slice(0, 5)" 
          :key="log.id"
          class="bg-zinc-950 p-3 rounded border border-zinc-800 space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-mono text-xs font-bold text-orange-400">{{ log.date }}</span>
            <span class="text-[9px] uppercase font-mono text-zinc-400 bg-zinc-900 px-2 py-0.5 rounded-full border border-zinc-800">
              {{ log.attendanceMode || 'In-Office' }}
            </span>
          </div>
          <p class="text-xs text-zinc-300 leading-relaxed">{{ log.workDone || log.todayLog }}</p>
          <div v-if="log.nextDayGoal || log.tomorrowGoal" class="pt-1.5 border-t border-zinc-800 text-[11px] text-zinc-400">
            <span class="text-zinc-500 font-medium">Planned:</span> {{ log.nextDayGoal || log.tomorrowGoal }}
          </div>
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


const todayString = new Date().toISOString().split('T')[0]
const selectedDate = ref(todayString)
const todayFormatted = computed(() => new Date().toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }))

const ATTENDANCE_MODES = [
  { id: 'office', label: 'In-Office', desc: 'Working from office' },
  { id: 'remote', label: 'Remote / WFH', desc: 'Working from home' },
  { id: 'field', label: 'On-Duty / Field', desc: 'Field / client duty' }
]

const attendanceMode = ref('office')
const todayWork = ref('')
const tomorrowGoal = ref('')
const previousGoal = ref('')
const isSubmitting = ref(false)
const statusMessage = ref('')
const statusError = ref(false)
const editingLogId = ref(null)

const myLogs = ref([])

const hasLoggedSelectedDate = computed(() => {
  return myLogs.value.some(l => l.date === selectedDate.value)
})

const fetchMyLogs = async () => {
  if (!authStore.user?.id && !authStore.user?.email) return
  try {
    const res = await fetch(`${getApiBase()}/api/logs/all`)
    if (res.ok) {
      const all = await res.json()
      myLogs.value = all.filter(l => 
        (authStore.user?.id && (l.user_id === authStore.user.id || l.userId === authStore.user.id)) || 
        (authStore.user?.rollNumber && l.rollNumber === authStore.user.rollNumber) || 
        (authStore.user?.name && l.name && l.name.toLowerCase() === authStore.user.name.toLowerCase())
      )
      loadLogForSelectedDate()
      findPreviousGoal()
    }
  } catch (err) {
    console.error('Error fetching logs:', err)
  }
}

const findPreviousGoal = () => {
  const sorted = [...myLogs.value].sort((a, b) => new Date(b.date) - new Date(a.date))
  const past = sorted.find(l => l.date < selectedDate.value && (l.nextDayGoal || l.tomorrowGoal))
  if (past) {
    previousGoal.value = past.nextDayGoal || past.tomorrowGoal
  }
}

const loadLogForSelectedDate = () => {
  const existing = myLogs.value.find(l => l.date === selectedDate.value)
  if (existing) {
    todayWork.value = existing.workDone || existing.todayLog || ''
    tomorrowGoal.value = existing.nextDayGoal || existing.tomorrowGoal || ''
    attendanceMode.value = existing.attendanceMode || 'office'
    editingLogId.value = existing.id
  } else {
    todayWork.value = ''
    tomorrowGoal.value = ''
    attendanceMode.value = 'office'
    editingLogId.value = null
  }
}

const handleSubmitLog = async () => {
  if (!todayWork.value.trim()) return
  isSubmitting.value = true
  statusMessage.value = ''
  statusError.value = false

  try {
    const payload = {
      date: selectedDate.value,
      workDone: todayWork.value.trim(),
      todayLog: todayWork.value.trim(),
      nextDayGoal: tomorrowGoal.value.trim(),
      tomorrowGoal: tomorrowGoal.value.trim(),
      attendanceMode: attendanceMode.value,
      name: authStore.user?.name || 'Intern',
      rollNumber: authStore.user?.rollNumber || 'EMP-001',
      team: authStore.user?.team || 'Frontend',
      user_id: authStore.user?.id,
      userId: authStore.user?.id
    }

    let res
    if (editingLogId.value) {
      res = await fetch(`${getApiBase()}/api/logs/update/${editingLogId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    } else {
      res = await fetch(`${getApiBase()}/api/logs/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
    }

    if (res.ok) {
      statusMessage.value = 'Work log saved successfully.'
      await fetchMyLogs()
    } else {
      const err = await res.json()
      statusError.value = true
      statusMessage.value = err.detail || 'Failed to save work log.'
    }
  } catch (err) {
    statusError.value = true
    statusMessage.value = 'Unable to connect to server.'
  } finally {
    isSubmitting.value = false
    setTimeout(() => { statusMessage.value = '' }, 3000)
  }
}

onMounted(() => {
  fetchMyLogs()
})
</script>
