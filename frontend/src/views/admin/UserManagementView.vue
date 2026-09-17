<template>
  <div class="space-y-5 w-full">
    
    <!-- Top Header -->
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-5 w-full">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5 text-xs text-zinc-400 font-mono">
            <span>ADMINISTRATION & GOVERNANCE</span>
            <span>•</span>
            <span>{{ users.length }} Personnel</span>
            <span>•</span>
            <span>{{ teams.length }} Teams</span>
          </div>
          <h1 class="text-xl sm:text-2xl font-bold text-white tracking-tight">Users & Team Management</h1>
          <p class="text-xs text-zinc-400 mt-0.5">Full administrative control over personnel profiles, department hierarchies, and system credentials.</p>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center gap-2.5 shrink-0" v-if="!authStore.isViewOnly">
          <button 
            v-if="activeTab === 'users'"
            @click="openCreateUserModal"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer shadow-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>
            <span>Add User</span>
          </button>
          <button 
            v-if="activeTab === 'teams'"
            @click="openCreateTeamModal"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold text-xs px-4 py-2 rounded transition-colors flex items-center gap-1.5 cursor-pointer shadow-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Create Team</span>
          </button>
        </div>
      </div>

      <!-- Quick Metrics Bar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 pt-4 border-t border-zinc-800/80">
        <div class="bg-zinc-950/60 p-2.5 rounded border border-zinc-800">
          <div class="text-[10px] font-mono uppercase text-zinc-400">Total Personnel</div>
          <div class="text-lg font-bold text-white mt-0.5">{{ users.length }}</div>
        </div>
        <div class="bg-zinc-950/60 p-2.5 rounded border border-zinc-800">
          <div class="text-[10px] font-mono uppercase text-emerald-400">Active Accounts</div>
          <div class="text-lg font-bold text-emerald-400 mt-0.5">{{ activeUsersCount }}</div>
        </div>
        <div class="bg-zinc-950/60 p-2.5 rounded border border-zinc-800">
          <div class="text-[10px] font-mono uppercase text-amber-400">Pending Approvals</div>
          <div class="text-lg font-bold text-amber-400 mt-0.5">{{ pendingUsersCount }}</div>
        </div>
        <div class="bg-zinc-950/60 p-2.5 rounded border border-zinc-800">
          <div class="text-[10px] font-mono uppercase text-orange-400">Departments / Teams</div>
          <div class="text-lg font-bold text-orange-400 mt-0.5">{{ teams.length }}</div>
        </div>
      </div>
    </div>

    <!-- Reviewer Notice -->
    <div v-if="authStore.isViewOnly" class="bg-zinc-900 border border-zinc-800 p-3 rounded text-xs text-zinc-400 flex items-center gap-2">
      <span class="w-2 h-2 rounded bg-amber-400 shrink-0"></span>
      <span><strong>Reviewer Mode:</strong> You have read-only access. Creating, editing, or deleting users and teams is restricted to workspace administrators.</span>
    </div>

    <!-- Toast Notification Banner -->
    <transition name="fade">
      <div v-if="toast.show" :class="['p-3 rounded text-xs flex items-center justify-between border shadow-lg', toast.type === 'error' ? 'bg-red-950/90 border-red-800 text-red-200' : 'bg-emerald-950/90 border-emerald-800 text-emerald-200']">
        <div class="flex items-center gap-2">
          <svg v-if="toast.type === 'error'" class="w-4 h-4 text-red-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <svg v-else class="w-4 h-4 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          <span>{{ toast.message }}</span>
        </div>
        <button @click="toast.show = false" class="text-zinc-400 hover:text-white font-bold ml-4">×</button>
      </div>
    </transition>

    <!-- Navigation Tabs -->
    <div class="flex items-center gap-2 border-b border-zinc-800">
      <button 
        @click="setTab('users')"
        :class="[
          'px-4 py-2.5 text-xs font-bold transition-all border-b-2 flex items-center gap-2 cursor-pointer',
          activeTab === 'users' 
            ? 'border-orange-500 text-orange-400 bg-zinc-900/40' 
            : 'border-transparent text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/20'
        ]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
        <span>Personnel & Users</span>
        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300">{{ users.length }}</span>
      </button>

      <button 
        @click="setTab('teams')"
        :class="[
          'px-4 py-2.5 text-xs font-bold transition-all border-b-2 flex items-center gap-2 cursor-pointer',
          activeTab === 'teams' 
            ? 'border-orange-500 text-orange-400 bg-zinc-900/40' 
            : 'border-transparent text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/20'
        ]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/></svg>
        <span>Teams & Departments</span>
        <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-300">{{ teams.length }}</span>
      </button>
    </div>

    <!-- ========================================================================= -->
    <!-- TAB 1: USERS & PERSONNEL MANAGEMENT -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'users'" class="space-y-4">
      
      <!-- Filter & Search Bar -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
        <div class="flex items-center gap-2 flex-1 min-w-[240px]">
          <svg class="w-4 h-4 text-zinc-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search by name, email, or employee ID..." 
            class="w-full bg-transparent text-xs text-white placeholder-zinc-500 outline-none"
          />
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <!-- Role Filter -->
          <select v-model="filterRole" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs text-zinc-300 outline-none cursor-pointer">
            <option value="">All Roles</option>
            <option value="ceo">CEO</option>
            <option value="cto">CTO</option>
            <option value="coo">COO</option>
            <option value="cfo">CFO</option>
            <option value="cmo">CMO</option>
            <option value="admin">System Admin</option>
            <option value="scrum_head">Scrum Head</option>
            <option value="frontend_developer">Frontend Intern</option>
            <option value="backend_developer">Backend Intern</option>
            <option value="devops_developer">DevOps Intern</option>
            <option value="mentor">Program Head / Mentor</option>
            <option value="cdc">CDC Head</option>
            <option value="viewer">Executive Viewer</option>
          </select>

          <!-- Department Filter -->
          <select v-model="filterTeam" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs text-zinc-300 outline-none cursor-pointer">
            <option value="">All Departments</option>
            <option v-for="t in teams" :key="t.id" :value="t.name">{{ t.name }}</option>
            <option value="unassigned">Unassigned</option>
          </select>

          <!-- Status Filter -->
          <select v-model="filterStatus" class="bg-zinc-950 border border-zinc-700 rounded px-2.5 py-1.5 text-xs text-zinc-300 outline-none cursor-pointer">
            <option value="">All Statuses</option>
            <option value="ACTIVE">Active</option>
            <option value="PENDING_APPROVAL">Pending Approval</option>
            <option value="REJECTED">Rejected</option>
          </select>

          <!-- Reset -->
          <button 
            v-if="searchQuery || filterRole || filterTeam || filterStatus"
            @click="resetUserFilters"
            class="text-zinc-400 hover:text-white text-xs px-2 py-1 underline cursor-pointer">
            Clear
          </button>
        </div>
      </div>

      <!-- Users Table -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg overflow-hidden w-full">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-zinc-300">
            <thead class="bg-zinc-950 text-[10px] uppercase font-mono tracking-wider text-zinc-400 border-b border-zinc-800">
              <tr>
                <th class="py-3 px-4 font-bold">User</th>
                <th class="py-3 px-4 font-bold">Email</th>
                <th class="py-3 px-4 font-bold">Department</th>
                <th class="py-3 px-4 font-bold">System Role</th>
                <th class="py-3 px-4 font-bold">Position Title</th>
                <th class="py-3 px-4 font-bold">Status</th>
                <th class="py-3 px-4 font-bold text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-zinc-800">
              <tr v-if="filteredUsers.length === 0">
                <td colspan="7" class="py-8 text-center text-zinc-500 italic">No users found matching your criteria.</td>
              </tr>
              <tr 
                v-for="u in filteredUsers" 
                :key="u.id"
                class="hover:bg-zinc-850/60 transition-colors">
                
                <!-- Name & Avatar -->
                <td class="py-2.5 px-4 font-medium text-white flex items-center gap-2.5">
                  <div :class="['w-7 h-7 rounded flex items-center justify-center text-xs font-bold shrink-0 border', getAvatarStyle(u.role)]">
                    {{ (u.name || 'U').charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <div class="font-semibold text-zinc-100">{{ u.name }}</div>
                    <div class="text-[10px] font-mono text-zinc-500">{{ u.rollNumber || 'NO ID' }}</div>
                  </div>
                </td>

                <!-- Email -->
                <td class="py-2.5 px-4 font-mono text-zinc-400 text-xs">
                  {{ u.email || 'N/A' }}
                </td>

                <!-- Department -->
                <td class="py-2.5 px-4">
                  <span :class="['px-2 py-0.5 rounded text-[10px] font-mono border', u.team ? 'bg-zinc-950 text-zinc-300 border-zinc-800' : 'bg-zinc-950/40 text-zinc-500 border-zinc-800/60 italic']">
                    {{ u.team || 'Unassigned' }}
                  </span>
                </td>

                <!-- Role -->
                <td class="py-2.5 px-4">
                  <span :class="['text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-bold', getRoleBadgeStyle(u.role)]">
                    {{ formatRole(u.role) }}
                  </span>
                </td>

                <!-- Position Title -->
                <td class="py-2.5 px-4 text-zinc-300">
                  {{ u.positionTitle || formatRole(u.role) }}
                </td>

                <!-- Status -->
                <td class="py-2.5 px-4">
                  <span :class="['text-[10px] font-mono uppercase px-2 py-0.5 rounded border font-bold', getStatusBadgeStyle(u.accountStatus)]">
                    {{ u.accountStatus || 'ACTIVE' }}
                  </span>
                </td>

                <!-- Actions -->
                <td class="py-2.5 px-4 text-right">
                  <div class="flex items-center justify-end gap-1.5">
                    <button 
                      @click="openEditUserModal(u)"
                      :disabled="authStore.isViewOnly"
                      title="Edit User"
                      class="p-1.5 bg-zinc-800 hover:bg-zinc-700 disabled:opacity-40 disabled:cursor-not-allowed text-zinc-300 hover:text-white rounded border border-zinc-700 transition-colors cursor-pointer">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                    </button>
                    <button 
                      @click="openDeleteUserModal(u)"
                      :disabled="authStore.isViewOnly"
                      title="Delete User"
                      class="p-1.5 bg-zinc-800 hover:bg-red-900/60 disabled:opacity-40 disabled:cursor-not-allowed text-zinc-400 hover:text-red-300 rounded border border-zinc-700 transition-colors cursor-pointer">
                      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- TAB 2: TEAMS & DEPARTMENTS MANAGEMENT -->
    <!-- ========================================================================= -->
    <div v-if="activeTab === 'teams'" class="space-y-4">
      
      <!-- Teams Header & Quick Filter -->
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-3.5 flex flex-wrap items-center justify-between gap-3 w-full">
        <div class="flex items-center gap-2 flex-1 min-w-[240px]">
          <svg class="w-4 h-4 text-zinc-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input 
            type="text" 
            v-model="teamSearchQuery" 
            placeholder="Search departments and teams..." 
            class="w-full bg-transparent text-xs text-white placeholder-zinc-500 outline-none"
          />
        </div>

        <div class="flex items-center gap-3 text-xs text-zinc-400">
          <span>Assigned Staff: <strong class="text-white">{{ assignedUsersCount }}</strong></span>
          <span>•</span>
          <span>Unassigned: <strong class="text-amber-400">{{ unassignedUsersCount }}</strong></span>
        </div>
      </div>

      <!-- Teams Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="t in filteredTeams" 
          :key="t.id"
          class="bg-zinc-900 border border-zinc-800 rounded-lg p-4 space-y-3.5 hover:border-zinc-700 transition-colors flex flex-col justify-between">
          
          <div class="space-y-2">
            <div class="flex items-start justify-between gap-2">
              <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded bg-orange-500/10 border border-orange-500/30 flex items-center justify-center text-orange-400 shrink-0 font-bold text-xs">
                  {{ t.name.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <h3 class="text-sm font-bold text-white">{{ t.name }}</h3>
                  <span class="text-[10px] font-mono text-zinc-500">ID: TM-{{ t.id }}</span>
                </div>
              </div>

              <!-- Member Count Badge -->
              <span class="text-[10px] font-mono px-2 py-0.5 rounded border border-zinc-700 bg-zinc-950 text-zinc-300 font-bold flex items-center gap-1 shrink-0">
                <svg class="w-3 h-3 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                <span>{{ t.memberCount || 0 }} Members</span>
              </span>
            </div>

            <!-- Description -->
            <p class="text-xs text-zinc-400 line-clamp-2">
              {{ t.description || 'No department mission statement provided.' }}
            </p>

            <!-- Team Lead -->
            <div class="p-2 rounded bg-zinc-950 border border-zinc-850 flex items-center justify-between text-xs">
              <span class="text-zinc-500 text-[10px] font-mono uppercase">Team Lead</span>
              <span class="font-medium text-zinc-200 truncate max-w-[150px]">
                {{ t.leadName || 'Unassigned' }}
              </span>
            </div>
          </div>

          <!-- Card Bottom & Actions -->
          <div class="pt-3 border-t border-zinc-800/80 flex items-center justify-between gap-2">
            <button 
              @click="toggleTeamMembers(t.name)"
              class="text-[11px] text-zinc-400 hover:text-white flex items-center gap-1 transition-colors cursor-pointer">
              <span>{{ expandedTeamName === t.name ? 'Hide Staff' : 'View Staff' }}</span>
              <svg :class="['w-3 h-3 transition-transform', expandedTeamName === t.name ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>

            <div class="flex items-center gap-1.5" v-if="!authStore.isViewOnly">
              <button 
                @click="openEditTeamModal(t)"
                class="px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white text-xs rounded border border-zinc-700 transition-colors cursor-pointer">
                Edit
              </button>
              <button 
                @click="openDeleteTeamModal(t)"
                class="px-2 py-1 bg-zinc-800 hover:bg-red-900/60 text-zinc-400 hover:text-red-300 text-xs rounded border border-zinc-700 transition-colors cursor-pointer">
                Delete
              </button>
            </div>
          </div>

          <!-- Expanded Members Drawer -->
          <div v-if="expandedTeamName === t.name" class="mt-2 p-2.5 bg-zinc-950 rounded border border-zinc-800 space-y-2">
            <div class="text-[10px] font-mono uppercase text-zinc-500">Staff Assigned to {{ t.name }}:</div>
            <div v-if="getTeamMembers(t.name).length === 0" class="text-xs text-zinc-500 italic">No personnel currently assigned.</div>
            <div v-else class="space-y-1.5 max-h-40 overflow-y-auto pr-1">
              <div 
                v-for="m in getTeamMembers(t.name)" 
                :key="m.id"
                class="flex items-center justify-between text-xs p-1.5 rounded hover:bg-zinc-900 transition-colors">
                <div class="flex items-center gap-2 truncate">
                  <div class="w-5 h-5 rounded bg-zinc-800 text-zinc-300 text-[10px] flex items-center justify-center font-bold">
                    {{ (m.name || 'U').charAt(0).toUpperCase() }}
                  </div>
                  <span class="text-zinc-200 font-medium truncate">{{ m.name }}</span>
                </div>
                <span class="text-[10px] font-mono text-zinc-400 shrink-0">{{ formatRole(m.role) }}</span>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: ADD USER -->
    <!-- ========================================================================= -->
    <div v-if="showCreateUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white flex items-center gap-2">
            <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>
            <span>Add New User Account</span>
          </h3>
          <button @click="showCreateUserModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <form @submit.prevent="handleCreateUser" class="space-y-3.5 text-xs">
          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Full Name *</label>
            <input 
              type="text" 
              v-model="newUserForm.name"
              required
              placeholder="e.g. John Doe"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Email Address *</label>
              <input 
                type="email" 
                v-model="newUserForm.email"
                required
                placeholder="e.g. john@fixly.internal"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 font-mono"
              />
            </div>
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Employee ID / Roll Number</label>
              <input 
                type="text" 
                v-model="newUserForm.rollNumber"
                placeholder="e.g. FX-1008"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 font-mono"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">System Role</label>
              <select 
                v-model="newUserForm.role"
                @change="onRoleChange('new')"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
                <option value="frontend_developer">Frontend Developer Intern</option>
                <option value="backend_developer">Backend Developer Intern</option>
                <option value="devops_developer">DevOps Developer Intern</option>
                <option value="scrum_head">Scrum Head</option>
                <option value="admin">System Admin</option>
                <option value="ceo">CEO</option>
                <option value="cto">CTO</option>
                <option value="coo">COO</option>
                <option value="cfo">CFO</option>
                <option value="cmo">CMO</option>
                <option value="mentor">Program Head / Mentor</option>
                <option value="cdc">CDC Head</option>
                <option value="viewer">Executive Viewer</option>
              </select>
            </div>

            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Department / Team</label>
              <select 
                v-model="newUserForm.team"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
                <option value="">Unassigned</option>
                <option v-for="t in teams" :key="t.id" :value="t.name">{{ t.name }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Position Title</label>
            <input 
              type="text" 
              v-model="newUserForm.positionTitle"
              placeholder="e.g. Senior Frontend Engineer"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Account Status</label>
              <select 
                v-model="newUserForm.accountStatus"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
                <option value="ACTIVE">ACTIVE</option>
                <option value="PENDING_APPROVAL">PENDING_APPROVAL</option>
              </select>
            </div>

            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Initial Password</label>
              <input 
                type="text" 
                v-model="newUserForm.password"
                placeholder="Leave blank for system default"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 font-mono"
              />
            </div>
          </div>

          <div class="pt-3 border-t border-zinc-800 flex items-center justify-end gap-2.5">
            <button 
              type="button"
              @click="showCreateUserModal = false"
              class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-medium transition-colors">
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2 bg-orange-500 hover:bg-orange-400 text-black font-bold rounded transition-colors flex items-center gap-1.5">
              <span v-if="isSubmitting">Saving...</span>
              <span v-else>Create Account</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: EDIT USER -->
    <!-- ========================================================================= -->
    <div v-if="showEditUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-lg w-full shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              <span>Edit User Profile</span>
            </h3>
            <p class="text-[10px] text-zinc-400 font-mono mt-0.5">{{ editUserForm.name }} (ID: {{ editUserForm.id }})</p>
          </div>
          <button @click="showEditUserModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <form @submit.prevent="handleUpdateUser" class="space-y-3.5 text-xs">
          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Full Name *</label>
            <input 
              type="text" 
              v-model="editUserForm.name"
              required
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Email Address</label>
              <input 
                type="email" 
                v-model="editUserForm.email"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 font-mono"
              />
            </div>
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Employee ID / Roll Number</label>
              <input 
                type="text" 
                v-model="editUserForm.rollNumber"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 font-mono"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">System Role</label>
              <select 
                v-model="editUserForm.role"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
                <option value="frontend_developer">Frontend Developer Intern</option>
                <option value="backend_developer">Backend Developer Intern</option>
                <option value="devops_developer">DevOps Developer Intern</option>
                <option value="scrum_head">Scrum Head</option>
                <option value="admin">System Admin</option>
                <option value="ceo">CEO</option>
                <option value="cto">CTO</option>
                <option value="coo">COO</option>
                <option value="cfo">CFO</option>
                <option value="cmo">CMO</option>
                <option value="mentor">Program Head / Mentor</option>
                <option value="cdc">CDC Head</option>
                <option value="viewer">Executive Viewer</option>
              </select>
            </div>

            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Department / Team</label>
              <select 
                v-model="editUserForm.team"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
                <option value="">Unassigned</option>
                <option v-for="t in teams" :key="t.id" :value="t.name">{{ t.name }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Position Title</label>
            <input 
              type="text" 
              v-model="editUserForm.positionTitle"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Account Status</label>
              <select 
                v-model="editUserForm.accountStatus"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
                <option value="ACTIVE">ACTIVE</option>
                <option value="PENDING_APPROVAL">PENDING_APPROVAL</option>
                <option value="REJECTED">REJECTED</option>
              </select>
            </div>

            <div>
              <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Reset Password (Optional)</label>
              <input 
                type="text" 
                v-model="editUserForm.password"
                placeholder="Leave blank to keep current"
                class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 font-mono text-[11px]"
              />
            </div>
          </div>

          <div class="pt-3 border-t border-zinc-800 flex items-center justify-end gap-2.5">
            <button 
              type="button"
              @click="showEditUserModal = false"
              class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-medium transition-colors">
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2 bg-orange-500 hover:bg-orange-400 text-black font-bold rounded transition-colors flex items-center gap-1.5">
              <span v-if="isSubmitting">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: DELETE USER CONFIRMATION -->
    <!-- ========================================================================= -->
    <div v-if="showDeleteUserModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-md w-full shadow-2xl space-y-4">
        <div class="flex items-center gap-3 text-red-400">
          <div class="w-9 h-9 rounded-full bg-red-500/10 border border-red-500/30 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          </div>
          <div>
            <h3 class="text-base font-bold text-white">Delete User Account</h3>
            <p class="text-xs text-zinc-400">This action will remove the user permanently.</p>
          </div>
        </div>

        <p class="text-xs text-zinc-300 leading-relaxed bg-zinc-950 p-3 rounded border border-zinc-800">
          Are you sure you want to delete <strong class="text-white">{{ userToDelete?.name }}</strong> (<span class="font-mono text-zinc-400">{{ userToDelete?.email || 'No email' }}</span>)? 
          Any active tasks or stories assigned to this user will be set to Unassigned.
        </p>

        <div class="pt-2 flex items-center justify-end gap-2.5">
          <button 
            @click="showDeleteUserModal = false"
            class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs rounded font-medium transition-colors">
            Cancel
          </button>
          <button 
            @click="handleDeleteUser"
            :disabled="isSubmitting"
            class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-bold text-xs rounded transition-colors flex items-center gap-1.5">
            <span v-if="isSubmitting">Deleting...</span>
            <span v-else>Confirm Delete</span>
          </button>
        </div>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: CREATE TEAM -->
    <!-- ========================================================================= -->
    <div v-if="showCreateTeamModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-md w-full shadow-2xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <h3 class="text-base font-bold text-white flex items-center gap-2">
            <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
            <span>Create New Team / Department</span>
          </h3>
          <button @click="showCreateTeamModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <form @submit.prevent="handleCreateTeam" class="space-y-3.5 text-xs">
          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Team Name *</label>
            <input 
              type="text" 
              v-model="newTeamForm.name"
              required
              placeholder="e.g. AI Innovation Hub"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500"
            />
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Mission / Description</label>
            <textarea 
              v-model="newTeamForm.description"
              rows="3"
              placeholder="Describe department responsibilities, scope, and objectives..."
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Designated Team Lead (Optional)</label>
            <select 
              v-model="newTeamForm.leadId"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
              <option :value="null">No lead assigned</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.name }} ({{ formatRole(u.role) }})</option>
            </select>
          </div>

          <div class="pt-3 border-t border-zinc-800 flex items-center justify-end gap-2.5">
            <button 
              type="button"
              @click="showCreateTeamModal = false"
              class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-medium transition-colors">
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2 bg-orange-500 hover:bg-orange-400 text-black font-bold rounded transition-colors flex items-center gap-1.5">
              <span v-if="isSubmitting">Creating...</span>
              <span v-else>Create Team</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: EDIT TEAM -->
    <!-- ========================================================================= -->
    <div v-if="showEditTeamModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-md w-full shadow-2xl space-y-4">
        <div class="flex items-center justify-between pb-3 border-b border-zinc-800">
          <div>
            <h3 class="text-base font-bold text-white flex items-center gap-2">
              <svg class="w-4 h-4 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
              <span>Edit Team / Department</span>
            </h3>
            <p class="text-[10px] text-zinc-400 font-mono mt-0.5">ID: TM-{{ editTeamForm.id }}</p>
          </div>
          <button @click="showEditTeamModal = false" class="text-zinc-400 hover:text-white text-lg font-bold">×</button>
        </div>

        <form @submit.prevent="handleUpdateTeam" class="space-y-3.5 text-xs">
          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Team Name *</label>
            <input 
              type="text" 
              v-model="editTeamForm.name"
              required
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500"
            />
            <p class="text-[10px] text-orange-400/90 mt-1 flex items-center gap-1">
              <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <span>Renaming this team automatically updates all assigned personnel.</span>
            </p>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Mission / Description</label>
            <textarea 
              v-model="editTeamForm.description"
              rows="3"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 resize-none"
            ></textarea>
          </div>

          <div>
            <label class="block text-[10px] font-bold text-zinc-400 uppercase tracking-wider mb-1">Designated Team Lead</label>
            <select 
              v-model="editTeamForm.leadId"
              class="w-full bg-zinc-950 border border-zinc-700 rounded p-2.5 text-white outline-none focus:border-zinc-500 cursor-pointer">
              <option :value="null">No lead assigned</option>
              <option v-for="u in users" :key="u.id" :value="u.id">{{ u.name }} ({{ formatRole(u.role) }})</option>
            </select>
          </div>

          <div class="pt-3 border-t border-zinc-800 flex items-center justify-end gap-2.5">
            <button 
              type="button"
              @click="showEditTeamModal = false"
              class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded font-medium transition-colors">
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2 bg-orange-500 hover:bg-orange-400 text-black font-bold rounded transition-colors flex items-center gap-1.5">
              <span v-if="isSubmitting">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ========================================================================= -->
    <!-- MODAL: DELETE TEAM CONFIRMATION -->
    <!-- ========================================================================= -->
    <div v-if="showDeleteTeamModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-md w-full shadow-2xl space-y-4">
        <div class="flex items-center gap-3 text-red-400">
          <div class="w-9 h-9 rounded-full bg-red-500/10 border border-red-500/30 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
          </div>
          <div>
            <h3 class="text-base font-bold text-white">Delete Team / Department</h3>
            <p class="text-xs text-zinc-400">This will remove the team from the workspace.</p>
          </div>
        </div>

        <p class="text-xs text-zinc-300 leading-relaxed bg-zinc-950 p-3 rounded border border-zinc-800">
          Are you sure you want to delete <strong class="text-white">{{ teamToDelete?.name }}</strong>? 
          All <strong class="text-amber-400">{{ teamToDelete?.memberCount || 0 }} assigned personnel</strong> will be marked as "Unassigned". Existing logs and tasks remain safe.
        </p>

        <div class="pt-2 flex items-center justify-end gap-2.5">
          <button 
            @click="showDeleteTeamModal = false"
            class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs rounded font-medium transition-colors">
            Cancel
          </button>
          <button 
            @click="handleDeleteTeam"
            :disabled="isSubmitting"
            class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white font-bold text-xs rounded transition-colors flex items-center gap-1.5">
            <span v-if="isSubmitting">Deleting...</span>
            <span v-else>Confirm Delete</span>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { getApiBase } from '@/config'
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()


// Active Tab
const activeTab = ref(route.query.tab === 'teams' ? 'teams' : 'users')

const setTab = (tab) => {
  activeTab.value = tab
  router.replace({ query: { ...route.query, tab } })
}

watch(() => route.query.tab, (newTab) => {
  if (newTab === 'teams' || newTab === 'users') {
    activeTab.value = newTab
  }
})

// Data State
const users = ref([])
const teams = ref([])
const isSubmitting = ref(false)
const expandedTeamName = ref(null)

// Toast Alert State
const toast = ref({
  show: false,
  message: '',
  type: 'success'
})

const showToast = (message, type = 'success') => {
  toast.value = { show: true, message, type }
  setTimeout(() => {
    toast.value.show = false
  }, 4000)
}

// User Filters
const searchQuery = ref('')
const filterRole = ref('')
const filterTeam = ref('')
const filterStatus = ref('')

const resetUserFilters = () => {
  searchQuery.value = ''
  filterRole.value = ''
  filterTeam.value = ''
  filterStatus.value = ''
}

// Team Filters
const teamSearchQuery = ref('')

// Modal States
const showCreateUserModal = ref(false)
const showEditUserModal = ref(false)
const showDeleteUserModal = ref(false)
const userToDelete = ref(null)

const showCreateTeamModal = ref(false)
const showEditTeamModal = ref(false)
const showDeleteTeamModal = ref(false)
const teamToDelete = ref(null)

// Forms
const newUserForm = ref({
  name: '',
  email: '',
  rollNumber: '',
  team: '',
  role: 'frontend_developer',
  positionTitle: 'Frontend Developer Intern',
  accountStatus: 'ACTIVE',
  password: ''
})

const editUserForm = ref({
  id: null,
  name: '',
  email: '',
  rollNumber: '',
  team: '',
  role: '',
  positionTitle: '',
  accountStatus: 'ACTIVE',
  password: ''
})

const newTeamForm = ref({
  name: '',
  description: '',
  leadId: null
})

const editTeamForm = ref({
  id: null,
  name: '',
  description: '',
  leadId: null
})

// Metrics
const activeUsersCount = computed(() => {
  return users.value.filter(u => (u.accountStatus || 'ACTIVE') === 'ACTIVE').length
})

const pendingUsersCount = computed(() => {
  return users.value.filter(u => u.accountStatus === 'PENDING_APPROVAL').length
})

const assignedUsersCount = computed(() => {
  return users.value.filter(u => !!u.team).length
})

const unassignedUsersCount = computed(() => {
  return users.value.filter(u => !u.team).length
})

// Filtered Users
const filteredUsers = computed(() => {
  return users.value.filter(u => {
    const matchRole = !filterRole.value || (u.role || '').toLowerCase() === filterRole.value.toLowerCase()
    
    let matchTeam = true
    if (filterTeam.value === 'unassigned') {
      matchTeam = !u.team
    } else if (filterTeam.value) {
      matchTeam = (u.team || '').toLowerCase() === filterTeam.value.toLowerCase()
    }

    const matchStatus = !filterStatus.value || (u.accountStatus || 'ACTIVE') === filterStatus.value

    const q = searchQuery.value.toLowerCase().trim()
    const matchSearch = !q ||
      (u.name && u.name.toLowerCase().includes(q)) ||
      (u.email && u.email.toLowerCase().includes(q)) ||
      (u.rollNumber && u.rollNumber.toLowerCase().includes(q)) ||
      (u.positionTitle && u.positionTitle.toLowerCase().includes(q))

    return matchRole && matchTeam && matchStatus && matchSearch
  })
})

// Filtered Teams
const filteredTeams = computed(() => {
  if (!teamSearchQuery.value.trim()) return teams.value
  const q = teamSearchQuery.value.toLowerCase().trim()
  return teams.value.filter(t => 
    t.name.toLowerCase().includes(q) || 
    (t.description && t.description.toLowerCase().includes(q)) ||
    (t.leadName && t.leadName.toLowerCase().includes(q))
  )
})

// Helper: Format Role
const formatRole = (r) => {
  if (!r) return 'User'
  const roleMap = {
    'ceo': 'CEO',
    'cto': 'CTO',
    'coo': 'COO',
    'cfo': 'CFO',
    'cmo': 'CMO',
    'admin': 'Admin',
    'scrum_head': 'Scrum Head',
    'frontend_developer': 'Frontend Intern',
    'backend_developer': 'Backend Intern',
    'devops_developer': 'DevOps Intern',
    'mentor': 'Program Head / Mentor',
    'cdc': 'CDC Head',
    'viewer': 'Executive Viewer',
    'student': 'Student',
    'intern': 'Intern'
  }
  return roleMap[r.toLowerCase()] || r.replace(/_/g, ' ').toUpperCase()
}

// Helper: Role badge styling
const getRoleBadgeStyle = (r) => {
  const role = (r || '').toLowerCase()
  if (['ceo', 'cto', 'admin', 'coo'].includes(role)) {
    return 'border-orange-500/30 bg-orange-500/10 text-orange-400'
  } else if (['scrum_head'].includes(role)) {
    return 'border-indigo-500/30 bg-indigo-500/10 text-indigo-400'
  } else if (['frontend_developer', 'backend_developer', 'devops_developer'].includes(role)) {
    return 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
  } else if (['mentor', 'cdc'].includes(role)) {
    return 'border-purple-500/30 bg-purple-500/10 text-purple-400'
  }
  return 'border-zinc-700 bg-zinc-800 text-zinc-300'
}

// Helper: Avatar styling
const getAvatarStyle = (r) => {
  const role = (r || '').toLowerCase()
  if (['ceo', 'cto', 'admin'].includes(role)) {
    return 'bg-orange-500/10 border-orange-500/30 text-orange-400'
  } else if (role === 'scrum_head') {
    return 'bg-indigo-500/10 border-indigo-500/30 text-indigo-400'
  } else if (['frontend_developer', 'backend_developer', 'devops_developer'].includes(role)) {
    return 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
  }
  return 'bg-zinc-800 border-zinc-700 text-zinc-300'
}

// Helper: Status badge styling
const getStatusBadgeStyle = (status) => {
  const s = (status || 'ACTIVE').toUpperCase()
  if (s === 'ACTIVE') return 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
  if (s === 'PENDING_APPROVAL') return 'border-amber-500/30 bg-amber-500/10 text-amber-400'
  if (s === 'REJECTED') return 'border-red-500/30 bg-red-500/10 text-red-400'
  return 'border-zinc-700 bg-zinc-800 text-zinc-400'
}

// Auto-fill position title on role change
const onRoleChange = (target) => {
  const titles = {
    'frontend_developer': 'Frontend Developer Intern',
    'backend_developer': 'Backend Developer Intern',
    'devops_developer': 'DevOps Developer Intern',
    'scrum_head': 'Scrum Head',
    'admin': 'System Administrator',
    'ceo': 'Chief Executive Officer',
    'cto': 'Chief Technology Officer',
    'coo': 'Chief Operating Officer',
    'cfo': 'Chief Financial Officer',
    'cmo': 'Chief Marketing Officer',
    'mentor': 'Program Head / Mentor',
    'cdc': 'Career Development Center Coordinator',
    'viewer': 'Executive Viewer'
  }
  if (target === 'new') {
    newUserForm.value.positionTitle = titles[newUserForm.value.role] || formatRole(newUserForm.value.role)
  }
}

// Members for expanded team
const getTeamMembers = (teamName) => {
  if (!teamName) return []
  return users.value.filter(u => (u.team || '').toLowerCase() === teamName.toLowerCase())
}

const toggleTeamMembers = (teamName) => {
  if (expandedTeamName.value === teamName) {
    expandedTeamName.value = null
  } else {
    expandedTeamName.value = teamName
  }
}

// API: Fetch Users
const fetchUsers = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/users/all`)
    if (res.ok) {
      users.value = await res.json()
    }
  } catch (err) {
    console.error('Error loading users:', err)
  }
}

// API: Fetch Teams
const fetchTeams = async () => {
  try {
    const res = await fetch(`${getApiBase()}/api/teams/`)
    if (res.ok) {
      teams.value = await res.json()
    }
  } catch (err) {
    console.error('Error loading teams:', err)
  }
}

// Modal Handlers: User
const openCreateUserModal = () => {
  newUserForm.value = {
    name: '',
    email: '',
    rollNumber: `FX-${Math.floor(1000 + Math.random() * 9000)}`,
    team: teams.value.length > 0 ? teams.value[0].name : '',
    role: 'frontend_developer',
    positionTitle: 'Frontend Developer Intern',
    accountStatus: 'ACTIVE',
    password: ''
  }
  showCreateUserModal.value = true
}

const handleCreateUser = async () => {
  isSubmitting.value = true
  try {
    const res = await fetch(`${getApiBase()}/api/users/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newUserForm.value)
    })
    const data = await res.json()
    if (res.ok) {
      showToast(`User '${data.name}' created successfully!`)
      showCreateUserModal.value = false
      await fetchUsers()
      await fetchTeams()
    } else {
      showToast(data.detail || 'Failed to create user', 'error')
    }
  } catch (err) {
    showToast('Failed to connect to server', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const openEditUserModal = (user) => {
  editUserForm.value = {
    id: user.id,
    name: user.name,
    email: user.email || '',
    rollNumber: user.rollNumber || '',
    team: user.team || '',
    role: user.role || 'intern',
    positionTitle: user.positionTitle || formatRole(user.role),
    accountStatus: user.accountStatus || 'ACTIVE',
    password: ''
  }
  showEditUserModal.value = true
}

const handleUpdateUser = async () => {
  isSubmitting.value = true
  try {
    const payload = {
      name: editUserForm.value.name,
      email: editUserForm.value.email || null,
      rollNumber: editUserForm.value.rollNumber || null,
      team: editUserForm.value.team || '',
      role: editUserForm.value.role,
      positionTitle: editUserForm.value.positionTitle,
      accountStatus: editUserForm.value.accountStatus
    }
    if (editUserForm.value.password && editUserForm.value.password.trim()) {
      payload.password = editUserForm.value.password.trim()
    }

    const res = await fetch(`${getApiBase()}/api/users/${editUserForm.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (res.ok) {
      showToast(`User '${data.name}' updated successfully!`)
      showEditUserModal.value = false
      await fetchUsers()
      await fetchTeams()
    } else {
      showToast(data.detail || 'Failed to update user', 'error')
    }
  } catch (err) {
    showToast('Failed to connect to server', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const openDeleteUserModal = (user) => {
  userToDelete.value = user
  showDeleteUserModal.value = true
}

const handleDeleteUser = async () => {
  if (!userToDelete.value) return
  isSubmitting.value = true
  try {
    const res = await fetch(`${getApiBase()}/api/users/${userToDelete.value.id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      showToast(`User '${userToDelete.value.name}' deleted successfully!`)
      showDeleteUserModal.value = false
      userToDelete.value = null
      await fetchUsers()
      await fetchTeams()
    } else {
      const data = await res.json()
      showToast(data.detail || 'Failed to delete user', 'error')
    }
  } catch (err) {
    showToast('Failed to delete user', 'error')
  } finally {
    isSubmitting.value = false
  }
}

// Modal Handlers: Team
const openCreateTeamModal = () => {
  newTeamForm.value = {
    name: '',
    description: '',
    leadId: null
  }
  showCreateTeamModal.value = true
}

const handleCreateTeam = async () => {
  isSubmitting.value = true
  try {
    const res = await fetch(`${getApiBase()}/api/teams/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTeamForm.value)
    })
    const data = await res.json()
    if (res.ok) {
      showToast(`Team '${data.name}' created successfully!`)
      showCreateTeamModal.value = false
      await fetchTeams()
    } else {
      showToast(data.detail || 'Failed to create team', 'error')
    }
  } catch (err) {
    showToast('Failed to connect to server', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const openEditTeamModal = (team) => {
  editTeamForm.value = {
    id: team.id,
    name: team.name,
    description: team.description || '',
    leadId: team.leadId || null
  }
  showEditTeamModal.value = true
}

const handleUpdateTeam = async () => {
  isSubmitting.value = true
  try {
    const res = await fetch(`${getApiBase()}/api/teams/${editTeamForm.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editTeamForm.value)
    })
    const data = await res.json()
    if (res.ok) {
      showToast(`Team '${data.name}' updated successfully!`)
      showEditTeamModal.value = false
      await fetchTeams()
      await fetchUsers()
    } else {
      showToast(data.detail || 'Failed to update team', 'error')
    }
  } catch (err) {
    showToast('Failed to connect to server', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const openDeleteTeamModal = (team) => {
  teamToDelete.value = team
  showDeleteTeamModal.value = true
}

const handleDeleteTeam = async () => {
  if (!teamToDelete.value) return
  isSubmitting.value = true
  try {
    const res = await fetch(`${getApiBase()}/api/teams/${teamToDelete.value.id}`, {
      method: 'DELETE'
    })
    if (res.ok) {
      showToast(`Team '${teamToDelete.value.name}' deleted successfully!`)
      showDeleteTeamModal.value = false
      teamToDelete.value = null
      await fetchTeams()
      await fetchUsers()
    } else {
      const data = await res.json()
      showToast(data.detail || 'Failed to delete team', 'error')
    }
  } catch (err) {
    showToast('Failed to delete team', 'error')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchUsers()
  fetchTeams()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
