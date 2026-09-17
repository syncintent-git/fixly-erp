<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>AUDIT & COMPLIANCE</span>
            <span>•</span>
            <span>{{ auditLogs.length }} Events</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">System Audit Trail</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Immutable record of all state transitions, task approvals, rework orders, and applicant decisions.</p>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
      <div class="flex items-center gap-2 flex-1 min-w-[240px]">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Filter audit logs by actor, action or detail..." 
          class="w-full bg-transparent text-xs text-white placeholder-zinc-500 outline-none"
        />
      </div>

      <div class="flex items-center gap-3">
        <select v-model="filterEntityType" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs text-zinc-300 outline-none cursor-pointer">
          <option value="">All Entities</option>
          <option value="TASK">Tasks</option>
          <option value="USER">Users</option>
          <option value="SPRINT">Sprints</option>
          <option value="STORY">Stories</option>
        </select>
      </div>
    </div>

    <!-- Audit Logs Table -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden w-full">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-zinc-300">
          <thead class="bg-zinc-950 text-[10px] uppercase font-mono tracking-wider text-zinc-400 border-b border-zinc-800">
            <tr>
              <th class="py-3 px-4 font-bold">Timestamp</th>
              <th class="py-3 px-4 font-bold">Action</th>
              <th class="py-3 px-4 font-bold">Entity</th>
              <th class="py-3 px-4 font-bold">Actor</th>
              <th class="py-3 px-4 font-bold">Details</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-zinc-800 font-mono text-[11px]">
            <tr v-if="filteredAuditLogs.length === 0">
              <td colspan="5" class="py-8 text-center text-zinc-500 italic">No audit records found matching filters.</td>
            </tr>
            <tr 
              v-for="log in filteredAuditLogs" 
              :key="log.id"
              class="hover:bg-zinc-850 transition-colors">
              <td class="py-2.5 px-4 text-zinc-400 shrink-0">{{ formatTime(log.createdAt || log.timestamp) }}</td>
              <td class="py-2.5 px-4">
                <span class="text-[10px] uppercase px-2 py-0.5 rounded-full border border-zinc-700 bg-zinc-950 text-zinc-300">
                  {{ log.action }}
                </span>
              </td>
              <td class="py-2.5 px-4 text-zinc-300">{{ log.entityType }}</td>
              <td class="py-2.5 px-4 text-white font-medium">{{ log.actorName || log.userName || 'System' }}</td>
              <td class="py-2.5 px-4 text-zinc-300 font-sans text-xs">{{ log.details }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useScrumStore } from '../../stores/scrum'

const scrumStore = useScrumStore()

const searchQuery = ref('')
const filterEntityType = ref('')

const auditLogs = computed(() => scrumStore.auditLogs)

const filteredAuditLogs = computed(() => {
  return auditLogs.value.filter(l => {
    const matchEntity = !filterEntityType.value || (l.entityType || '').toUpperCase() === filterEntityType.value
    const actor = l.actorName || l.userName || ''
    const matchSearch = !searchQuery.value ||
      (l.action && l.action.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (actor && actor.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (l.details && l.details.toLowerCase().includes(searchQuery.value.toLowerCase()))
    return matchEntity && matchSearch
  })
})

const formatTime = (ts) => {
  if (!ts) return ''
  return new Date(ts).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  scrumStore.fetchAuditLogs()
})
</script>
