<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>IDENTITY & ACCESS</span>
            <span>•</span>
            <span>{{ pendingUsers.length }} Requests</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Access Requests & Onboarding</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Review new signups, verify requested tracks, assign departments, and approve accounts.</p>
        </div>
      </div>
    </div>

    <!-- Reviewer Alert -->
    <div v-if="authStore.isViewOnly" class="bg-zinc-900 border border-zinc-800 p-3 rounded text-xs text-zinc-400">
      Reviewer Mode Active: Access requests can only be approved or rejected by administrative accounts (CEO, CTO, Admin).
    </div>

    <!-- Requests Queue -->
    <div v-if="pendingUsers.length === 0" class="bg-zinc-900/60 border border-zinc-800 rounded-lg p-10 text-center text-zinc-500 w-full">
      <p class="font-medium text-sm text-zinc-400">No pending access requests</p>
      <p class="text-xs text-zinc-600 mt-0.5">All applicant onboarding requests have been reviewed.</p>
    </div>

    <div v-else class="space-y-3 w-full">
      <div 
        v-for="user in pendingUsers" 
        :key="user.id"
        class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 space-y-3 hover:border-zinc-700 transition-colors w-full">
        
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded bg-orange-500/10 border border-orange-500/30 text-orange-400 font-bold flex items-center justify-center text-sm">
              {{ (user.name || 'U').charAt(0) }}
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-sm font-semibold text-white">{{ user.name }}</h3>
                <span class="font-mono text-xs text-zinc-500">({{ user.email }})</span>
              </div>
              <p class="text-xs text-zinc-300 mt-0.5">
                Requested: <span class="font-mono text-orange-400 font-bold">{{ formatRole(user.requestedRole) }}</span>
              </p>
            </div>
          </div>

          <span class="text-[10px] font-mono uppercase bg-orange-500/10 text-orange-400 border border-orange-500/30 px-2 py-0.5 rounded shrink-0 font-bold">
            Pending Approval
          </span>
        </div>

        <!-- Role & Team Customization Form -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-3 border-t border-zinc-800 text-xs">
          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Approved Role</label>
            <select 
              v-model="user.approvedRole"
              :disabled="authStore.isViewOnly"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
              <option value="frontend_developer">Frontend Developer Intern</option>
              <option value="backend_developer">Backend Developer Intern</option>
              <option value="devops_developer">DevOps Developer Intern</option>
              <option value="intern">Engineering Intern</option>
              <option value="scrum_head">Scrum Head</option>
            </select>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Assigned Department</label>
            <select 
              v-model="user.assignedTeam"
              :disabled="authStore.isViewOnly"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none cursor-pointer">
              <option value="">-- Select Team / Department --</option>
              <option v-for="team in dbTeams" :key="team.id || team.name" :value="team.name">
                {{ team.name }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Position Title</label>
            <input 
              type="text" 
              v-model="user.positionTitle"
              :disabled="authStore.isViewOnly"
              placeholder="e.g. Frontend Developer Intern"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2 text-xs text-white focus:border-zinc-500 outline-none"
            />
          </div>
        </div>

        <!-- Approval Actions -->
        <div v-if="!authStore.isViewOnly" class="pt-2.5 flex items-center justify-end gap-2.5 border-t border-zinc-800">
          <button 
            @click="handleReject(user)"
            class="bg-zinc-800 hover:bg-zinc-750 text-zinc-400 hover:text-red-400 border border-zinc-700 text-xs font-medium px-3 py-1.5 rounded transition-colors cursor-pointer">
            Reject
          </button>
          <button 
            @click="handleApprove(user)"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-1.5 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <span>Approve & Activate</span>
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
import { formatRoleTitle } from '../../constants'
import { getApiBase } from '../../config'

const authStore = useAuthStore()
const scrumStore = useScrumStore()
const dbTeams = ref([])

const pendingUsers = computed(() => {
  return scrumStore.pendingUsers.map(u => ({
    ...u,
    approvedRole: u.requestedRole || 'intern',
    assignedTeam: u.team || '',
    positionTitle: u.positionTitle || formatRoleTitle(u.requestedRole || 'intern')
  }))
})

const formatRole = (role) => {
  return formatRoleTitle(role)
}

const handleApprove = async (user) => {
  await scrumStore.approveUser(user.id, {
    role: user.approvedRole,
    team: user.assignedTeam,
    positionTitle: user.positionTitle
  }, authStore.user?.id)
  await scrumStore.fetchPendingUsers()
}

const handleReject = async (user) => {
  await scrumStore.rejectUser(user.id, authStore.user?.id)
  await scrumStore.fetchPendingUsers()
}

onMounted(async () => {
  scrumStore.fetchPendingUsers()
  try {
    const res = await fetch(`${getApiBase()}/api/teams`)
    if (res.ok) {
      dbTeams.value = await res.json()
    }
  } catch (err) {
    console.error('Failed to load teams:', err)
  }
})
</script>
