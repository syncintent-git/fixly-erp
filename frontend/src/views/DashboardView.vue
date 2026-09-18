<template>
  <div class="space-y-6 w-full">

    <!-- Top Role Greeting & Context Banner -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 sm:p-6 w-full relative overflow-hidden shadow-lg">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
        
        <div class="space-y-1.5">
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-[10px] font-mono uppercase tracking-wider text-zinc-400">Fixly Command Center</span>
            <span class="text-zinc-600">•</span>
            <span class="text-[10px] font-mono uppercase tracking-wider text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded border border-orange-500/30 font-bold">
              {{ currentRoleBadge }}
            </span>
            <span class="text-zinc-600">•</span>
            <span class="text-[10px] font-mono text-zinc-400">{{ todayFormatted }}</span>
          </div>

          <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {{ greetingText }}, <span class="text-orange-400">{{ authStore.user?.name || 'User' }}</span>
          </h1>

          <p class="text-xs sm:text-sm text-zinc-400 max-w-2xl leading-relaxed">
            {{ roleDescription }}
          </p>
        </div>

        <!-- Quick Top Action Button according to role -->
        <div class="flex items-center gap-2.5 shrink-0">
          <!-- Intern: Quick Daily Log -->
          <router-link 
            v-if="isIntern"
            to="/workforce/daily-log" 
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2.5 rounded-lg transition-colors flex items-center gap-2 shadow-sm cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            <span>{{ isLoggedToday ? 'View Today\'s Log' : 'Submit Daily Log' }}</span>
          </router-link>

          <!-- Scrum Head: Review Queue -->
          <router-link 
            v-else-if="isScrumHead"
            to="/scrum/reviews" 
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2.5 rounded-lg transition-colors flex items-center gap-2 shadow-sm cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>Review Queue ({{ pendingApprovalsCount }})</span>
          </router-link>

          <!-- Admin: Access Requests -->
          <router-link 
            v-else-if="isAdmin"
            to="/admin/access-requests" 
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2.5 rounded-lg transition-colors flex items-center gap-2 shadow-sm cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>
            <span>Requests ({{ pendingUsersCount }})</span>
          </router-link>

          <!-- Executive: Executive Reports -->
          <router-link 
            v-else
            to="/admin/reports" 
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2.5 rounded-lg transition-colors flex items-center gap-2 shadow-sm cursor-pointer">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span>Executive Reports</span>
          </router-link>
        </div>

      </div>

      <!-- Background Glow Accent -->
      <div class="absolute -right-12 -top-12 w-64 h-64 bg-orange-500/5 rounded-full blur-3xl pointer-events-none"></div>
    </div>

    <!-- 4 High-Signal Key Metric Pulse Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      
      <!-- Card 1 -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 sm:p-5 hover:border-zinc-700 transition-colors">
        <div class="flex items-center justify-between text-zinc-400">
          <span class="text-[10px] font-mono uppercase tracking-wider font-semibold">{{ kpi1.label }}</span>
          <span class="p-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-orange-400" v-html="kpi1.icon"></span>
        </div>
        <div class="mt-2.5 flex items-baseline gap-2">
          <span class="text-2xl sm:text-3xl font-black text-white font-mono">{{ kpi1.value }}</span>
          <span v-if="kpi1.unit" class="text-xs text-zinc-400 font-medium">{{ kpi1.unit }}</span>
        </div>
        <p class="text-[11px] text-zinc-500 mt-1">{{ kpi1.subtext }}</p>
      </div>

      <!-- Card 2 -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 sm:p-5 hover:border-zinc-700 transition-colors">
        <div class="flex items-center justify-between text-zinc-400">
          <span class="text-[10px] font-mono uppercase tracking-wider font-semibold">{{ kpi2.label }}</span>
          <span class="p-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-orange-400" v-html="kpi2.icon"></span>
        </div>
        <div class="mt-2.5 flex items-baseline gap-2">
          <span :class="['text-2xl sm:text-3xl font-black font-mono', kpi2.highlight ? 'text-orange-400' : 'text-white']">
            {{ kpi2.value }}
          </span>
          <span v-if="kpi2.unit" class="text-xs text-zinc-400 font-medium">{{ kpi2.unit }}</span>
        </div>
        <p class="text-[11px] text-zinc-500 mt-1">{{ kpi2.subtext }}</p>
      </div>

      <!-- Card 3 -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 sm:p-5 hover:border-zinc-700 transition-colors">
        <div class="flex items-center justify-between text-zinc-400">
          <span class="text-[10px] font-mono uppercase tracking-wider font-semibold">{{ kpi3.label }}</span>
          <span class="p-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-orange-400" v-html="kpi3.icon"></span>
        </div>
        <div class="mt-2.5 flex items-baseline gap-2">
          <span class="text-2xl sm:text-3xl font-black text-white font-mono">{{ kpi3.value }}</span>
          <span v-if="kpi3.unit" class="text-xs text-zinc-400 font-medium">{{ kpi3.unit }}</span>
        </div>
        <p class="text-[11px] text-zinc-500 mt-1">{{ kpi3.subtext }}</p>
      </div>

      <!-- Card 4 -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-4 sm:p-5 hover:border-zinc-700 transition-colors">
        <div class="flex items-center justify-between text-zinc-400">
          <span class="text-[10px] font-mono uppercase tracking-wider font-semibold">{{ kpi4.label }}</span>
          <span class="p-1.5 rounded-lg bg-zinc-950 border border-zinc-800 text-orange-400" v-html="kpi4.icon"></span>
        </div>
        <div class="mt-2.5 flex items-baseline gap-2">
          <span class="text-2xl sm:text-3xl font-black text-white font-mono">{{ kpi4.value }}</span>
          <span v-if="kpi4.unit" class="text-xs text-zinc-400 font-medium">{{ kpi4.unit }}</span>
        </div>
        <p class="text-[11px] text-zinc-500 mt-1">{{ kpi4.subtext }}</p>
      </div>

    </div>

    <!-- Quick Shortcuts Bar (Common to all roles, curated for speed) -->
    <div class="bg-zinc-900/80 border border-zinc-800 rounded-xl p-3 sm:p-4 flex flex-wrap items-center justify-between gap-2.5">
      <div class="flex items-center gap-2 text-xs font-semibold text-zinc-300">
        <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        <span>Frequent Hub Shortcuts:</span>
      </div>

      <div class="flex flex-wrap items-center gap-2 text-xs">
        <router-link to="/scrum/active-sprint" class="px-3 py-1.5 rounded-lg bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition-colors">
          Kanban Board
        </router-link>
        <router-link to="/workforce/daily-log" class="px-3 py-1.5 rounded-lg bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition-colors">
          Daily Log & Attendance
        </router-link>
        <router-link to="/workforce/feed" class="px-3 py-1.5 rounded-lg bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition-colors">
          Department Feed
        </router-link>
        <router-link to="/operations/mom" class="px-3 py-1.5 rounded-lg bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition-colors">
          Meeting Minutes
        </router-link>
        <router-link v-if="authStore.canAccessAdmin" to="/admin/reports" class="px-3 py-1.5 rounded-lg bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition-colors">
          Executive Reports
        </router-link>
      </div>
    </div>

    <!-- MAIN ROLE-SPECIFIC CONTENT PANELS -->

    <!-- ========================================================================= -->
    <!-- 1. INTERN / DEVELOPER WORKSPACE -->
    <!-- ========================================================================= -->
    <div v-if="isIntern" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column (2 cols): My Sprint Deliverables -->
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">My Assigned Sprint Tasks</h2>
              <p class="text-xs text-zinc-400 mt-0.5">Tasks assigned to you in {{ scrumStore.activeSprint?.name || 'Active Sprint' }}</p>
            </div>
            <router-link to="/scrum/active-sprint" class="text-xs text-orange-400 hover:text-orange-300 font-semibold inline-flex items-center gap-1">
              <span>Full Board</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </router-link>
          </div>

          <!-- Empty State -->
          <div v-if="myTasks.length === 0" class="p-8 text-center bg-zinc-950/60 rounded-lg border border-zinc-800/80 space-y-2">
            <p class="text-xs text-zinc-300 font-medium">No tasks assigned to your account in this cycle</p>
            <p class="text-[11px] text-zinc-500">Pick an open story task from the Backlog or request your Scrum Head.</p>
            <router-link to="/scrum/stories" class="inline-block mt-2 px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs rounded-lg transition-colors border border-zinc-700">
              Browse Stories Backlog
            </router-link>
          </div>

          <!-- Task Cards List -->
          <div v-else class="space-y-2.5">
            <div 
              v-for="task in myTasks" 
              :key="task.id"
              class="p-3.5 rounded-lg bg-zinc-950 border border-zinc-800 hover:border-zinc-700 transition-colors flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              
              <div class="space-y-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="font-mono text-[10px] font-bold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded-full border border-orange-500/30">
                    {{ task.taskId }}
                  </span>
                  <span class="text-xs font-semibold text-white truncate">{{ task.title }}</span>
                </div>
                <p v-if="task.description" class="text-[11px] text-zinc-400 truncate max-w-md">{{ task.description }}</p>
              </div>

              <!-- Status Action Pill -->
              <div class="flex items-center gap-2 shrink-0 self-end sm:self-center">
                <span 
                  :class="[
                    'text-[10px] font-mono uppercase px-2 py-0.5 rounded font-bold border',
                    taskStatusClass(task.status)
                  ]">
                  {{ formatTaskStatus(task.status) }}
                </span>

                <!-- 1-Click Quick Action -->
                <button 
                  v-if="task.status === 'TODO'"
                  @click="quickUpdateTaskStatus(task, 'IN_PROGRESS')"
                  class="text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-200 px-2.5 py-1 rounded transition-colors cursor-pointer border border-zinc-700">
                  Start Work
                </button>

                <router-link 
                  v-else-if="task.status === 'IN_PROGRESS'"
                  to="/scrum/active-sprint"
                  class="text-xs bg-orange-500 hover:bg-orange-400 text-black font-bold px-2.5 py-1 rounded transition-colors cursor-pointer shadow-sm">
                  Submit Work
                </router-link>
              </div>

            </div>
          </div>

        </div>
      </div>

      <!-- Right Column (1 col): Daily Accountability Status -->
      <div class="space-y-4">
        
        <!-- Today's Log Card -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Today's Attendance</h2>
            <span 
              :class="[
                'text-[10px] font-mono px-2 py-0.5 rounded font-bold border',
                isLoggedToday 
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' 
                  : 'bg-orange-500/10 text-orange-400 border-orange-500/30'
              ]">
              {{ isLoggedToday ? 'Recorded ✓' : 'Action Required' }}
            </span>
          </div>

          <div v-if="isLoggedToday" class="space-y-2 text-xs">
            <p class="text-zinc-400">You submitted your daily deliverable and attendance for today.</p>
            <div class="p-3 bg-zinc-950 rounded border border-zinc-800 space-y-1">
              <span class="text-[10px] font-mono text-zinc-500 uppercase">Work Done Today:</span>
              <p class="text-zinc-200 line-clamp-2">{{ todayLogItem?.workDone || todayLogItem?.todayLog }}</p>
            </div>
            <router-link to="/workforce/daily-log" class="block text-center text-xs text-orange-400 hover:underline pt-1">
              Edit Today's Submission →
            </router-link>
          </div>

          <div v-else class="space-y-3 text-xs">
            <p class="text-zinc-400">Keep your attendance record unbroken by logging today's work summary.</p>
            <router-link 
              to="/workforce/daily-log" 
              class="w-full bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs py-2 rounded-lg text-center block transition-colors cursor-pointer shadow-sm">
              Log Today's Work & Attendance
            </router-link>
          </div>
        </div>

        <!-- Active Sprint Health Card -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">{{ scrumStore.activeSprint?.name || 'Active Sprint' }} Milestone</h2>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-zinc-400">Velocity Progress</span>
              <span class="font-mono font-bold text-orange-400">{{ sprintProgressPercentage }}%</span>
            </div>
            <div class="w-full h-2 bg-zinc-950 rounded-full overflow-hidden border border-zinc-800">
              <div class="bg-orange-500 h-full rounded-full transition-all duration-300" :style="{ width: `${sprintProgressPercentage}%` }"></div>
            </div>
            <div class="flex items-center justify-between text-[10px] text-zinc-500 font-mono pt-1">
              <span>Cycle: {{ scrumStore.activeSprint?.startDate ? new Date(scrumStore.activeSprint.startDate).toISOString().split('T')[0] : 'TBD' }}</span>
              <span>Ends: {{ scrumStore.activeSprint?.endDate ? new Date(scrumStore.activeSprint.endDate).toISOString().split('T')[0] : 'TBD' }}</span>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- 2. SCRUM HEAD WORKSPACE -->
    <!-- ========================================================================= -->
    <div v-else-if="isScrumHead" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column (2 cols): Tasks Awaiting Review (Review Queue Widget) -->
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <div class="flex items-center gap-2">
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Tasks Awaiting Quality Review</h2>
              <span v-if="pendingReviewTasks.length > 0" class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500 text-black font-bold min-w-[18px] text-center leading-none inline-flex items-center justify-center shadow-sm">
                {{ pendingReviewTasks.length }}
              </span>
            </div>
            <router-link to="/scrum/reviews" class="text-xs text-orange-400 hover:text-orange-300 font-semibold inline-flex items-center gap-1">
              <span>Full Queue</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </router-link>
          </div>

          <div v-if="pendingReviewTasks.length === 0" class="p-8 text-center bg-zinc-950/60 rounded-lg border border-zinc-800/80 space-y-1">
            <p class="text-xs text-zinc-300 font-medium">Review queue is empty</p>
            <p class="text-[11px] text-zinc-500">All intern work submissions have been reviewed and approved.</p>
          </div>

          <div v-else class="space-y-3">
            <div 
              v-for="task in pendingReviewTasks" 
              :key="task.id"
              class="p-4 rounded-lg bg-zinc-950 border border-zinc-800 hover:border-zinc-700 transition-colors flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              
              <div class="space-y-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="font-mono text-xs font-bold text-orange-400 bg-orange-500/10 px-2 py-0.5 rounded border border-orange-500/30">
                    {{ task.taskId }}
                  </span>
                  <span class="text-xs font-bold text-white">{{ task.title }}</span>
                </div>
                <p class="text-xs text-zinc-400">
                  Submitted by: <strong class="text-zinc-200">{{ task.assignedToName || 'Intern' }}</strong>
                  <span v-if="task.submissionNotes" class="text-zinc-500"> — "{{ task.submissionNotes }}"</span>
                </p>
              </div>

              <!-- Decision Buttons -->
              <div class="flex items-center gap-2 shrink-0 self-end sm:self-center">
                <button 
                  @click="quickApproveTask(task)"
                  class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-3 py-1.5 rounded transition-colors cursor-pointer shadow-sm">
                  Approve ✓
                </button>
                <router-link 
                  to="/scrum/reviews"
                  class="bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs px-2.5 py-1.5 rounded transition-colors border border-zinc-700">
                  Inspect
                </router-link>
              </div>

            </div>
          </div>

        </div>

        <!-- Team Workload Distribution Strip -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Team Task Load Overview</h2>
            <router-link to="/scrum/team" class="text-xs text-orange-400 hover:underline">Full Matrix →</router-link>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
            <div v-for="intern in internsList.slice(0, 3)" :key="intern.id" class="p-3 bg-zinc-950 rounded-lg border border-zinc-800">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white truncate">{{ intern.name }}</span>
                <span class="text-[10px] font-mono text-orange-400">{{ intern.team }}</span>
              </div>
              <p class="text-[11px] text-zinc-500 mt-1">Tasks: {{ getInternTaskCount(intern.id) }} assigned</p>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column (1 col): Sprint Velocity Governance -->
      <div class="space-y-4">
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
          <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono pb-2 border-b border-zinc-800">{{ scrumStore.activeSprint?.name || 'Active Sprint' }} Health</h2>
          
          <div class="space-y-3 text-xs">
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">Approved Deliverables</span>
              <span class="font-mono font-bold text-emerald-400">{{ approvedTasksCount }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">In Progress Work</span>
              <span class="font-mono font-bold text-orange-400">{{ inProgressTasksCount }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">Pending Review</span>
              <span class="font-mono font-bold text-amber-400">{{ pendingReviewTasks.length }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">To Do (Unstarted)</span>
              <span class="font-mono font-bold text-zinc-400">{{ todoTasksCount }}</span>
            </div>

            <div class="pt-2 border-t border-zinc-800">
              <div class="flex items-center justify-between text-xs mb-1.5">
                <span class="text-zinc-300 font-semibold">Total Completion</span>
                <span class="font-mono font-bold text-orange-400">{{ sprintProgressPercentage }}%</span>
              </div>
              <div class="w-full h-2 bg-zinc-950 rounded-full overflow-hidden border border-zinc-800">
                <div class="bg-orange-500 h-full rounded-full transition-all duration-300" :style="{ width: `${sprintProgressPercentage}%` }"></div>
              </div>
            </div>
          </div>

          <div class="pt-2">
            <router-link 
              to="/scrum/sprints" 
              class="w-full bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs py-2 rounded-lg text-center block transition-colors border border-zinc-700">
              Sprint History & Planner →
            </router-link>
          </div>
        </div>
      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- 3. SYSTEM ADMINISTRATOR WORKSPACE -->
    <!-- ========================================================================= -->
    <div v-else-if="isAdmin" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column (2 cols): Pending User Registrations -->
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <div class="flex items-center gap-2">
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Pending Identity & Access Requests</h2>
              <span v-if="scrumStore.pendingUsers.length > 0" class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-orange-500 text-black font-bold min-w-[18px] text-center leading-none inline-flex items-center justify-center shadow-sm">
                {{ scrumStore.pendingUsers.length }}
              </span>
            </div>
            <router-link to="/admin/access-requests" class="text-xs text-orange-400 hover:text-orange-300 font-semibold inline-flex items-center gap-1">
              <span>View All</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </router-link>
          </div>

          <div v-if="scrumStore.pendingUsers.length === 0" class="p-8 text-center bg-zinc-950/60 rounded-lg border border-zinc-800/80 space-y-1">
            <p class="text-xs text-zinc-300 font-medium">No pending user registrations</p>
            <p class="text-[11px] text-zinc-500">All applicant onboarding requests are verified.</p>
          </div>

          <div v-else class="space-y-3">
            <div 
              v-for="user in scrumStore.pendingUsers" 
              :key="user.id"
              class="p-4 rounded-lg bg-zinc-950 border border-zinc-800 hover:border-zinc-700 transition-colors flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              
              <div class="space-y-0.5">
                <div class="flex items-center gap-2">
                  <span class="text-xs font-bold text-white">{{ user.name }}</span>
                  <span class="text-[11px] font-mono text-zinc-500">({{ user.email }})</span>
                </div>
                <p class="text-xs text-zinc-400">
                  Requested Role: <strong class="text-orange-400 font-mono">{{ user.requestedRole }}</strong>
                </p>
              </div>

              <!-- Quick Approve -->
              <div class="flex items-center gap-2 shrink-0">
                <button 
                  @click="quickApproveUser(user)"
                  class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-3 py-1.5 rounded transition-colors cursor-pointer shadow-sm">
                  Approve Access
                </button>
                <router-link 
                  to="/admin/access-requests"
                  class="bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs px-2.5 py-1.5 rounded transition-colors border border-zinc-700">
                  Configure
                </router-link>
              </div>

            </div>
          </div>

        </div>

        <!-- Recent Audit Events Preview -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Live Audit Events Stream</h2>
            <router-link to="/admin/audit" class="text-xs text-orange-400 hover:underline">Full Trail →</router-link>
          </div>

          <div class="space-y-2 text-xs">
            <div 
              v-for="log in scrumStore.auditLogs.slice(0, 4)" 
              :key="log.id"
              class="p-2.5 rounded bg-zinc-950 border border-zinc-800/80 flex items-center justify-between gap-3">
              <div class="flex items-center gap-2 truncate">
                <span class="w-1.5 h-1.5 rounded-full bg-orange-400 shrink-0"></span>
                <span class="font-bold text-zinc-200">{{ log.action }}</span>
                <span class="text-zinc-500 truncate">{{ log.details }}</span>
              </div>
              <span class="text-[10px] font-mono text-zinc-500 shrink-0">{{ formatTime(log.timestamp) }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column (1 col): System Controls -->
      <div class="space-y-4">
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono pb-2 border-b border-zinc-800">Administration Hubs</h2>
          <div class="space-y-2">
            <router-link 
              to="/admin/users" 
              class="p-3 bg-zinc-950 hover:bg-zinc-850 rounded-lg border border-zinc-800 text-xs flex items-center justify-between transition-colors block">
              <span class="font-semibold text-zinc-200">Personnel & Teams</span>
              <span class="text-orange-400 font-mono">Manage →</span>
            </router-link>

            <router-link 
              to="/admin/reports" 
              class="p-3 bg-zinc-950 hover:bg-zinc-850 rounded-lg border border-zinc-800 text-xs flex items-center justify-between transition-colors block">
              <span class="font-semibold text-zinc-200">Executive Daily Reports</span>
              <span class="text-orange-400 font-mono">Export PDF →</span>
            </router-link>

            <router-link 
              to="/admin/audit" 
              class="p-3 bg-zinc-950 hover:bg-zinc-850 rounded-lg border border-zinc-800 text-xs flex items-center justify-between transition-colors block">
              <span class="font-semibold text-zinc-200">System Audit Trail</span>
              <span class="text-orange-400 font-mono">Inspect →</span>
            </router-link>
          </div>
        </div>
      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- 4. EXECUTIVE LEADERSHIP & REVIEWER WORKSPACE (CEO, CTO, COO, CFO, CMO, CDC, MENTOR) -->
    <!-- ========================================================================= -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column (2 cols): Cross-Department Deliverables & Reports -->
      <div class="lg:col-span-2 space-y-4">
        
        <!-- Attendance & Deliverables Pulse -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-4">
          <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
            <div>
              <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">Today's Workforce Deliverables Pulse</h2>
              <p class="text-xs text-zinc-400 mt-0.5">Summary of employee work logged today</p>
            </div>
            <router-link to="/admin/reports" class="text-xs text-orange-400 hover:text-orange-300 font-semibold inline-flex items-center gap-1">
              <span>Executive Report</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </router-link>
          </div>

          <!-- Department Cards Strip -->
          <!-- Team Pulse Cards -->
          <div v-if="allTeams.length > 0" class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div 
              v-for="(t, idx) in allTeams.slice(0, 4)" 
              :key="t.id || t.name"
              class="p-3 rounded-lg bg-zinc-950 border border-zinc-800 text-center">
              <span class="text-[10px] font-mono uppercase text-zinc-500 truncate block">{{ t.name }}</span>
              <p :class="['text-lg font-black mt-0.5 font-mono', idx === 0 ? 'text-orange-400' : 'text-white']">
                {{ countByTeam(t.name) }}
              </p>
            </div>
          </div>
          <div v-else class="p-4 bg-zinc-950 rounded border border-zinc-800 text-center text-xs text-zinc-500">
            No departments configured. Add teams in Admin &gt; Users &amp; Teams.
          </div>

          <!-- Feed Teaser -->
          <div class="space-y-2 pt-2 border-t border-zinc-800">
            <h3 class="text-xs font-bold text-zinc-300 uppercase tracking-wider font-mono">Latest Activity Highlights</h3>
            <div class="space-y-2 text-xs">
              <div 
                v-for="log in todayLogs.slice(0, 3)" 
                :key="log.id"
                class="p-3 bg-zinc-950 rounded border border-zinc-800 flex items-center justify-between">
                <div>
                  <span class="font-bold text-white">{{ log.name }}</span>
                  <span class="text-zinc-500 text-[11px] ml-1.5">({{ log.team }})</span>
                  <p class="text-zinc-400 text-[11px] mt-0.5 line-clamp-1">{{ log.workDone || log.todayLog }}</p>
                </div>
                <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded-full bg-orange-500/10 text-orange-400 border border-orange-500/30 shrink-0 font-medium">
                  {{ log.attendanceMode || 'Office' }}
                </span>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- Right Column (1 col): Operations & Quick Governance -->
      <div class="space-y-4">
        
        <!-- Sprint Delivery Index Card -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono pb-2 border-b border-zinc-800">Sprint Delivery Index</h2>
          <div class="space-y-2 text-xs">
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">Active Sprint</span>
              <span class="font-mono text-white font-bold">{{ scrumStore.activeSprint?.name || 'Sprint' }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">Total Commitments</span>
              <span class="font-mono text-zinc-300">{{ scrumStore.tasks.length }} Tasks</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-zinc-400">Completion Velocity</span>
              <span class="font-mono text-orange-400 font-bold">{{ sprintProgressPercentage }}%</span>
            </div>
            <div class="w-full h-2 bg-zinc-950 rounded-full overflow-hidden border border-zinc-800 mt-1">
              <div class="bg-orange-500 h-full rounded-full transition-all duration-300" :style="{ width: `${sprintProgressPercentage}%` }"></div>
            </div>
          </div>
        </div>

        <!-- Quick Governance Actions -->
        <div class="bg-zinc-900 border border-zinc-800 rounded-xl p-5 space-y-3">
          <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono pb-2 border-b border-zinc-800">Executive Shortcuts</h2>
          <div class="space-y-2 text-xs">
            <router-link to="/admin/reports" class="p-2.5 bg-zinc-950 hover:bg-zinc-850 rounded border border-zinc-800 text-zinc-300 hover:text-white flex items-center justify-between transition-colors block">
              <span>Generate Daily Executive PDF</span>
              <span class="text-orange-400 font-mono">→</span>
            </router-link>
            <router-link to="/operations/mom" class="p-2.5 bg-zinc-950 hover:bg-zinc-850 rounded border border-zinc-800 text-zinc-300 hover:text-white flex items-center justify-between transition-colors block">
              <span>Minutes of Meeting (MoM)</span>
              <span class="text-orange-400 font-mono">→</span>
            </router-link>
            <router-link to="/operations/proposals" class="p-2.5 bg-zinc-950 hover:bg-zinc-850 rounded border border-zinc-800 text-zinc-300 hover:text-white flex items-center justify-between transition-colors block">
              <span>Improvement Proposals</span>
              <span class="text-orange-400 font-mono">→</span>
            </router-link>
          </div>
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { getApiBase } from '@/config'
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useScrumStore } from '../stores/scrum'
import { formatRoleTitle } from '../constants'

const authStore = useAuthStore()
const scrumStore = useScrumStore()

const allLogs = ref([])
const allUsers = ref([])
const allTeams = ref([])


// Today formatted
const todayFormatted = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
})

const todayDateString = computed(() => {
  return new Date().toISOString().split('T')[0]
})

// Role Category Checks
const isIntern = computed(() => authStore.isIntern)
const isScrumHead = computed(() => (authStore.user?.role || '').toLowerCase() === 'scrum_head')
const isAdmin = computed(() => (authStore.user?.role || '').toLowerCase() === 'admin')
const isExecutive = computed(() => !isIntern.value && !isScrumHead.value && !isAdmin.value)

// Role Description & Badges
const currentRoleBadge = computed(() => {
  const u = authStore.user
  if (!u) return 'Guest'
  return formatRoleTitle(u.role, u.positionTitle)
})

const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good Morning'
  if (hour < 18) return 'Good Afternoon'
  return 'Good Evening'
})

const roleDescription = computed(() => {
  if (isIntern.value) {
    return 'Your personal engineering sprint workspace. Track your assigned deliverables, submit work for review, and maintain your daily attendance.'
  }
  if (isScrumHead.value) {
    return `${scrumStore.activeSprint?.name || 'Active Sprint'} delivery and governance dashboard. Review intern submissions, balance team workload, and manage sprint progression.`
  }
  if (isAdmin.value) {
    return 'Enterprise system governance center. Review applicant access requests, manage user credentials, and monitor audit security.'
  }
  return 'High-level executive telemetry. Monitor company-wide attendance compliance, sprint deliverables completion, and operational initiatives.'
})

// Tasks Data
const myTasks = computed(() => {
  if (!authStore.user?.id) return []
  return scrumStore.tasks.filter(t => t.assignedToId === authStore.user.id || t.assignedToName === authStore.user.name)
})

const pendingReviewTasks = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'PENDING_APPROVAL')
})

const approvedTasksCount = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'APPROVED').length
})

const inProgressTasksCount = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'IN_PROGRESS').length
})

const todoTasksCount = computed(() => {
  return scrumStore.tasks.filter(t => t.status === 'TODO').length
})

const pendingApprovalsCount = computed(() => pendingReviewTasks.value.length)
const pendingUsersCount = computed(() => scrumStore.pendingUsers.length)

// Sprint Progress Percentage
const sprintProgressPercentage = computed(() => {
  if (scrumStore.tasks.length === 0) return 0
  return Math.round((approvedTasksCount.value / scrumStore.tasks.length) * 100)
})

// Today's Log Status for Current User
const myTodayLogs = computed(() => {
  if (!authStore.user?.name) return []
  return allLogs.value.filter(l => l.date === todayDateString.value && (l.name === authStore.user.name || l.userId === authStore.user.id))
})

const isLoggedToday = computed(() => myTodayLogs.value.length > 0)
const todayLogItem = computed(() => myTodayLogs.value[0] || null)

const myAllLogs = computed(() => {
  if (!authStore.user?.name) return []
  return allLogs.value.filter(l => l.name === authStore.user.name || l.userId === authStore.user.id)
})

const todayLogs = computed(() => {
  return allLogs.value.filter(l => l.date === todayDateString.value)
})

const internsList = computed(() => {
  return allUsers.value.filter(u => ['frontend_developer', 'backend_developer', 'devops_developer', 'intern'].includes((u.role || '').toLowerCase()))
})

const getInternTaskCount = (internId) => {
  return scrumStore.tasks.filter(t => t.assignedToId === internId && t.status !== 'APPROVED').length
}

const countByTeam = (teamName) => {
  const target = (teamName || '').toLowerCase().trim()
  if (!target) return 0
  return todayLogs.value.filter(l => {
    const userTeam = (l.team || '').toLowerCase().trim()
    return userTeam === target || userTeam.includes(target) || target.includes(userTeam)
  }).length
}

// 4 High-Signal KPIs per Role
const kpi1 = computed(() => {
  if (isIntern.value) {
    const active = myTasks.value.filter(t => ['TODO', 'IN_PROGRESS'].includes(t.status)).length
    return {
      label: 'My Active Tasks',
      value: active,
      subtext: 'Tasks to complete this sprint',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>'
    }
  }
  if (isScrumHead.value) {
    return {
      label: 'Sprint Velocity',
      value: `${sprintProgressPercentage.value}%`,
      subtext: `${approvedTasksCount.value} of ${scrumStore.tasks.length} tasks approved`,
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>'
    }
  }
  if (isAdmin.value) {
    return {
      label: 'Pending Access Requests',
      value: pendingUsersCount.value,
      highlight: pendingUsersCount.value > 0,
      subtext: 'Awaiting administrator verification',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>'
    }
  }
  // Executive
  const rate = allUsers.value.length > 0 ? Math.round((todayLogs.value.length / allUsers.value.length) * 100) : 0
  return {
    label: 'Attendance Compliance',
    value: `${rate}%`,
    subtext: `${todayLogs.value.length} of ${allUsers.value.length} logged today`,
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
  }
})

const kpi2 = computed(() => {
  if (isIntern.value) {
    const underReview = myTasks.value.filter(t => t.status === 'PENDING_APPROVAL').length
    return {
      label: 'Awaiting QA Review',
      value: underReview,
      subtext: 'Work submitted to Scrum Head',
      highlight: underReview > 0,
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    }
  }
  if (isScrumHead.value) {
    return {
      label: 'Review Queue Pending',
      value: pendingReviewTasks.value.length,
      subtext: 'Submissions needing decision',
      highlight: pendingReviewTasks.value.length > 0,
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    }
  }
  if (isAdmin.value) {
    return {
      label: 'Active Personnel',
      value: allUsers.value.length,
      subtext: 'Registered system accounts',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>'
    }
  }
  // Executive
  return {
    label: 'Sprint Delivery Index',
    value: `${sprintProgressPercentage.value}%`,
    subtext: `${approvedTasksCount.value} committed items delivered`,
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>'
  }
})

const kpi3 = computed(() => {
  if (isIntern.value) {
    return {
      label: 'Today\'s Work Log',
      value: isLoggedToday.value ? 'Recorded' : 'Pending',
      subtext: isLoggedToday.value ? 'Daily record submitted' : 'Log before 8:00 PM',
      highlight: !isLoggedToday.value,
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>'
    }
  }
  if (isScrumHead.value) {
    return {
      label: 'Active Tasks In Progress',
      value: inProgressTasksCount.value,
      subtext: 'Currently being developed',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>'
    }
  }
  if (isAdmin.value) {
    return {
      label: 'Teams & Departments',
      value: allTeams.value.length,
      subtext: 'Functional org units',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>'
    }
  }
  // Executive
  return {
    label: 'Deliverables Submitted',
    value: todayLogs.value.length,
    subtext: 'Daily work logs logged today',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>'
  }
})

const kpi4 = computed(() => {
  if (isIntern.value) {
    return {
      label: 'Days Logged',
      value: `${myAllLogs.value.length}`,
      unit: 'Days',
      subtext: 'Total attendance submissions',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'
    }
  }
  if (isScrumHead.value) {
    return {
      label: 'User Stories Backlog',
      value: scrumStore.stories.length,
      subtext: 'Defined stories in roadmap',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>'
    }
  }
  if (isAdmin.value) {
    return {
      label: 'Audit Events',
      value: scrumStore.auditLogs.length,
      subtext: 'Security and system mutations',
      icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>'
    }
  }
  // Executive
  return {
    label: 'Cycle Duration',
    value: scrumStore.activeSprint?.durationDays ? `${scrumStore.activeSprint.durationDays} Days` : (scrumStore.activeSprint ? 'Active' : 'Unscheduled'),
    subtext: scrumStore.activeSprint ? `${scrumStore.activeSprint.name} cadence` : 'Sprint cycle not configured',
    icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>'
  }
})

// Quick 1-click status actions
const quickUpdateTaskStatus = async (task, newStatus) => {
  await scrumStore.updateTaskStatus(task.id, newStatus, authStore.user?.id)
}

const quickApproveTask = async (task) => {
  try {
    await scrumStore.reviewTask(task.id, 'APPROVE', 'Approved from command center', authStore.user?.id || 1)
  } catch (err) {
    console.error('Error approving task:', err)
  }
}

const quickApproveUser = async (user) => {
  try {
    await scrumStore.approveUser(user.id, {
      role: user.requestedRole || 'intern',
      team: user.team || (allTeams.value.length > 0 ? allTeams.value[0].name : '')
    }, authStore.user?.id)
  } catch (err) {
    console.error('Error approving user:', err)
  }
}

const formatTaskStatus = (status) => {
  switch (status) {
    case 'TODO': return 'To Do'
    case 'IN_PROGRESS': return 'In Progress'
    case 'PENDING_APPROVAL': return 'In Review'
    case 'APPROVED': return 'Approved'
    default: return status
  }
}

const taskStatusClass = (status) => {
  switch (status) {
    case 'TODO': return 'bg-zinc-800 text-zinc-300 border-zinc-700'
    case 'IN_PROGRESS': return 'bg-orange-500/10 text-orange-400 border-orange-500/30'
    case 'PENDING_APPROVAL': return 'bg-amber-500/10 text-amber-400 border-amber-500/30'
    case 'APPROVED': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    default: return 'bg-zinc-800 text-zinc-400 border-zinc-700'
  }
}

const formatTime = (ts) => {
  if (!ts) return ''
  const d = new Date(ts)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Fetch Initial Data
onMounted(async () => {
  const roleParam = authStore.user?.role ? `?user_role=${encodeURIComponent(authStore.user.role)}` : ''
  await Promise.allSettled([
    scrumStore.fetchSprints(),
    scrumStore.fetchTasks(),
    scrumStore.fetchStories(),
    scrumStore.fetchPendingUsers(),
    scrumStore.fetchAuditLogs(),
    fetch(`${getApiBase()}/api/logs`).then(r => r.ok ? r.json() : []).then(d => { allLogs.value = d }),
    fetch(`${getApiBase()}/api/users`).then(r => r.ok ? r.json() : []).then(d => { allUsers.value = d }),
    fetch(`${getApiBase()}/api/teams${roleParam}`).then(r => r.ok ? r.json() : []).then(d => { allTeams.value = d })
  ])
})
</script>
