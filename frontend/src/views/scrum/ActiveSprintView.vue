<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Sprint Header Card (Clean flat enterprise style, NO colored strips, NO neon pills) -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-5">
        <div>
          <div class="flex flex-wrap items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>Cycle: {{ activeSprint?.startDate }} — {{ activeSprint?.endDate }}</span>
            <span>•</span>
            <span>Scrum Lead: <strong class="text-zinc-200">{{ activeSprint?.scrumHeadName || 'Rahul Sharma' }}</strong></span>
          </div>

          <div class="flex flex-wrap items-center gap-3">
            <h1 class="text-xl sm:text-2xl font-bold tracking-tight text-white">
              {{ activeSprint ? activeSprint.name : 'Sprint 07 - Core Execution' }}
            </h1>
            <select 
              v-if="scrumStore.sprints.length > 1"
              v-model="selectedSprintId"
              @change="onSprintChange"
              class="bg-zinc-950 border border-zinc-700 text-xs font-medium text-zinc-200 rounded px-2.5 py-1 outline-none cursor-pointer">
              <option v-for="s in scrumStore.sprints" :key="s.id" :value="s.id">
                {{ s.sprintId }}: {{ s.name }} ({{ s.status }})
              </option>
            </select>
          </div>

          <p class="text-xs text-zinc-400 mt-1 max-w-3xl leading-relaxed">
            {{ activeSprint?.goals || 'Deliver sprint commitments on schedule. Complete backlog items and coordinate approvals.' }}
          </p>
        </div>

        <!-- Progress Indicator -->
        <div class="bg-zinc-950 border border-zinc-800 rounded-md p-3.5 shrink-0 flex flex-col justify-center min-w-[200px]">
          <div class="flex items-baseline justify-between text-xs">
            <span class="font-mono text-zinc-400 uppercase font-semibold">Sprint Progress</span>
            <span class="font-mono text-orange-400 font-black text-sm">{{ sprintProgressPercentage }}%</span>
          </div>
          <div class="w-full bg-zinc-800 rounded h-1.5 mt-2 overflow-hidden">
            <div 
              class="bg-orange-500 h-full rounded transition-all duration-300" 
              :style="{ width: `${sprintProgressPercentage}%` }">
            </div>
          </div>
          <p class="text-[10px] text-zinc-400 mt-1.5 font-mono">
            {{ approvedTasks.length }} of {{ sprintTasks.length }} tasks approved
          </p>
        </div>
      </div>

      <!-- Metric Numbers Strip -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 mt-4 border-t border-zinc-800 text-xs">
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Total Tasks</span>
          <p class="text-xl font-bold text-white mt-0.5">{{ sprintTasks.length }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">In Progress</span>
          <p class="text-xl font-black text-orange-400 mt-0.5">{{ inProgressTasks.length }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Pending Review</span>
          <p class="text-xl font-bold text-white mt-0.5">{{ pendingReviewTasks.length }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Approved</span>
          <p class="text-xl font-bold text-zinc-300 mt-0.5">{{ approvedTasks.length }}</p>
        </div>
      </div>
    </div>

    <!-- Active Rework Alert Banner (if user has rework tasks) -->
    <div v-if="myReworkTasks.length > 0" class="space-y-2.5 w-full">
      <div 
        v-for="task in myReworkTasks" 
        :key="task.id"
        class="bg-zinc-900 border border-orange-500/40 rounded-md p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div class="space-y-1">
          <div class="flex items-center gap-2 text-xs">
            <span class="font-mono text-orange-400 font-bold">{{ task.taskId }}</span>
            <span class="text-zinc-600">•</span>
            <span class="text-sm font-semibold text-white">{{ task.title }}</span>
            <span class="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/30 font-bold">Rework Required</span>
          </div>
          <p class="text-xs text-zinc-300 font-medium">
            <strong class="text-orange-400">Lead Feedback:</strong> {{ task.reviewNotes || 'Please adjust per requirements and re-submit.' }}
          </p>
        </div>
        <button 
          @click="openSubmitModal(task)"
          class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-3 py-1.5 rounded transition-colors shrink-0 cursor-pointer">
          Re-submit Work
        </button>
      </div>
    </div>

    <!-- Interactive Sprint Kanban Board (Spans 100% full width) -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-zinc-800">
        <div>
          <h2 class="text-base font-bold text-white">Sprint Kanban Board</h2>
          <p class="text-xs text-zinc-400">Full lifecycle pipeline across 14-day workflow stages</p>
        </div>

        <!-- Filter / Quick Action -->
        <div class="flex items-center gap-2">
          <button 
            v-if="authStore.isIntern"
            @click="filterMyTasksOnly = !filterMyTasksOnly"
            :class="['px-3 py-1.5 rounded text-xs font-bold transition-colors border cursor-pointer', filterMyTasksOnly ? 'bg-orange-500 text-black border-orange-400' : 'bg-zinc-950 text-zinc-300 border-zinc-700 hover:border-zinc-500 hover:text-white']">
            {{ filterMyTasksOnly ? 'Showing My Tasks' : 'Filter My Tasks' }}
          </button>
        </div>
      </div>

      <!-- Kanban 4 Columns Grid (Full Width) -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 w-full">
        
        <!-- 1. To Do Column -->
        <div class="bg-zinc-950 border border-zinc-800 rounded-md p-3.5 flex flex-col">
          <div class="flex items-center justify-between pb-2.5 mb-2.5 border-b border-zinc-800 text-xs">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-sm bg-zinc-500"></span>
              <span class="font-bold text-zinc-200">To Do</span>
            </div>
            <span class="font-mono text-zinc-400 font-bold">{{ displayTodoTasks.length }}</span>
          </div>
          <div class="space-y-2.5 flex-1 overflow-y-auto max-h-[620px]">
            <div v-if="displayTodoTasks.length === 0" class="py-6 text-center text-xs text-zinc-600">No tasks in To Do</div>
            <div 
              v-for="task in displayTodoTasks" 
              :key="task.id"
              class="bg-zinc-900 border border-zinc-800 rounded p-3 text-xs space-y-1.5 hover:border-zinc-700 transition-colors">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10px] text-orange-400 font-bold">{{ task.taskId }}</span>
                <span class="text-[10px] text-zinc-400 font-mono truncate max-w-[110px]">{{ task.assignedToName || 'Unassigned' }}</span>
              </div>
              <p class="font-medium text-white text-xs leading-snug">{{ task.title }}</p>
              
              <div class="pt-2 border-t border-zinc-800 flex items-center justify-between">
                <span class="text-[10px] text-zinc-500 font-mono">{{ task.track || 'General' }}</span>
                <button 
                  v-if="canOperateTask(task)"
                  @click="updateStatus(task, 'IN_PROGRESS')" 
                  class="text-[10px] font-semibold text-orange-400 hover:text-orange-300 underline cursor-pointer">
                  Start Work →
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. In Progress Column -->
        <div class="bg-zinc-950 border border-zinc-800 rounded-md p-3.5 flex flex-col">
          <div class="flex items-center justify-between pb-2.5 mb-2.5 border-b border-zinc-800 text-xs">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-sm bg-orange-500"></span>
              <span class="font-bold text-orange-400">In Progress</span>
            </div>
            <span class="font-mono text-orange-400 font-bold">{{ displayInProgressTasks.length }}</span>
          </div>
          <div class="space-y-2.5 flex-1 overflow-y-auto max-h-[620px]">
            <div v-if="displayInProgressTasks.length === 0" class="py-6 text-center text-xs text-zinc-600">No active tasks</div>
            <div 
              v-for="task in displayInProgressTasks" 
              :key="task.id"
              class="bg-zinc-900 border border-zinc-800 rounded p-3 text-xs space-y-1.5 hover:border-zinc-700 transition-colors">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10px] text-orange-400 font-bold">{{ task.taskId }}</span>
                <span class="text-[10px] text-zinc-300 font-mono truncate max-w-[110px]">{{ task.assignedToName || 'Intern' }}</span>
              </div>
              <p class="font-medium text-white text-xs leading-snug">{{ task.title }}</p>
              
              <div v-if="task.reviewNotes" class="bg-zinc-950 p-1.5 rounded text-[10px] text-orange-300/90 border border-orange-500/20">
                Rework: {{ task.reviewNotes }}
              </div>

              <div class="pt-2 border-t border-zinc-800 flex items-center justify-between text-[10px]">
                <button 
                  v-if="canOperateTask(task)"
                  @click="updateStatus(task, 'TODO')" 
                  class="text-zinc-500 hover:text-zinc-300 cursor-pointer">
                  ← Back
                </button>
                <button 
                  v-if="canOperateTask(task)"
                  @click="openSubmitModal(task)" 
                  class="text-orange-400 hover:text-orange-300 underline font-bold cursor-pointer">
                  Submit Work →
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Pending Review Column -->
        <div class="bg-zinc-950 border border-zinc-800 rounded-md p-3.5 flex flex-col">
          <div class="flex items-center justify-between pb-2.5 mb-2.5 border-b border-zinc-800 text-xs">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-sm bg-white"></span>
              <span class="font-bold text-white">Pending Review</span>
            </div>
            <span class="font-mono text-white font-bold">{{ displayPendingReviewTasks.length }}</span>
          </div>
          <div class="space-y-2.5 flex-1 overflow-y-auto max-h-[620px]">
            <div v-if="displayPendingReviewTasks.length === 0" class="py-6 text-center text-xs text-zinc-600">No tasks in review</div>
            <div 
              v-for="task in displayPendingReviewTasks" 
              :key="task.id"
              class="bg-zinc-900 border border-zinc-800 rounded p-3 text-xs space-y-1.5">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10px] text-orange-400 font-bold">{{ task.taskId }}</span>
                <span class="text-[10px] text-zinc-300 font-mono truncate max-w-[110px]">{{ task.assignedToName }}</span>
              </div>
              <p class="font-medium text-white text-xs leading-snug">{{ task.title }}</p>
              
              <div v-if="task.submissionNotes" class="bg-zinc-950 p-2 rounded text-[10px] text-zinc-300 border border-zinc-800">
                <span class="text-zinc-400 font-medium">Notes:</span> {{ task.submissionNotes }}
                <div v-if="task.submissionLink" class="mt-1">
                  <a :href="task.submissionLink" target="_blank" class="text-orange-400 hover:text-orange-300 underline font-mono text-[10px]">View PR Link</a>
                </div>
              </div>

              <!-- Action for Scrum Head / Admin -->
              <div v-if="canReviewTask" class="pt-2 border-t border-zinc-800 flex items-center justify-between">
                <button @click="openRejectModal(task)" class="text-[10px] text-zinc-400 hover:text-red-400 cursor-pointer">Reject</button>
                <button @click="approveTask(task)" class="text-[10px] font-bold text-white hover:text-orange-400 hover:underline cursor-pointer">Approve</button>
              </div>
              <div v-else class="pt-2 border-t border-zinc-800 text-[10px] text-zinc-500 italic">
                Awaiting Lead Review
              </div>
            </div>
          </div>
        </div>

        <!-- 4. Approved Column -->
        <div class="bg-zinc-950 border border-zinc-800 rounded-md p-3.5 flex flex-col">
          <div class="flex items-center justify-between pb-2.5 mb-2.5 border-b border-zinc-800 text-xs">
            <div class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-sm bg-zinc-400"></span>
              <span class="font-bold text-zinc-200">Approved</span>
            </div>
            <span class="font-mono text-zinc-400 font-bold">{{ displayApprovedTasks.length }}</span>
          </div>
          <div class="space-y-2.5 flex-1 overflow-y-auto max-h-[620px]">
            <div v-if="displayApprovedTasks.length === 0" class="py-6 text-center text-xs text-zinc-600">No completed tasks yet</div>
            <div 
              v-for="task in displayApprovedTasks" 
              :key="task.id"
              class="bg-zinc-900 border border-zinc-800 rounded p-3 text-xs space-y-1">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[10px] text-orange-400 font-bold">{{ task.taskId }}</span>
                <span class="text-[10px] text-zinc-400 font-mono truncate max-w-[110px]">{{ task.assignedToName }}</span>
              </div>
              <p class="font-medium text-zinc-200 text-xs leading-snug">{{ task.title }}</p>
              <p class="text-[10px] text-zinc-500 font-mono">Approved by {{ task.reviewedByName || 'Lead' }}</p>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Modal: Intern Work Submission -->
    <div v-if="submittingTask" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <div>
            <span class="font-mono text-xs font-bold text-zinc-400">{{ submittingTask.taskId }}</span>
            <h3 class="text-base font-bold text-white">Submit Work for Review</h3>
          </div>
          <button @click="submittingTask = null" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Submission Notes</label>
          <textarea 
            v-model="submitNotes"
            rows="3"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="Explain what was implemented and test results...">
          </textarea>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">PR / Repository Link</label>
          <input 
            type="text" 
            v-model="submitLink"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none font-mono"
            placeholder="https://github.com/..."
          />
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="submittingTask = null" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="confirmSubmit"
            :disabled="!submitNotes.trim()"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Submit for Review
          </button>
        </div>
      </div>
    </div>

    <!-- Modal: Reject with Rework Feedback -->
    <div v-if="rejectingTask" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <div>
            <span class="font-mono text-xs font-bold text-orange-400">{{ rejectingTask.taskId }}</span>
            <h3 class="text-base font-bold text-white">Return Task for Rework</h3>
          </div>
          <button @click="rejectingTask = null" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Feedback & Instructions</label>
          <textarea 
            v-model="rejectFeedback"
            rows="4"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="Explain specifically what needs to be changed...">
          </textarea>
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="rejectingTask = null" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="confirmReject"
            :disabled="!rejectFeedback.trim()"
            class="bg-white hover:bg-zinc-200 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Return for Rework
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

const selectedSprintId = ref(null)
const filterMyTasksOnly = ref(false)

const submittingTask = ref(null)
const submitNotes = ref('')
const submitLink = ref('')

const rejectingTask = ref(null)
const rejectFeedback = ref('')

const activeSprint = computed(() => {
  if (selectedSprintId.value) {
    return scrumStore.sprints.find(s => s.id === selectedSprintId.value) || scrumStore.activeSprint
  }
  return scrumStore.activeSprint
})

const sprintTasks = computed(() => {
  if (!activeSprint.value) return scrumStore.tasks
  return scrumStore.tasks.filter(t => t.sprintId === activeSprint.value.id)
})

const filteredTasks = computed(() => {
  if (filterMyTasksOnly.value && authStore.user?.id) {
    return sprintTasks.value.filter(t => t.assignedToId === authStore.user.id)
  }
  return sprintTasks.value
})

const todoTasks = computed(() => sprintTasks.value.filter(t => t.status === 'TODO'))
const inProgressTasks = computed(() => sprintTasks.value.filter(t => t.status === 'IN_PROGRESS'))
const pendingReviewTasks = computed(() => sprintTasks.value.filter(t => t.status === 'PENDING_APPROVAL'))
const approvedTasks = computed(() => sprintTasks.value.filter(t => t.status === 'APPROVED' || t.status === 'DONE'))

const displayTodoTasks = computed(() => filteredTasks.value.filter(t => t.status === 'TODO'))
const displayInProgressTasks = computed(() => filteredTasks.value.filter(t => t.status === 'IN_PROGRESS'))
const displayPendingReviewTasks = computed(() => filteredTasks.value.filter(t => t.status === 'PENDING_APPROVAL'))
const displayApprovedTasks = computed(() => filteredTasks.value.filter(t => t.status === 'APPROVED' || t.status === 'DONE'))

const sprintProgressPercentage = computed(() => {
  if (sprintTasks.value.length === 0) return 0
  return Math.round((approvedTasks.value.length / sprintTasks.value.length) * 100)
})

const myReworkTasks = computed(() => {
  if (!authStore.user?.id) return []
  return scrumStore.tasks.filter(t => t.assignedToId === authStore.user.id && t.status === 'IN_PROGRESS' && t.reviewNotes)
})

const canOperateTask = (task) => {
  if (authStore.isViewOnly) return false
  if (authStore.canManageScrum || authStore.canAccessAdmin) return true
  return task.assignedToId === authStore.user?.id
}

const canReviewTask = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin
})

const onSprintChange = () => {
  if (selectedSprintId.value) {
    scrumStore.fetchTasks(selectedSprintId.value)
  }
}

const updateStatus = async (task, newStatus) => {
  await scrumStore.updateTaskStatus(task.id, newStatus, authStore.user?.id)
  await scrumStore.fetchTasks(activeSprint.value?.id)
}

const openSubmitModal = (task) => {
  submittingTask.value = task
  submitNotes.value = ''
  submitLink.value = ''
}

const confirmSubmit = async () => {
  if (!submittingTask.value || !submitNotes.value.trim()) return
  await scrumStore.submitTask(submittingTask.value.id, submitNotes.value, submitLink.value, authStore.user?.id)
  submittingTask.value = null
  await scrumStore.fetchTasks(activeSprint.value?.id)
}

const openRejectModal = (task) => {
  rejectingTask.value = task
  rejectFeedback.value = ''
}

const confirmReject = async () => {
  if (!rejectingTask.value || !rejectFeedback.value.trim()) return
  await scrumStore.reviewTask(rejectingTask.value.id, 'REJECTED', rejectFeedback.value, authStore.user?.id)
  rejectingTask.value = null
  await scrumStore.fetchTasks(activeSprint.value?.id)
}

const approveTask = async (task) => {
  await scrumStore.reviewTask(task.id, 'APPROVED', 'Approved by lead', authStore.user?.id)
  await scrumStore.fetchTasks(activeSprint.value?.id)
}

onMounted(async () => {
  await scrumStore.fetchSprints()
  if (scrumStore.activeSprint?.id) {
    selectedSprintId.value = scrumStore.activeSprint.id
    await scrumStore.fetchTasks(scrumStore.activeSprint.id)
  } else {
    await scrumStore.fetchTasks()
  }
})
</script>
