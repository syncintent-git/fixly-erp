<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>QUALITY ASSURANCE</span>
            <span>•</span>
            <span>{{ pendingTasks.length }} Awaiting Review</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Task Review Queue</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Review work submitted by interns. Approve to mark complete or reject to request rework.</p>
        </div>
      </div>
    </div>

    <!-- Review Queue Items -->
    <div v-if="pendingTasks.length === 0" class="bg-zinc-900/60 border border-zinc-800 rounded-lg p-10 text-center text-zinc-500 w-full">
      <p class="font-medium text-sm text-zinc-300">All submissions are reviewed</p>
      <p class="text-xs text-zinc-600 mt-0.5">No tasks are currently waiting for your review.</p>
    </div>

    <div v-else class="space-y-3 w-full">
      <div 
        v-for="task in pendingTasks" 
        :key="task.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 hover:border-zinc-700 transition-colors w-full">
        
        <div class="space-y-1.5 flex-1">
          <div class="flex flex-wrap items-center gap-2">
            <span class="font-mono text-xs font-bold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded border border-orange-500/30">
              {{ task.taskId }}
            </span>
            <span class="text-xs text-zinc-300">
              Submitted by: <strong class="text-white">{{ task.assignedToName || 'Intern' }}</strong>
            </span>
            <span class="text-zinc-600">•</span>
            <span class="text-xs text-zinc-400">Story: {{ task.storyTitle || 'User Story' }}</span>
          </div>

          <h3 class="text-sm font-semibold text-white">{{ task.title }}</h3>
          <p v-if="task.description" class="text-xs text-zinc-400">{{ task.description }}</p>

          <div class="bg-zinc-950 border border-zinc-800 rounded p-3 text-xs text-zinc-300 space-y-1">
            <div>
              <span class="text-zinc-400 font-medium">Submission Notes:</span> 
              <span class="text-zinc-200 ml-1">{{ task.submissionNotes || 'No notes provided.' }}</span>
            </div>
            <div v-if="task.submissionLink" class="pt-1 border-t border-zinc-800 font-mono text-[11px]">
              <a :href="task.submissionLink" target="_blank" class="text-orange-400 hover:text-orange-300 underline inline-flex items-center gap-1">
                <span>View PR Link</span>
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
              </a>
            </div>
          </div>
        </div>

        <!-- Decision Buttons -->
        <div v-if="canReview" class="flex items-center gap-2 shrink-0">
          <button 
            @click="openRejectModal(task)"
            class="bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white border border-zinc-700 text-xs font-semibold px-3.5 py-1.5 rounded transition-colors cursor-pointer">
            Reject & Rework
          </button>

          <button 
            @click="handleApprove(task)"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-1.5 rounded transition-colors cursor-pointer">
            Approve Work
          </button>
        </div>
        <div v-else class="text-xs text-zinc-500 italic">
          Reviewer View Only
        </div>

      </div>
    </div>

    <!-- Reject Modal -->
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
            Return to Intern
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

const rejectingTask = ref(null)
const rejectFeedback = ref('')

const canReview = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin
})

const pendingTasks = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'PENDING_APPROVAL')
})

const handleApprove = async (task) => {
  await scrumStore.reviewTask(task.id, 'APPROVED', 'Work verified and approved by lead', authStore.user?.id)
  await scrumStore.fetchTasks()
}

const openRejectModal = (task) => {
  rejectingTask.value = task
  rejectFeedback.value = ''
}

const confirmReject = async () => {
  if (!rejectingTask.value || !rejectFeedback.value.trim()) return
  await scrumStore.reviewTask(rejectingTask.value.id, 'REJECTED', rejectFeedback.value, authStore.user?.id)
  rejectingTask.value = null
  rejectFeedback.value = ''
  await scrumStore.fetchTasks()
}

onMounted(() => {
  scrumStore.fetchTasks()
})
</script>
