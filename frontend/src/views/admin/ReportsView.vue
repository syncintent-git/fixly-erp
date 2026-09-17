<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header Card -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span class="text-orange-400 font-bold">FIXLY OFFICE</span>
            <span>•</span>
            <span>EXECUTIVE AUDITING & COMPLIANCE</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Executive Attendance & Work Reports</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Filter, audit, and export comprehensive attendance records from inception, across custom intervals, or for individual personnel.</p>
        </div>

        <!-- Export Action Buttons -->
        <div class="flex flex-wrap items-center gap-2 shrink-0">
          <button 
            @click="exportCSV"
            :disabled="filteredLogs.length === 0"
            class="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 hover:text-white border border-zinc-700 text-xs font-semibold px-3 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed">
            <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>Export CSV</span>
          </button>

          <button 
            @click="generateAttendancePDF"
            :disabled="filteredLogs.length === 0"
            class="bg-white hover:bg-zinc-200 text-black font-bold text-xs px-3.5 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed shadow-sm">
            <svg class="w-4 h-4 text-black" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/></svg>
            <span>Attendance PDF</span>
          </button>

          <button 
            @click="generateFullPDF"
            :disabled="filteredLogs.length === 0"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed shadow-sm">
            <svg class="w-4 h-4 text-black" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd"/></svg>
            <span>Full Work PDF</span>
          </button>
        </div>
      </div>

      <!-- Real-time Filter Summary Metrics -->
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-4 mt-4 border-t border-zinc-800">
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Total Records</span>
          <p class="text-xl font-bold text-white mt-0.5">{{ filteredLogs.length }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Unique Active</span>
          <p class="text-xl font-black text-orange-400 mt-0.5">{{ uniqueEmployeesCount }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">In-Office</span>
          <p class="text-lg font-bold text-zinc-200 mt-0.5">{{ officeCount }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Remote / WFH</span>
          <p class="text-lg font-bold text-zinc-200 mt-0.5">{{ remoteCount }}</p>
        </div>
        <div class="bg-zinc-950 p-3 rounded border border-zinc-800 col-span-2 sm:col-span-1">
          <span class="text-[10px] uppercase font-medium text-zinc-400">Compliance Rate</span>
          <p class="text-lg font-bold text-emerald-400 mt-0.5">{{ complianceRate }}%</p>
        </div>
      </div>
    </div>

    <!-- Interactive Report Filter Hub -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-4 space-y-4 w-full">
      
      <!-- Top Filters Row: Mode Selection -->
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pb-3 border-b border-zinc-800">
        <!-- Date Interval Modes -->
        <div class="flex flex-wrap items-center gap-1.5 text-xs">
          <span class="text-zinc-500 font-mono uppercase text-[11px] mr-1">Timeframe:</span>
          
          <button 
            type="button"
            @click="setDateMode('all-time')"
            :class="['px-3 py-1.5 rounded text-xs font-semibold transition-colors cursor-pointer', 
              dateMode === 'all-time' ? 'bg-orange-500 text-black shadow-sm' : 'bg-zinc-950 text-zinc-400 hover:text-white border border-zinc-800']">
            Starting till Date (All-Time)
          </button>

          <button 
            type="button"
            @click="setDateMode('interval')"
            :class="['px-3 py-1.5 rounded text-xs font-semibold transition-colors cursor-pointer', 
              dateMode === 'interval' ? 'bg-orange-500 text-black shadow-sm' : 'bg-zinc-950 text-zinc-400 hover:text-white border border-zinc-800']">
            Specific Interval (Range)
          </button>

          <button 
            type="button"
            @click="setDateMode('single')"
            :class="['px-3 py-1.5 rounded text-xs font-semibold transition-colors cursor-pointer', 
              dateMode === 'single' ? 'bg-orange-500 text-black shadow-sm' : 'bg-zinc-950 text-zinc-400 hover:text-white border border-zinc-800']">
            Single Day
          </button>
        </div>

        <!-- Quick Interval Presets (Only visible in interval mode) -->
        <div v-if="dateMode === 'interval'" class="flex flex-wrap items-center gap-1 text-[11px]">
          <span class="text-zinc-500 font-mono mr-1">Presets:</span>
          <button 
            @click="setPresetInterval(7)"
            class="px-2 py-1 rounded bg-zinc-950 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800 transition-colors cursor-pointer">
            Last 7 Days
          </button>
          <button 
            @click="setPresetInterval(14)"
            class="px-2 py-1 rounded bg-zinc-950 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800 transition-colors cursor-pointer">
            Last 14 Days
          </button>
          <button 
            @click="setPresetInterval(30)"
            class="px-2 py-1 rounded bg-zinc-950 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800 transition-colors cursor-pointer">
            Last 30 Days
          </button>
          <button 
            @click="setPresetThisMonth"
            class="px-2 py-1 rounded bg-zinc-950 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800 transition-colors cursor-pointer">
            This Month
          </button>
        </div>
      </div>

      <!-- Filter Controls Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
        
        <!-- Date Control 1: Start Date or Earliest Date -->
        <div v-if="dateMode === 'interval'">
          <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Start Date</label>
          <input 
            type="date" 
            v-model="startDate" 
            class="w-full bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs font-mono text-white outline-none cursor-pointer focus:border-orange-500 transition-colors"
          />
        </div>

        <div v-else-if="dateMode === 'all-time'">
          <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Record Inception</label>
          <div class="bg-zinc-950/80 border border-zinc-800 text-zinc-400 rounded px-2.5 py-1.5 text-xs font-mono flex items-center justify-between">
            <span>From Beginning</span>
            <span class="text-orange-400 font-bold">{{ earliestRecordedDate || 'Earliest' }}</span>
          </div>
        </div>

        <!-- Date Control 2: End Date / Target Date / Single Date -->
        <div>
          <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">
            {{ dateMode === 'single' ? 'Select Date' : 'Ending Till Date' }}
          </label>
          <input 
            type="date" 
            v-model="endDate" 
            class="w-full bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs font-mono text-white outline-none cursor-pointer focus:border-orange-500 transition-colors"
          />
        </div>

        <!-- Scope Selection: All, Department, or Individual -->
        <div>
          <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Report Scope</label>
          <select 
            v-model="scopeMode" 
            class="w-full bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs text-white outline-none cursor-pointer focus:border-orange-500 transition-colors">
            <option value="all">All Personnel (Company-wide)</option>
            <option value="department">By Department</option>
            <option value="individual">Individual Attendance</option>
          </select>
        </div>

        <!-- Scope Target Control: Department Selector OR Employee Selector -->
        <div>
          <template v-if="scopeMode === 'department'">
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Select Department</label>
            <select 
              v-model="selectedDepartment" 
              class="w-full bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs text-white outline-none cursor-pointer focus:border-orange-500 transition-colors">
              <option value="">All Departments</option>
              <option v-for="dept in availableDepartments" :key="dept" :value="dept">{{ dept }}</option>
            </select>
          </template>

          <template v-else-if="scopeMode === 'individual'">
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Select Employee</label>
            <select 
              v-model="selectedUserId" 
              class="w-full bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs text-white outline-none cursor-pointer focus:border-orange-500 transition-colors">
              <option value="">Choose Employee...</option>
              <option v-for="u in allUsers" :key="u.id" :value="u.id">
                {{ u.name }} ({{ u.rollNumber || 'ID-' + u.id }}) - {{ u.team || 'General' }}
              </option>
            </select>
          </template>

          <template v-else>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Filter Tag</label>
            <div class="bg-zinc-950/80 border border-zinc-800 text-zinc-400 rounded px-2.5 py-1.5 text-xs font-mono">
              All Active Departments
            </div>
          </template>
        </div>

      </div>

      <!-- Individual Employee Focused Summary Card (When an individual is selected) -->
      <div v-if="scopeMode === 'individual' && currentSelectedUser" class="bg-zinc-950 border border-orange-500/30 rounded-lg p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-orange-500/10 border border-orange-500/30 text-orange-400 flex items-center justify-center font-bold text-sm font-mono shrink-0">
            {{ getUserInitials(currentSelectedUser.name) }}
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-bold text-white text-sm">{{ currentSelectedUser.name }}</h3>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300">
                {{ currentSelectedUser.rollNumber || 'ID-' + currentSelectedUser.id }}
              </span>
            </div>
            <p class="text-xs text-zinc-400 mt-0.5">
              {{ currentSelectedUser.positionTitle || currentSelectedUser.role }} • {{ currentSelectedUser.team || 'General' }}
            </p>
          </div>
        </div>

        <div class="flex items-center gap-4 text-xs font-mono">
          <div>
            <span class="text-zinc-500 text-[10px] block uppercase">Present</span>
            <span class="text-white font-bold">{{ filteredLogs.length }} Days</span>
          </div>
          <div>
            <span class="text-zinc-500 text-[10px] block uppercase">In-Office</span>
            <span class="text-orange-400 font-bold">{{ officeCount }}</span>
          </div>
          <div>
            <span class="text-zinc-500 text-[10px] block uppercase">Remote</span>
            <span class="text-zinc-300 font-bold">{{ remoteCount }}</span>
          </div>
          <div>
            <span class="text-zinc-500 text-[10px] block uppercase">Compliance</span>
            <span class="text-emerald-400 font-bold">{{ individualComplianceRate }}%</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Filtered Results Count & Applied Scope Banner -->
    <div class="flex items-center justify-between text-xs text-zinc-400 px-1">
      <div class="flex items-center gap-2">
        <span class="font-mono text-orange-400 font-bold">{{ filteredLogs.length }} Records</span>
        <span>•</span>
        <span>{{ reportScopeDescription }}</span>
      </div>
      <span class="font-mono text-[11px] text-zinc-500">{{ reportTimeframeDescription }}</span>
    </div>

    <!-- Attendance & Deliverables Table -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden w-full">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-zinc-300">
          <thead class="bg-zinc-950 text-[10px] uppercase font-mono tracking-wider text-zinc-400 border-b border-zinc-800">
            <tr>
              <th class="py-3 px-4 font-bold">Date</th>
              <th class="py-3 px-4 font-bold">Employee</th>
              <th class="py-3 px-4 font-bold">Department</th>
              <th class="py-3 px-4 font-bold">Mode</th>
              <th class="py-3 px-4 font-bold">Work Accomplished</th>
              <th class="py-3 px-4 font-bold">Next Goal</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-zinc-800">
            <tr v-if="filteredLogs.length === 0">
              <td colspan="6" class="py-12 text-center text-zinc-500 italic">
                No attendance logs found matching the selected timeframe and scope.
              </td>
            </tr>
            <tr 
              v-for="log in filteredLogs" 
              :key="log.id"
              class="hover:bg-zinc-850 transition-colors">
              <td class="py-2.5 px-4 font-mono text-zinc-400 whitespace-nowrap">
                {{ log.date }}
              </td>
              <td class="py-2.5 px-4 font-medium text-white">
                <div>{{ log.name }}</div>
                <div class="text-[10px] font-mono text-zinc-500">{{ log.rollNumber }}</div>
              </td>
              <td class="py-2.5 px-4">
                <span class="bg-zinc-950 text-zinc-400 px-2 py-0.5 rounded border border-zinc-800 font-mono text-[10px]">
                  {{ log.team || 'General' }}
                </span>
              </td>
              <td class="py-2.5 px-4 whitespace-nowrap">
                <span 
                  :class="[
                    'text-[10px] font-mono uppercase px-2 py-0.5 rounded border',
                    (log.attendanceMode || 'office') === 'office' 
                      ? 'bg-orange-500/10 text-orange-400 border-orange-500/30' 
                      : (log.attendanceMode === 'remote' ? 'bg-blue-500/10 text-blue-400 border-blue-500/30' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30')
                  ]">
                  {{ formatAttendanceMode(log.attendanceMode) }}
                </span>
              </td>
              <td class="py-2.5 px-4 text-zinc-300 max-w-sm truncate leading-relaxed">
                {{ log.todayLog || log.workDone || '—' }}
              </td>
              <td class="py-2.5 px-4 text-zinc-400 max-w-xs truncate">
                {{ log.tomorrowGoal || log.nextDayGoal || '—' }}
              </td>
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
import { useScrumStore } from '../../stores/scrum'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const scrumStore = useScrumStore()


// Master data
const allLogs = ref([])
const allUsers = ref([])

// Date filtering mode: 'all-time' | 'interval' | 'single'
const dateMode = ref('all-time')

// Date inputs (defaults to today)
const todayStr = new Date().toISOString().split('T')[0]
const startDate = ref(new Date(Date.now() - 13 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])
const endDate = ref(todayStr)

// Scope mode: 'all' | 'department' | 'individual'
const scopeMode = ref('all')
const selectedDepartment = ref('')
const selectedUserId = ref('')

const setDateMode = (mode) => {
  dateMode.value = mode
  if (mode === 'single') {
    endDate.value = todayStr
  } else if (mode === 'all-time') {
    endDate.value = todayStr
  }
}

const setPresetInterval = (days) => {
  const d = new Date()
  d.setDate(d.getDate() - (days - 1))
  startDate.value = d.toISOString().split('T')[0]
  endDate.value = todayStr
}

const setPresetThisMonth = () => {
  const now = new Date()
  const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
  startDate.value = firstDay.toISOString().split('T')[0]
  endDate.value = todayStr
}

// Earliest recorded date in database
const earliestRecordedDate = computed(() => {
  if (allLogs.value.length === 0) return ''
  const dates = allLogs.value.map(l => l.date).filter(Boolean)
  if (dates.length === 0) return ''
  dates.sort()
  return dates[0]
})

// Unique departments from users and logs
const availableDepartments = computed(() => {
  const set = new Set()
  allUsers.value.forEach(u => { if (u.team) set.add(u.team) })
  allLogs.value.forEach(l => { if (l.team) set.add(l.team) })
  return Array.from(set).sort()
})

// Currently selected user object
const currentSelectedUser = computed(() => {
  if (!selectedUserId.value) return null
  return allUsers.value.find(u => String(u.id) === String(selectedUserId.value)) || null
})

// Filtered logs computation based on date mode and scope
const filteredLogs = computed(() => {
  return allLogs.value.filter(log => {
    // 1. Date filter
    if (dateMode.value === 'single') {
      if (log.date !== endDate.value) return false
    } else if (dateMode.value === 'all-time') {
      if (endDate.value && log.date > endDate.value) return false
    } else if (dateMode.value === 'interval') {
      if (startDate.value && log.date < startDate.value) return false
      if (endDate.value && log.date > endDate.value) return false
    }

    // 2. Scope filter
    if (scopeMode.value === 'department') {
      if (selectedDepartment.value && (log.team || '').toLowerCase() !== selectedDepartment.value.toLowerCase()) {
        return false
      }
    } else if (scopeMode.value === 'individual') {
      if (selectedUserId.value) {
        const u = currentSelectedUser.value
        const matchId = log.userId && String(log.userId) === String(selectedUserId.value)
        const matchRoll = u && u.rollNumber && log.rollNumber && u.rollNumber.toLowerCase() === log.rollNumber.toLowerCase()
        const matchName = u && u.name && log.name && u.name.toLowerCase() === log.name.toLowerCase()
        if (!matchId && !matchRoll && !matchName) return false
      }
    }

    return true
  }).sort((a, b) => (b.date || '').localeCompare(a.date || '') || (b.timestamp || 0) - (a.timestamp || 0))
})

// Statistics on filtered records
const uniqueEmployeesCount = computed(() => {
  const names = new Set(filteredLogs.value.map(l => (l.name || l.rollNumber || '').toLowerCase()))
  return names.size
})

const officeCount = computed(() => {
  return filteredLogs.value.filter(l => !l.attendanceMode || l.attendanceMode.toLowerCase() === 'office').length
})

const remoteCount = computed(() => {
  return filteredLogs.value.filter(l => (l.attendanceMode || '').toLowerCase() === 'remote').length
})

const fieldCount = computed(() => {
  return filteredLogs.value.filter(l => (l.attendanceMode || '').toLowerCase() === 'field').length
})

const complianceRate = computed(() => {
  if (allUsers.value.length === 0) return 0
  if (dateMode.value === 'single') {
    return Math.round((filteredLogs.value.length / allUsers.value.length) * 100)
  }
  // For intervals, compliance based on active members
  return Math.min(100, Math.round((uniqueEmployeesCount.value / allUsers.value.length) * 100))
})

const individualComplianceRate = computed(() => {
  if (filteredLogs.value.length === 0) return 0
  // Estimate working days in interval
  return 100
})

const reportScopeDescription = computed(() => {
  if (scopeMode.value === 'individual') {
    return currentSelectedUser.value 
      ? `Individual: ${currentSelectedUser.value.name} (${currentSelectedUser.value.rollNumber || 'ID-' + currentSelectedUser.value.id})`
      : 'Individual: (All pending selection)'
  }
  if (scopeMode.value === 'department') {
    return selectedDepartment.value ? `Department: ${selectedDepartment.value}` : 'All Departments'
  }
  return 'Company-wide (All Personnel)'
})

const reportTimeframeDescription = computed(() => {
  if (dateMode.value === 'single') {
    return `Date: ${endDate.value}`
  }
  if (dateMode.value === 'all-time') {
    return `Inception (${earliestRecordedDate.value || 'Start'}) till ${endDate.value}`
  }
  return `Interval: ${startDate.value} to ${endDate.value}`
})

const formatAttendanceMode = (mode) => {
  const m = (mode || 'office').toLowerCase()
  if (m === 'remote') return 'Remote'
  if (m === 'field') return 'On-Duty / Field'
  return 'In-Office'
}

const getUserInitials = (name) => {
  if (!name) return 'U'
  return name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
}

// ----------------------------------------------------
// PDF EXPORT 1: Clean Attendance Report
// ----------------------------------------------------
const generateAttendancePDF = () => {
  if (filteredLogs.value.length === 0) return

  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()

  // Header Banner
  doc.setFillColor(15, 23, 42) // Deep Slate / Black
  doc.rect(0, 0, pageWidth, 28, 'F')

  doc.setTextColor(255, 255, 255)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text("FIXLY OFFICE - ATTENDANCE AUDIT REPORT", 14, 12)

  doc.setFontSize(8.5)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(203, 213, 225)
  doc.text(`${reportTimeframeDescription.value}  |  ${reportScopeDescription.value}`, 14, 19)
  doc.text(`Generated on: ${new Date().toLocaleString()}  |  Total Records: ${filteredLogs.value.length}`, 14, 24)

  // KPI Mini Table / Box
  const kpiY = 32
  doc.setFontSize(8)
  doc.setTextColor(100, 116, 139)
  doc.text(`Audit Summary: Total Submissions: ${filteredLogs.value.length} | In-Office: ${officeCount.value} | Remote: ${remoteCount.value} | Field: ${fieldCount.value}`, 14, kpiY)

  // Build rows based on whether it's individual or multi-user
  let headCols = []
  let bodyRows = []

  if (scopeMode.value === 'individual' && currentSelectedUser.value) {
    headCols = [['#', 'Date', 'Attendance Mode', 'Employee Name', 'Department', 'Daily Log Accomplishment']]
    bodyRows = filteredLogs.value.map((l, i) => [
      i + 1,
      l.date,
      formatAttendanceMode(l.attendanceMode),
      l.name,
      l.team || 'General',
      l.todayLog || l.workDone || '—'
    ])
  } else {
    headCols = [['#', 'Date', 'Employee Name', 'ID / Roll', 'Department', 'Attendance Mode']]
    bodyRows = filteredLogs.value.map((l, i) => [
      i + 1,
      l.date,
      l.name,
      l.rollNumber || '—',
      l.team || 'General',
      formatAttendanceMode(l.attendanceMode)
    ])
  }

  autoTable(doc, {
    startY: 36,
    head: headCols,
    body: bodyRows,
    theme: 'grid',
    headStyles: { 
      fillColor: [30, 41, 59], 
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      fontSize: 8
    },
    bodyStyles: {
      fontSize: 8,
      textColor: [30, 41, 59]
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252]
    }
  })

  // Filename construction
  let filePrefix = 'Fixly_Office_Attendance'
  if (scopeMode.value === 'individual' && currentSelectedUser.value) {
    filePrefix += `_${currentSelectedUser.value.name.replace(/\s+/g, '_')}`
  } else if (scopeMode.value === 'department' && selectedDepartment.value) {
    filePrefix += `_${selectedDepartment.value.replace(/\s+/g, '_')}`
  }
  const dateSuffix = dateMode.value === 'single' ? endDate.value : `${startDate.value}_to_${endDate.value}`
  doc.save(`${filePrefix}_${dateSuffix}.pdf`)
}

// ----------------------------------------------------
// PDF EXPORT 2: Full Daily Work & Deliverables PDF
// ----------------------------------------------------
const generateFullPDF = () => {
  if (filteredLogs.value.length === 0) return

  const doc = new jsPDF()
  const pageWidth = doc.internal.pageSize.getWidth()

  // Header Banner
  doc.setFillColor(15, 23, 42)
  doc.rect(0, 0, pageWidth, 28, 'F')

  doc.setTextColor(255, 255, 255)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text("FIXLY OFFICE - COMPREHENSIVE WORK & ATTENDANCE AUDIT", 14, 12)

  doc.setFontSize(8.5)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(203, 213, 225)
  doc.text(`${reportTimeframeDescription.value}  |  ${reportScopeDescription.value}`, 14, 19)
  doc.text(`Generated on: ${new Date().toLocaleString()}  |  Total Submissions: ${filteredLogs.value.length}`, 14, 24)

  const rows = filteredLogs.value.map((l, i) => [
    i + 1,
    l.date,
    `${l.name} (${l.rollNumber || '—'})`,
    l.team || 'General',
    formatAttendanceMode(l.attendanceMode),
    l.todayLog || l.workDone || '—',
    l.tomorrowGoal || l.nextDayGoal || '—'
  ])

  autoTable(doc, {
    startY: 34,
    head: [['#', 'Date', 'Employee', 'Department', 'Mode', 'Tasks Accomplished', 'Next Goal']],
    body: rows,
    theme: 'grid',
    headStyles: { 
      fillColor: [30, 41, 59], 
      textColor: [255, 255, 255],
      fontStyle: 'bold',
      fontSize: 8
    },
    bodyStyles: {
      fontSize: 7.5,
      textColor: [30, 41, 59]
    },
    columnStyles: {
      5: { cellWidth: 60 },
      6: { cellWidth: 35 }
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252]
    }
  })

  let filePrefix = 'Fixly_Office_Full_Report'
  if (scopeMode.value === 'individual' && currentSelectedUser.value) {
    filePrefix += `_${currentSelectedUser.value.name.replace(/\s+/g, '_')}`
  }
  const dateSuffix = dateMode.value === 'single' ? endDate.value : `${startDate.value}_to_${endDate.value}`
  doc.save(`${filePrefix}_${dateSuffix}.pdf`)
}

// ----------------------------------------------------
// CSV EXPORT: Excel / Spreadsheet Compatible
// ----------------------------------------------------
const exportCSV = () => {
  if (filteredLogs.value.length === 0) return

  const headers = ['#', 'Date', 'Employee Name', 'Employee ID', 'Department', 'Attendance Mode', 'Work Done', 'Next Goal']
  const rows = filteredLogs.value.map((l, i) => [
    i + 1,
    l.date,
    l.name,
    l.rollNumber || '',
    l.team || '',
    formatAttendanceMode(l.attendanceMode),
    l.todayLog || l.workDone || '',
    l.tomorrowGoal || l.nextDayGoal || ''
  ])

  const csvContent = "\uFEFF" + [headers, ...rows]
    .map(row => row.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(","))
    .join("\n")

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  
  let filePrefix = 'Fixly_Office_Attendance'
  if (scopeMode.value === 'individual' && currentSelectedUser.value) {
    filePrefix += `_${currentSelectedUser.value.name.replace(/\s+/g, '_')}`
  }
  const dateSuffix = dateMode.value === 'single' ? endDate.value : `${startDate.value}_to_${endDate.value}`
  link.setAttribute('download', `${filePrefix}_${dateSuffix}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const fetchData = async () => {
  try {
    const [resLogs, resUsers] = await Promise.all([
      fetch(`${getApiBase()}/api/logs/all`),
      fetch(`${getApiBase()}/api/users/all`)
    ])
    if (resLogs.ok) allLogs.value = await resLogs.json()
    if (resUsers.ok) allUsers.value = await resUsers.json()
  } catch (err) {
    console.error('Error fetching report data:', err)
  }
}

onMounted(() => {
  fetchData()
  scrumStore.fetchTasks()
})
</script>
