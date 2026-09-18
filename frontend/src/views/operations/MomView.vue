<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>GOVERNANCE & RECORDS</span>
            <span>•</span>
            <span>{{ allMoMs.length }} Meetings</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Minutes of Meeting (MoM)</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Review meeting agendas, decisions, attendee records, and official attachments.</p>
        </div>

        <div v-if="canCreateMoM" class="shrink-0">
          <button 
            @click="showCreateModal = true"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Record New MoM</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MoM Entries List -->
    <div v-if="allMoMs.length === 0" class="bg-zinc-900/60 border border-zinc-800 rounded-lg p-10 text-center text-zinc-500 w-full">
      <p class="font-medium text-sm text-zinc-400">No meeting minutes recorded yet</p>
      <p class="text-xs text-zinc-600 mt-0.5">Record a meeting summary to establish governance records.</p>
    </div>

    <div v-else class="space-y-3 w-full">
      <div 
        v-for="mom in allMoMs" 
        :key="mom.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 space-y-3 hover:border-zinc-700 transition-colors w-full">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 pb-2.5 border-b border-zinc-800">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="bg-zinc-950 text-zinc-400 border border-zinc-800 text-[10px] font-mono px-2 py-0.5 rounded-full">
                {{ mom.team || 'All Hands' }}
              </span>
              <span class="text-xs font-mono text-zinc-500">{{ mom.date }}</span>
            </div>
            <h2 class="text-base font-bold text-white">{{ mom.title }}</h2>
          </div>

          <div class="flex items-center gap-2 text-xs text-zinc-400">
            <span>Recorded by: <strong class="text-zinc-200">{{ mom.author_name || 'Unassigned' }}</strong></span>
          </div>
        </div>

        <!-- Agenda & Attendees -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs">
          <div v-if="mom.agenda" class="bg-zinc-950 p-2.5 rounded border border-zinc-800">
            <span class="text-[10px] uppercase font-bold text-zinc-400">Agenda:</span>
            <p class="text-zinc-300 mt-0.5">{{ mom.agenda }}</p>
          </div>
          <div v-if="mom.attendees" class="bg-zinc-950 p-2.5 rounded border border-zinc-800">
            <span class="text-[10px] uppercase font-bold text-zinc-400">Attendees:</span>
            <p class="text-zinc-300 mt-0.5">{{ mom.attendees }}</p>
          </div>
        </div>

        <!-- Rich Content View -->
        <div class="bg-zinc-950 p-3.5 rounded border border-zinc-800 text-xs text-zinc-200 leading-relaxed overflow-hidden">
          <div v-html="mom.content" class="prose prose-invert prose-xs max-w-none"></div>
        </div>

        <!-- Attachment Link -->
        <div v-if="mom.file_name" class="pt-2 flex items-center justify-between text-xs border-t border-zinc-800">
          <div class="flex items-center gap-2 text-zinc-400">
            <span>Attachment: <strong class="text-zinc-200">{{ mom.file_name }}</strong></span>
          </div>
          <button 
            @click="previewMoM(mom.id)"
            class="text-zinc-300 hover:text-white underline font-medium cursor-pointer">
            Preview Document →
          </button>
        </div>

      </div>
    </div>

    <!-- Create MoM Modal with Quill -->
    <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 overflow-y-auto">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-2xl w-full shadow-xl space-y-4 my-8">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white">Record Minutes of Meeting</h3>
          <button @click="showCreateModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Meeting Title</label>
            <input 
              type="text" 
              v-model="newTitle" 
              placeholder="e.g. Sprint 07 Architecture Alignment"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none"
            />
          </div>
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Department / Team</label>
            <input 
              type="text" 
              v-model="newTeam" 
              placeholder="e.g. Engineering All-Hands"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Meeting Date</label>
            <input 
              type="date" 
              v-model="newDate" 
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer"
            />
          </div>
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Attendees</label>
            <input 
              type="text" 
              v-model="newAttendees" 
              placeholder="Abhijeet, Karthik, Rahul, Alex..."
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none"
            />
          </div>
        </div>

        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Agenda</label>
          <input 
            type="text" 
            v-model="newAgenda" 
            placeholder="Review backlog, assign GIS task, discuss deployment blockers"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none"
          />
        </div>

        <!-- Rich Text Notes -->
        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Meeting Notes & Action Items</label>
          <div class="bg-zinc-950 border border-zinc-700 rounded overflow-hidden text-white min-h-[160px]">
            <QuillEditor 
              theme="snow" 
              v-model:content="newContent" 
              contentType="html" 
              placeholder="Record key decisions, action items, assignees, and deadlines..."
            />
          </div>
        </div>

        <!-- File Attachment -->
        <div>
          <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Attach Document (Optional)</label>
          <input 
            type="file" 
            @change="handleFileUpload"
            class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-zinc-400 file:mr-3 file:py-1 file:px-2.5 file:rounded file:border-0 file:text-xs file:font-medium file:bg-zinc-800 file:text-zinc-200 cursor-pointer"
          />
        </div>

        <div class="flex items-center justify-end gap-2.5 pt-3">
          <button @click="showCreateModal = false" class="px-3 py-1.5 text-xs font-medium text-zinc-400 hover:text-white rounded cursor-pointer">Cancel</button>
          <button 
            @click="submitMoM"
            :disabled="!newTitle.trim() || !newContent"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors cursor-pointer disabled:opacity-50">
            Save Minutes
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
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const authStore = useAuthStore()


const allMoMs = ref([])
const showCreateModal = ref(false)

const newTitle = ref('')
const newTeam = ref('')
const newDate = ref(new Date().toISOString().split('T')[0])
const newAttendees = ref('')
const newAgenda = ref('')
const newContent = ref('')
const attachedFile = ref(null)

const canCreateMoM = computed(() => {
  if (authStore.isViewOnly) return false
  return authStore.canManageScrum || authStore.canAccessAdmin || !authStore.isIntern
})

const handleFileUpload = (e) => {
  if (e.target.files?.length > 0) {
    attachedFile.value = e.target.files[0]
  }
}

const previewMoM = (id) => {
  window.open(`${getApiBase()}/api/moms/view/${id}`, '_blank')
}

const fetchMoMs = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/moms/all`)
    if (res.ok) {
      allMoMs.value = await res.json()
    }
  } catch (err) {
    console.error('Error fetching MoMs:', err)
  }
}

const submitMoM = async () => {
  if (!newTitle.value.trim() || !newContent.value) return

  const formData = new FormData()
  formData.append('title', newTitle.value.trim())
  formData.append('team', newTeam.value.trim() || 'All Teams')
  formData.append('date', newDate.value)
  formData.append('attendees', newAttendees.value.trim())
  formData.append('agenda', newAgenda.value.trim())
  formData.append('content', newContent.value)
  formData.append('author_name', authStore.user?.name || authStore.user?.email || 'Anonymous')

  if (attachedFile.value) {
    formData.append('file', attachedFile.value)
  }

  try {
    const res = await fetch(`${getApiBase()}/api/moms/create`, {
      method: 'POST',
      body: formData
    })
    if (res.ok) {
      newTitle.value = ''
      newTeam.value = ''
      newAttendees.value = ''
      newAgenda.value = ''
      newContent.value = ''
      attachedFile.value = null
      showCreateModal.value = false
      await fetchMoMs()
    }
  } catch (err) {
    console.error('Error creating MoM:', err)
  }
}

onMounted(() => {
  fetchMoMs()
})
</script>
