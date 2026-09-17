<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>WORKFORCE AUDIT</span>
            <span>•</span>
            <span>{{ attendanceRecords.length }} Records</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Attendance Records & Reports</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Audit daily presence, track office vs remote status, and export official attendance PDFs.</p>
        </div>

        <!-- Export Buttons -->
        <div class="flex flex-wrap items-center gap-2.5 shrink-0">
          <button 
            @click="copyAttendanceList"
            class="bg-white hover:bg-zinc-200 text-black font-bold text-xs px-3.5 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
            <span>{{ copied ? 'Copied' : 'Copy List' }}</span>
          </button>

          <button 
            @click="exportCSV"
            class="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 hover:text-white border border-zinc-700 text-xs font-semibold px-3.5 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>Export CSV</span>
          </button>

          <button 
            @click="generateAttendancePDF"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>Export PDF</span>
          </button>
        </div>
      </div>

      <!-- KPI Summary Cards -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 mt-4 border-t border-zinc-800">
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Total Logged</span>
          <p class="text-xl font-bold text-white mt-0.5">{{ attendanceRecords.length }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">In-Office</span>
          <p class="text-xl font-black text-orange-400 mt-0.5">{{ officeCount }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Remote / WFH</span>
          <p class="text-lg font-bold text-zinc-200 mt-0.5">{{ remoteCount }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">On-Duty / Field</span>
          <p class="text-lg font-bold text-zinc-200 mt-0.5">{{ fieldCount }}</p>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
      <div class="flex items-center gap-2 text-xs">
        <span class="text-zinc-500 font-mono uppercase">Filter Date:</span>
        <input 
          type="date" 
          v-model="selectedDate" 
          class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs font-mono text-white outline-none cursor-pointer"
        />
        <button 
          v-if="selectedDate"
          @click="selectedDate = ''"
          class="text-xs text-zinc-400 hover:text-white underline cursor-pointer ml-1">
          Clear
        </button>
      </div>

      <div class="flex items-center gap-3">
        <select v-model="filterTeam" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1 text-xs text-zinc-300 outline-none cursor-pointer">
          <option value="">All Departments</option>
          <option value="Frontend">Frontend</option>
          <option value="Backend">Backend</option>
          <option value="DevOps">DevOps</option>
          <option value="Mobile">Mobile</option>
          <option value="QA">QA</option>
          <option value="Design">Design</option>
        </select>
      </div>
    </div>

    <!-- Attendance Records Table -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden w-full">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-zinc-300">
          <thead class="bg-zinc-950 text-[10px] uppercase font-mono tracking-wider text-zinc-400 border-b border-zinc-800">
            <tr>
              <th class="py-3 px-4 font-bold">Employee</th>
              <th class="py-3 px-4 font-bold">ID</th>
              <th class="py-3 px-4 font-bold">Department</th>
              <th class="py-3 px-4 font-bold">Date</th>
              <th class="py-3 px-4 font-bold">Mode</th>
              <th class="py-3 px-4 font-bold">Work Done</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-zinc-800">
            <tr v-if="attendanceRecords.length === 0">
              <td colspan="6" class="py-8 text-center text-zinc-500 italic">No attendance records found.</td>
            </tr>
            <tr 
              v-for="rec in attendanceRecords" 
              :key="rec.id"
              class="hover:bg-zinc-850 transition-colors">
              <td class="py-2.5 px-4 font-medium text-white">{{ rec.name }}</td>
              <td class="py-2.5 px-4 font-mono text-zinc-400">{{ rec.rollNumber }}</td>
              <td class="py-2.5 px-4">
                <span class="bg-zinc-950 text-zinc-400 px-2 py-0.5 rounded border border-zinc-800 font-mono text-[10px]">
                  {{ rec.team }}
                </span>
              </td>
              <td class="py-2.5 px-4 font-mono text-zinc-400">{{ rec.date }}</td>
              <td class="py-2.5 px-4">
                <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border border-zinc-800 bg-zinc-950 text-zinc-300">
                  {{ rec.attendanceMode || 'In-Office' }}
                </span>
              </td>
              <td class="py-2.5 px-4 text-zinc-300 max-w-sm truncate">{{ rec.workDone || rec.todayLog }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { getApiBase } from '@/config'
import { ref, computed, onMounted } from 'vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'


const allLogs = ref([])
const selectedDate = ref(new Date().toISOString().split('T')[0])
const filterTeam = ref('')
const copied = ref(false)

const attendanceRecords = computed(() => {
  return allLogs.value.filter(l => {
    const matchDate = !selectedDate.value || l.date === selectedDate.value
    const matchTeam = !filterTeam.value || (l.team || '').toLowerCase() === filterTeam.value.toLowerCase()
    return matchDate && matchTeam
  })
})

const officeCount = computed(() => attendanceRecords.value.filter(r => !r.attendanceMode || r.attendanceMode === 'office').length)
const remoteCount = computed(() => attendanceRecords.value.filter(r => r.attendanceMode === 'remote').length)
const fieldCount = computed(() => attendanceRecords.value.filter(r => r.attendanceMode === 'field').length)

const copyAttendanceList = () => {
  const text = attendanceRecords.value.map((r, i) => `${i + 1}. ${r.name} (${r.rollNumber}) - ${r.team} - ${r.attendanceMode || 'In-Office'}`).join('\n')
  navigator.clipboard.writeText(text)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

const generateAttendancePDF = () => {
  const doc = new jsPDF()
  doc.setFontSize(16)
  doc.text("Fixly Office - Daily Attendance Sheet", 14, 15)
  doc.setFontSize(10)
  doc.text(`Date: ${selectedDate.value || 'All Dates'} | Total Present: ${attendanceRecords.value.length}`, 14, 22)

  const rows = attendanceRecords.value.map((r, i) => [
    i + 1,
    r.name,
    r.rollNumber,
    r.team,
    r.attendanceMode || 'In-Office',
    r.date
  ])

  autoTable(doc, {
    startY: 28,
    head: [['#', 'Name', 'Employee ID', 'Department', 'Mode', 'Date']],
    body: rows,
    theme: 'grid',
    headStyles: { fillColor: [40, 40, 45] }
  })

  doc.save(`Fixly_Office_Attendance_${selectedDate.value || 'Report'}.pdf`)
}

const exportCSV = () => {
  if (attendanceRecords.value.length === 0) return
  const headers = ['#', 'Name', 'Employee ID', 'Department', 'Mode', 'Date', 'Work Accomplished']
  const rows = attendanceRecords.value.map((r, i) => [
    i + 1,
    r.name,
    r.rollNumber || '',
    r.team || '',
    r.attendanceMode || 'In-Office',
    r.date,
    r.workDone || r.todayLog || ''
  ])
  const csvContent = "\uFEFF" + [headers, ...rows]
    .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(","))
    .join("\n")
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `Fixly_Office_Attendance_${selectedDate.value || 'All'}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const fetchLogs = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/logs/all`)
    if (res.ok) {
      allLogs.value = await res.json()
    }
  } catch (err) {
    console.error('Error fetching logs:', err)
  }
}

onMounted(() => {
  fetchLogs()
})
</script>
