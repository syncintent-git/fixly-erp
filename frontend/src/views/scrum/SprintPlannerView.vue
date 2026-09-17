<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>AGILE CYCLES</span>
            <span>•</span>
            <span>14-Day Cadence</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Sprint Planner & History</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Configure 14-day sprint cycles, set sprint goals, and manage sprint rollover.</p>
        </div>

        <div v-if="canManageSprints" class="shrink-0">
          <button 
            @click="showCreateModal = true"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>New 14-Day Sprint</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Sprints List -->
    <div class="space-y-3 w-full">
      <div 
        v-for="sprint in scrumStore.sprints" 
        :key="sprint.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 space-y-3 hover:border-zinc-700 transition-colors w-full">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="space-y-0.5">
            <div class="flex flex-wrap items-center gap-2">
              <span class="font-mono text-xs font-bold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded border border-orange-500/30">
                {{ sprint.sprintId }}
              </span>
              <span 
                :class="[
                  'text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-bold',
                  sprint.status === 'ACTIVE' 
                    ? 'border-orange-500/30 bg-orange-500/10 text-orange-400' 
                    : 'border-zinc-700 bg-zinc-950 text-zinc-300'
                ]">
                {{ sprint.status }}
              </span>
              <span class="text-xs font-mono text-zinc-400">
                {{ sprint.startDate }} — {{ sprint.endDate }}
              </span>
            </div>
            <h2 class="text-base font-bold text-white mt-1">{{ sprint.name }}</h2>
          </div>

          <!-- Rollover or Status Actions -->
          <div v-if="canManageSprints" class="flex items-center gap-2 shrink-0">
            <button 
              v-if="sprint.status === 'ACTIVE'"
              @click="openRolloverModal(sprint)"
              class="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium px-3 py-1.5 rounded border border-zinc-700 transition-colors cursor-pointer">
              Rollover Tasks →
            </button>
          </div>
        </div>

        <p class="text-xs text-zinc-300 leading-relaxed bg-zinc-950 p-3 rounded border border-zinc-800">
          <strong class="text-zinc-400">Goals:</strong> {{ sprint.goals || 'Execute sprint backlog items on schedule.' }}
        </p>

        <div class="flex flex-wrap items-center justify-between gap-4 pt-2 text-xs text-zinc-400 border-t border-zinc-800">
          <div>
            <span>Scrum Lead: <strong class="text-zinc-200">{{ sprint.scrumHeadName || 'Rahul Sharma' }}</strong></span>
          </div>
          <div>
            <span>Created: <strong class="text-zinc-200 font-mono">{{ sprint.startDate }}</strong></span>
          </div>
        </div>

      </div>
    </div>

    <!-- Create 14-Day Sprint Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Create 14-Day Sprint</h3>
          <button @click="showCreateModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Sprint Name</label>
          <input 
            type="text" 
            v-model="newSprintName"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="e.g. Sprint 08 - Performance & Features"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Start Date</label>
            <input 
              type="date" 
              v-model="newSprintStart"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer"
            />
          </div>
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Duration</label>
            <div class="bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-zinc-300 font-mono">
              14 Days (Standard)
            </div>
          </div>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Sprint Goals & Deliverables</label>
          <textarea 
            v-model="newSprintGoals"
            rows="3"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="Outline expected deliverables for this 14-day cycle...">
          </textarea>
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="showCreateModal = false" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="handleCreateSprint"
            :disabled="!newSprintName.trim()"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Create 14-Day Sprint
          </button>
        </div>
      </div>
    </div>

    <!-- Rollover Modal -->
    <div v-if="rolloverSprintTarget" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Rollover Incomplete Tasks</h3>
          <button @click="rolloverSprintTarget = null" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <p class="text-xs text-zinc-300">
          Move all unfinished tasks from <strong>{{ rolloverSprintTarget.name }}</strong> to a target sprint.
        </p>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Target Sprint</label>
          <select v-model="targetSprintId" class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
            <option v-for="s in eligibleTargetSprints" :key="s.id" :value="s.id">
              {{ s.sprintId }}: {{ s.name }} ({{ s.status }})
            </option>
          </select>
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="rolloverSprintTarget = null" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="confirmRollover"
            :disabled="!targetSprintId"
            class="bg-white hover:bg-zinc-200 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Execute Rollover
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useScrumStore } from '../../stores/scrum'

const authStore = useAuthStore()
const scrumStore = useScrumStore()

const showCreateModal = ref(false)
const newSprintName = ref('')
const newSprintStart = ref(new Date().toISOString().split('T')[0])
const newSprintGoals = ref('')

const rolloverSprintTarget = ref(null)
const targetSprintId = ref(null)

const canManageSprints = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin
})

const eligibleTargetSprints = computed(() => {
  if (!rolloverSprintTarget.value) return []
  return scrumStore.sprints.filter(s => s.id !== rolloverSprintTarget.value.id)
})

const handleCreateSprint = async () => {
  if (!newSprintName.value.trim()) return

  const start = new Date(newSprintStart.value)
  const end = new Date(start)
  end.setDate(end.getDate() + 14)
  const endStr = end.toISOString().split('T')[0]

  await scrumStore.createSprint({
    name: newSprintName.value.trim(),
    startDate: newSprintStart.value,
    endDate: endStr,
    goals: newSprintGoals.value.trim(),
    scrumHeadName: authStore.user?.name || 'Rahul Sharma'
  }, authStore.user?.id)

  newSprintName.value = ''
  newSprintGoals.value = ''
  showCreateModal.value = false
  await scrumStore.fetchSprints()
}

const openRolloverModal = (sprint) => {
  rolloverSprintTarget.value = sprint
  const other = scrumStore.sprints.find(s => s.id !== sprint.id)
  targetSprintId.value = other ? other.id : null
}

const confirmRollover = async () => {
  if (!rolloverSprintTarget.value || !targetSprintId.value) return
  await scrumStore.rolloverSprint(rolloverSprintTarget.value.id, targetSprintId.value)
  rolloverSprintTarget.value = null
  targetSprintId.value = null
  await scrumStore.fetchSprints()
}

onMounted(() => {
  scrumStore.fetchSprints()
})
</script>
