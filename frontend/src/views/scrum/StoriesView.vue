<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>SCRUM BACKLOG</span>
            <span>•</span>
            <span>{{ filteredStories.length }} User Stories</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">User Stories Backlog</h1>
          <p class="text-xs text-zinc-400 mt-0.5">High-level user stories, deliverables, and acceptance criteria.</p>
        </div>

        <div v-if="canManageStories" class="shrink-0">
          <button 
            @click="showCreateModal = true"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Create Story</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Filter & Search Bar -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
      <div class="flex items-center gap-2 flex-1 min-w-[240px]">
        <svg class="w-4 h-4 text-zinc-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search stories by title or ID..." 
          class="w-full bg-transparent text-xs text-white placeholder-zinc-500 outline-none"
        />
      </div>

      <div class="flex items-center gap-3">
        <select v-model="filterPriority" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs text-zinc-300 outline-none cursor-pointer">
          <option value="">All Priorities</option>
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
          <option value="URGENT">Urgent</option>
        </select>
      </div>
    </div>

    <!-- Stories List -->
    <div v-if="filteredStories.length === 0" class="bg-zinc-900/60 border border-zinc-800 rounded-lg p-10 text-center text-zinc-500 w-full">
      <p class="font-medium text-sm text-zinc-400">No stories found</p>
      <p class="text-xs text-zinc-600 mt-0.5">Create a user story or adjust your search filters.</p>
    </div>

    <div v-else class="space-y-3 w-full">
      <div 
        v-for="story in filteredStories" 
        :key="story.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-4 space-y-2.5 hover:border-zinc-700 transition-colors w-full">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
          <div class="flex flex-wrap items-center gap-2">
            <span class="font-mono text-xs font-bold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded border border-orange-500/30">
              {{ story.storyId }}
            </span>
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-700 bg-zinc-950 text-zinc-300">
              {{ story.priority }} Priority
            </span>
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-700 bg-zinc-950 text-zinc-300">
              {{ story.status }}
            </span>
          </div>

          <div class="flex items-center gap-1.5 text-xs text-zinc-400">
            <span>Lead:</span>
            <span class="font-medium text-zinc-200">{{ story.assignedToName || 'Unassigned' }}</span>
          </div>
        </div>

        <h3 class="text-sm font-semibold text-white">{{ story.title }}</h3>
        <p v-if="story.description" class="text-xs text-zinc-400 leading-relaxed">{{ story.description }}</p>

        <!-- Associated Subtasks Summary -->
        <div class="pt-2.5 border-t border-zinc-800 flex flex-wrap items-center justify-between gap-2 text-xs">
          <div class="flex items-center gap-2 text-zinc-400">
            <span>Subtasks: <strong class="text-zinc-200">{{ getStoryTaskCount(story.id) }}</strong></span>
          </div>

          <button 
            @click="toggleStoryExpand(story.id)" 
            class="text-[11px] font-medium text-zinc-300 hover:text-white underline cursor-pointer">
            {{ expandedStories.includes(story.id) ? 'Hide Subtasks' : 'View Subtasks' }}
          </button>
        </div>

        <!-- Expanded Subtasks List -->
        <div v-if="expandedStories.includes(story.id)" class="pt-2 space-y-1.5">
          <div 
            v-for="task in getStoryTasks(story.id)" 
            :key="task.id"
            class="bg-zinc-950 p-2.5 rounded border border-zinc-800 flex items-center justify-between text-xs">
            <div class="flex items-center gap-2.5">
              <span class="font-mono text-[10px] text-zinc-400 font-bold">{{ task.taskId }}</span>
              <span class="font-medium text-zinc-200">{{ task.title }}</span>
            </div>
            <div class="flex items-center gap-2.5">
              <span class="text-[10px] text-zinc-400 font-mono">{{ task.assignedToName }}</span>
              <span class="text-[9px] font-mono uppercase px-2 py-0.5 rounded-full border border-zinc-800 bg-zinc-900 text-zinc-400">
                {{ task.status }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Create Story Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Create User Story</h3>
          <button @click="showCreateModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Story Title</label>
          <input 
            type="text" 
            v-model="newTitle"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="e.g. Implement Google GIS Sign-In with Role Selection"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Priority</label>
            <select v-model="newPriority" class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
              <option value="URGENT">Urgent</option>
            </select>
          </div>
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Assign Lead Intern</label>
            <select v-model="newAssignee" class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
              <option :value="null">Unassigned</option>
              <option v-for="user in internList" :key="user.id" :value="user.id">{{ user.name }}</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1.5">Story Description</label>
          <textarea 
            v-model="newDesc"
            rows="3"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-xs text-white placeholder-zinc-500 focus:border-zinc-500 outline-none"
            placeholder="Acceptance criteria and deliverables...">
          </textarea>
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="showCreateModal = false" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="handleCreateStory"
            :disabled="!newTitle.trim()"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Create Story
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

const searchQuery = ref('')
const filterPriority = ref('')
const showCreateModal = ref(false)
const expandedStories = ref([])

const newTitle = ref('')
const newDesc = ref('')
const newPriority = ref('MEDIUM')
const newAssignee = ref(null)

const internList = ref([])

const canManageStories = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin
})

const filteredStories = computed(() => {
  return scrumStore.stories.filter(s => {
    const matchQuery = !searchQuery.value || 
      s.title.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
      (s.storyId && s.storyId.toLowerCase().includes(searchQuery.value.toLowerCase()))
    const matchPri = !filterPriority.value || s.priority === filterPriority.value
    return matchQuery && matchPri
  })
})

const toggleStoryExpand = (id) => {
  if (expandedStories.value.includes(id)) {
    expandedStories.value = expandedStories.value.filter(x => x !== id)
  } else {
    expandedStories.value.push(id)
  }
}

const getStoryTaskCount = (storyId) => {
  return scrumStore.tasks.filter(t => t.storyId === storyId).length
}

const getStoryTasks = (storyId) => {
  return scrumStore.tasks.filter(t => t.storyId === storyId)
}

const handleCreateStory = async () => {
  if (!newTitle.value.trim()) return
  await scrumStore.createStory({
    title: newTitle.value.trim(),
    description: newDesc.value.trim(),
    priority: newPriority.value,
    assignedToId: newAssignee.value,
    sprintId: scrumStore.activeSprint?.id || null
  }, authStore.user?.id)

  newTitle.value = ''
  newDesc.value = ''
  newPriority.value = 'MEDIUM'
  newAssignee.value = null
  showCreateModal.value = false
  await scrumStore.fetchStories()
}

onMounted(async () => {
  await scrumStore.fetchStories()
  await scrumStore.fetchTasks()

  try {
    const res = await fetch(`${getApiBase()}/api/users/all`)
    if (res.ok) {
      const all = await res.json()
      internList.value = all.filter(u => ['frontend_developer', 'backend_developer', 'devops_developer', 'intern'].includes(u.role?.toLowerCase()))
    }
  } catch (err) {
    console.error('Error fetching interns:', err)
  }
})
</script>
