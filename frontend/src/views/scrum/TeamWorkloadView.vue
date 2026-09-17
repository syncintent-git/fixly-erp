<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>CAPACITY PLANNING</span>
            <span>•</span>
            <span>{{ internList.length }} Interns</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Intern Workload Matrix</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Monitor task distribution across Frontend, Backend, and DevOps engineering tracks.</p>
        </div>

        <div v-if="canAssign" class="shrink-0">
          <button 
            @click="openAssignModal(null)"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Assign New Task</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Track Filter Tabs -->
    <div class="flex space-x-2 overflow-x-auto pb-1 w-full">
      <button 
        v-for="track in ['ALL', 'Frontend', 'Backend', 'DevOps']"
        :key="track"
        @click="selectedTrack = track"
        :class="[
          'px-3 py-1.5 rounded text-xs font-semibold transition-colors border cursor-pointer',
          selectedTrack === track 
            ? 'bg-orange-500 text-black border-orange-400 font-bold shadow-sm' 
            : 'bg-zinc-900 text-zinc-300 border-zinc-800 hover:bg-zinc-850 hover:text-white'
        ]">
        {{ track === 'ALL' ? 'All Tracks' : `${track} Engineering` }}
      </button>
    </div>

    <!-- Intern Workload Cards Grid (Full Width) -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full">
      <div 
        v-for="intern in filteredInterns" 
        :key="intern.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 space-y-4 hover:border-zinc-700 transition-colors flex flex-col justify-between">
        
        <div class="space-y-3">
          <div class="flex items-start justify-between gap-3">
            <div>
              <h3 class="text-sm font-bold text-white">{{ intern.name }}</h3>
              <p class="text-xs text-zinc-400 font-mono">{{ intern.email }}</p>
            </div>
            <span class="text-[9px] font-mono uppercase px-2 py-0.5 rounded border border-orange-500/30 bg-orange-500/10 text-orange-400 font-bold">
              {{ formatRole(intern.role) }}
            </span>
          </div>

          <!-- Task Metrics -->
          <div class="grid grid-cols-3 gap-2 bg-zinc-950 p-2.5 rounded border border-zinc-800 text-center">
            <div>
              <span class="text-[9px] font-medium text-zinc-500 uppercase">To Do</span>
              <p class="text-sm font-bold text-zinc-200 mt-0.5">{{ getInternTasks(intern.id, 'TODO').length }}</p>
            </div>
            <div>
              <span class="text-[9px] font-medium text-zinc-400 uppercase">Active</span>
              <p class="text-sm font-black text-orange-400 mt-0.5">{{ getInternTasks(intern.id, 'IN_PROGRESS').length }}</p>
            </div>
            <div>
              <span class="text-[9px] font-medium text-zinc-400 uppercase">Done</span>
              <p class="text-sm font-bold text-white mt-0.5">{{ getInternTasks(intern.id, 'APPROVED').length }}</p>
            </div>
          </div>

          <!-- Active Tasks Previews -->
          <div class="space-y-1.5 pt-1">
            <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Current Assignments</p>
            <div v-if="getInternActiveTasks(intern.id).length === 0" class="text-xs text-zinc-600 italic py-1">
              No active tasks right now.
            </div>
            <div 
              v-for="t in getInternActiveTasks(intern.id).slice(0, 2)" 
              :key="t.id"
              class="bg-zinc-950 p-2 rounded border border-zinc-800 text-xs">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10px] text-orange-400 font-bold">{{ t.taskId }}</span>
                <span class="text-[9px] text-zinc-500 font-mono">{{ t.status }}</span>
              </div>
              <p class="text-zinc-300 truncate mt-0.5">{{ t.title }}</p>
            </div>
          </div>
        </div>

        <!-- Assign Task Button -->
        <div v-if="canAssign" class="pt-3 border-t border-zinc-800">
          <button 
            @click="openAssignModal(intern)"
            class="w-full bg-zinc-800 hover:bg-zinc-750 hover:border-orange-500/40 hover:text-orange-400 text-zinc-200 font-medium text-xs py-1.5 rounded transition-colors flex items-center justify-center gap-1.5 cursor-pointer border border-zinc-700">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Assign Task</span>
          </button>
        </div>

      </div>
    </div>

    <!-- Assign Task Modal -->
    <div v-if="showAssignModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Assign Task</h3>
          <button @click="showAssignModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Parent User Story</label>
          <select v-model="assignStoryId" class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
            <option v-for="s in scrumStore.stories" :key="s.id" :value="s.id">{{ s.storyId }}: {{ s.title }}</option>
          </select>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Task Title</label>
          <input 
            type="text" 
            v-model="assignTitle"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="e.g. Implement Docker health checks"
          />
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Assign Intern</label>
          <select v-model="assignInternId" class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
            <option v-for="u in internList" :key="u.id" :value="u.id">{{ u.name }} ({{ formatRole(u.role) }})</option>
          </select>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Task Instructions</label>
          <textarea 
            v-model="assignDesc"
            rows="3"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="Detailed instructions for the intern...">
          </textarea>
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="showAssignModal = false" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="handleCreateTask"
            :disabled="!assignTitle.trim() || !assignInternId || !assignStoryId"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Assign Task
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
import { getApiBase } from '../../config'

const authStore = useAuthStore()
const scrumStore = useScrumStore()

const selectedTrack = ref('ALL')
const internList = ref([])

const showAssignModal = ref(false)
const assignStoryId = ref(null)
const assignTitle = ref('')
const assignInternId = ref(null)
const assignDesc = ref('')

const canAssign = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin
})

const filteredInterns = computed(() => {
  if (selectedTrack.value === 'ALL') return internList.value
  const t = selectedTrack.value.toLowerCase()
  return internList.value.filter(u => (u.role || '').toLowerCase().includes(t))
})

const getInternTasks = (internId, status = null) => {
  return scrumStore.tasks.filter(t => {
    const matchIntern = t.assignedToId === internId
    const matchStatus = !status || (status === 'APPROVED' ? (t.status === 'APPROVED' || t.status === 'DONE') : t.status === status)
    return matchIntern && matchStatus
  })
}

const getInternActiveTasks = (internId) => {
  return scrumStore.tasks.filter(t => t.assignedToId === internId && t.status !== 'APPROVED' && t.status !== 'DONE')
}

const formatRole = (role) => {
  if (!role) return 'Intern'
  if (role === 'frontend_developer') return 'Frontend'
  if (role === 'backend_developer') return 'Backend'
  if (role === 'devops_developer') return 'DevOps'
  return role.replace('_', ' ')
}

const openAssignModal = (intern) => {
  if (intern) assignInternId.value = intern.id
  if (scrumStore.stories.length > 0 && !assignStoryId.value) {
    assignStoryId.value = scrumStore.stories[0].id
  }
  showAssignModal.value = true
}

const handleCreateTask = async () => {
  if (!assignTitle.value.trim() || !assignStoryId.value || !assignInternId.value) return

  const intern = internList.value.find(u => u.id === assignInternId.value)
  const trackName = intern ? formatRole(intern.role) : 'General'

  await scrumStore.createTask({
    title: assignTitle.value.trim(),
    description: assignDesc.value.trim(),
    storyId: assignStoryId.value,
    assignedToId: assignInternId.value,
    assignedToName: intern?.name || 'Intern',
    sprintId: scrumStore.activeSprint?.id || null,
    track: trackName
  }, authStore.user?.id)

  assignTitle.value = ''
  assignDesc.value = ''
  showAssignModal.value = false
  await scrumStore.fetchTasks()
}

onMounted(async () => {
  await scrumStore.fetchStories()
  await scrumStore.fetchTasks()

  try {
    const res = await fetch(`${getApiBase()}/api/users/all`)
    if (res.ok) {
      const all = await res.json()
      internList.value = all.filter(u => ['frontend_developer', 'backend_developer', 'devops_developer', 'intern'].includes(u.role?.toLowerCase()))
      if (internList.value.length > 0 && !assignInternId.value) {
        assignInternId.value = internList.value[0].id
      }
    }
  } catch (err) {
    console.error('Error fetching interns:', err)
  }
})
</script>
