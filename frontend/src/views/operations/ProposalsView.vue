<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>SUGGESTIONS & INITIATIVES</span>
            <span>•</span>
            <span>{{ proposals.length }} Proposals</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Improvement Proposals</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Submit workflow suggestions, process improvements, and product feature requests.</p>
        </div>

        <div class="shrink-0">
          <button 
            @click="showCreateModal = true"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Submit Proposal</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
      <div class="flex items-center gap-2 flex-1 min-w-[240px]">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Filter proposals by keyword or contributor..." 
          class="w-full bg-transparent text-xs text-white placeholder-zinc-500 outline-none"
        />
      </div>

      <div class="flex items-center gap-3">
        <select v-model="filterType" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs text-zinc-300 outline-none cursor-pointer">
          <option value="">All Types</option>
          <option value="Suggestion">Suggestion</option>
          <option value="Feature Request">Feature Request</option>
        </select>
      </div>
    </div>

    <!-- Proposals List -->
    <div v-if="filteredProposals.length === 0" class="bg-zinc-900/60 border border-zinc-800 rounded-lg p-10 text-center text-zinc-500 w-full">
      <p class="font-medium text-sm text-zinc-400">No proposals found</p>
      <p class="text-xs text-zinc-600 mt-0.5">Submit the first proposal or suggestion to kickstart ideas.</p>
    </div>

    <div v-else class="space-y-3 w-full">
      <div 
        v-for="item in filteredProposals" 
        :key="item.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 flex flex-col md:flex-row justify-between gap-4 hover:border-zinc-700 transition-colors w-full">
        
        <div class="space-y-1.5 flex-1">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-orange-500/30 bg-orange-500/10 text-orange-400 font-bold">
              {{ item.suggestionType }}
            </span>
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-800 bg-zinc-900 text-zinc-400">
              {{ item.suggestionStatus }}
            </span>
            <span class="text-zinc-600 text-xs">•</span>
            <span class="text-xs text-zinc-400 font-mono">By {{ item.name }} ({{ item.team || 'Team' }})</span>
          </div>

          <p class="text-xs text-zinc-200 font-medium whitespace-pre-line leading-relaxed">{{ item.suggestionDescription }}</p>

          <p class="text-[10px] text-zinc-500 font-mono">
            Logged on {{ item.date }}
          </p>
        </div>

        <div v-if="item.suggestionDeadline" class="md:text-right shrink-0">
          <p class="text-[10px] text-zinc-500 uppercase font-mono mb-0.5">Target Date</p>
          <p class="text-xs font-mono text-zinc-300 bg-zinc-950 border border-zinc-800 px-2.5 py-1 rounded inline-block">
            {{ item.suggestionDeadline }}
          </p>
        </div>

      </div>
    </div>

    <!-- Create Proposal Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Submit Improvement Proposal</h3>
          <button @click="showCreateModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Type</label>
            <select v-model="newType" class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
              <option value="Suggestion">Workflow Suggestion</option>
              <option value="Feature Request">Product Feature Request</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Target Date</label>
            <input 
              type="date" 
              v-model="newDeadline" 
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer"
            />
          </div>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Description</label>
          <textarea 
            v-model="newDesc" 
            rows="4" 
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="Explain the suggestion, problem it solves, and anticipated impact...">
          </textarea>
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="showCreateModal = false" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="handleSubmit"
            :disabled="!newDesc.trim()"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Submit Proposal
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


const proposals = ref([])
const searchQuery = ref('')
const filterType = ref('')

const showCreateModal = ref(false)
const newType = ref('Suggestion')
const newDeadline = ref('')
const newDesc = ref('')

const filteredProposals = computed(() => {
  return proposals.value.filter(p => {
    const matchType = !filterType.value || p.suggestionType === filterType.value
    const matchSearch = !searchQuery.value ||
      (p.suggestionDescription && p.suggestionDescription.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (p.name && p.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchType && matchSearch
  })
})

const fetchProposals = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/logs/all`)
    if (res.ok) {
      const all = await res.json()
      proposals.value = all.filter(l => l.suggestionDescription && l.suggestionDescription.trim() !== '')
    }
  } catch (err) {
    console.error('Error fetching proposals:', err)
  }
}

const handleSubmit = async () => {
  if (!newDesc.value.trim()) return

  const payload = {
    date: new Date().toISOString().split('T')[0],
    workDone: 'Logged an improvement proposal',
    todayLog: 'Logged an improvement proposal',
    name: authStore.user?.name || 'Intern',
    rollNumber: authStore.user?.rollNumber || 'EMP-001',
    team: authStore.user?.team || 'General',
    user_id: authStore.user?.id,
    userId: authStore.user?.id,
    suggestionType: newType.value,
    suggestionDescription: newDesc.value.trim(),
    suggestionDeadline: newDeadline.value,
    suggestionStatus: 'Pending'
  }

  try {
    const res = await fetch(`${getApiBase()}/api/logs/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      newDesc.value = ''
      newDeadline.value = ''
      showCreateModal.value = false
      await fetchProposals()
    }
  } catch (err) {
    console.error('Error submitting proposal:', err)
  }
}

onMounted(() => {
  fetchProposals()
})
</script>
