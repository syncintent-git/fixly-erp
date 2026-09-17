<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>ACTIVITY STREAM</span>
            <span>•</span>
            <span>{{ filteredFeed.length }} Updates</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Department Activity Feed</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Real-time daily feed of what your team and cross-functional departments are working on.</p>
        </div>
      </div>
    </div>

    <!-- Filters & Search -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
      <div class="flex items-center gap-2 flex-1 min-w-[240px]">
        <svg class="w-4 h-4 text-zinc-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by employee, task or keyword..." 
          class="w-full bg-transparent text-xs text-white placeholder-zinc-500 outline-none"
        />
      </div>

      <div class="flex items-center gap-3">
        <select v-model="filterDepartment" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs text-zinc-300 outline-none cursor-pointer">
          <option value="">All Departments</option>
          <option value="Frontend">Frontend</option>
          <option value="Backend">Backend</option>
          <option value="DevOps">DevOps</option>
          <option value="Mobile">Mobile</option>
          <option value="QA">QA</option>
          <option value="Design">Design</option>
        </select>
        <input 
          type="date" 
          v-model="filterDate" 
          class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs font-mono text-white outline-none cursor-pointer"
        />
        <button 
          v-if="filterDate"
          @click="filterDate = ''"
          class="text-xs text-zinc-400 hover:text-white underline cursor-pointer">
          Clear
        </button>
      </div>
    </div>

    <!-- Feed Cards -->
    <div v-if="filteredFeed.length === 0" class="bg-zinc-900/60 border border-zinc-800 rounded-lg p-10 text-center text-zinc-500 w-full">
      <p class="font-medium text-sm text-zinc-400">No updates found</p>
      <p class="text-xs text-zinc-600 mt-0.5">Adjust search parameters or date filters.</p>
    </div>

    <div v-else class="space-y-3 w-full">
      <div 
        v-for="log in filteredFeed" 
        :key="log.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-4 space-y-2.5 hover:border-zinc-700 transition-colors w-full">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded bg-orange-500/10 border border-orange-500/30 text-orange-400 font-bold flex items-center justify-center text-xs">
              {{ (log.name || 'U').charAt(0) }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="font-bold text-white text-xs sm:text-sm">{{ log.name }}</h3>
                <span class="text-[10px] text-zinc-500 font-mono">({{ log.rollNumber }})</span>
                <span class="bg-orange-500/10 text-orange-400 text-[10px] font-mono px-2 py-0.5 rounded-full border border-orange-500/30 font-bold">
                  {{ log.team }}
                </span>
              </div>
            </div>
          </div>

          <div class="flex items-center gap-2 text-xs font-mono text-zinc-500">
            <span>{{ log.date }}</span>
            <span>•</span>
            <span class="text-zinc-400 uppercase text-[10px]">{{ log.attendanceMode || 'Office' }}</span>
          </div>
        </div>

        <div class="bg-zinc-950 p-3 rounded border border-zinc-800 text-xs text-zinc-200 leading-relaxed whitespace-pre-line">
          {{ log.workDone || log.todayLog }}
        </div>

        <div v-if="log.nextDayGoal || log.tomorrowGoal" class="pt-1 flex items-start gap-2 text-xs text-zinc-400">
          <span class="text-zinc-500 font-medium shrink-0">Next Goal:</span>
          <span class="text-zinc-300">{{ log.nextDayGoal || log.tomorrowGoal }}</span>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { getApiBase } from '@/config'
import { ref, computed, onMounted } from 'vue'


const allLogs = ref([])
const searchQuery = ref('')
const filterDepartment = ref('')
const filterDate = ref('')

const filteredFeed = computed(() => {
  return allLogs.value.filter(log => {
    const matchDept = !filterDepartment.value || (log.team || '').toLowerCase() === filterDepartment.value.toLowerCase()
    const matchDate = !filterDate.value || log.date === filterDate.value
    const contentText = (log.workDone || log.todayLog || '').toLowerCase()
    const matchSearch = !searchQuery.value || 
      (log.name && log.name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      contentText.includes(searchQuery.value.toLowerCase()) ||
      (log.rollNumber && log.rollNumber.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchDept && matchDate && matchSearch
  }).sort((a, b) => new Date(b.date) - new Date(a.date))
})

const fetchFeed = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/logs/all`)
    if (res.ok) {
      allLogs.value = await res.json()
    }
  } catch (err) {
    console.error('Error loading feed:', err)
  }
}

onMounted(() => {
  fetchFeed()
})
</script>
