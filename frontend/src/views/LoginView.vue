<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-zinc-950">
    <div class="bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl w-full max-w-lg overflow-hidden relative z-10 transition-all duration-300">
      
      <!-- Top Brand Header -->
      <div class="p-6 text-center border-b border-zinc-800 bg-zinc-950">
        <!-- Fixly Brand Logo -->
        <div class="flex items-center justify-center mb-2.5">
          <img 
            src="/logo.png" 
            alt="Fixly" 
            class="w-12 h-12 object-contain drop-shadow-[0_4px_16px_rgba(231,138,68,0.25)] transition-transform hover:scale-105 duration-200" 
          />
        </div>

        <div class="flex items-center justify-center gap-1.5">
          <h1 class="text-xl font-bold tracking-tight text-white">
            Fixly Office
          </h1>
        </div>
        <p class="text-xs text-zinc-400 mt-0.5 font-normal">
          Scrum, Sprint & Workforce Management
        </p>
      </div>
      
      <div class="p-6 bg-zinc-900">
        
        <!-- Tab Selector: Google & Roles / Legacy Password / Admin Key -->
        <div class="grid grid-cols-3 gap-1 mb-5 bg-zinc-950 p-1 rounded border border-zinc-800 text-xs">
          <button 
            type="button"
            @click="authMode = 'google'" 
            :class="['py-2 rounded text-xs transition-colors cursor-pointer', 
              authMode === 'google' ? 'bg-orange-500 text-black font-bold shadow-sm' : 'text-zinc-400 hover:text-white']">
            Google
          </button>
          <button 
            type="button"
            @click="authMode = 'login'" 
            :class="['py-2 rounded text-xs transition-colors cursor-pointer', 
              authMode === 'login' ? 'bg-orange-500 text-black font-bold shadow-sm' : 'text-zinc-400 hover:text-white']">
            Employee ID
          </button>
          <button 
            type="button"
            @click="authMode = 'admin'" 
            :class="['py-2 rounded text-xs transition-colors cursor-pointer', 
              authMode === 'admin' ? 'bg-orange-500 text-black font-bold shadow-sm' : 'text-zinc-400 hover:text-white']">
            Admin Key
          </button>
        </div>

        <!-- Error Alert -->
        <div v-if="authStore.authError" class="mb-4 p-3 bg-zinc-950 border border-zinc-700 text-red-300 text-xs rounded flex items-center gap-2">
          <span class="font-medium">{{ authStore.authError }}</span>
        </div>

        <!-- Pending Approval Waiting Screen -->
        <div v-if="pendingApprovalUser" class="mb-5 p-5 bg-zinc-950 border border-zinc-800 rounded text-center space-y-2.5">
          <img src="/logo.png" alt="Fixly" class="w-9 h-9 mx-auto object-contain opacity-90 drop-shadow-sm" />
          <h3 class="text-sm font-semibold text-white">Registration Pending Approval</h3>
          <p class="text-xs text-zinc-400 leading-relaxed">
            Your application for <strong>{{ pendingApprovalUser.name }}</strong> ({{ pendingApprovalUser.email }}) is awaiting administrator approval.
          </p>
          <button 
            @click="checkApprovalStatus" 
            class="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-medium px-3 py-1.5 rounded transition-colors border border-zinc-700 cursor-pointer mt-1">
            Check Status Again
          </button>
        </div>

        <!-- MODE 1: GOOGLE SIGN-IN & DEMO ROLES SELECTOR -->
        <div v-if="authMode === 'google'" class="space-y-5">
          
          <!-- Google Sign-In Action -->
          <div class="space-y-3">
            <button 
              type="button"
              @click="triggerGoogleSignInPrompt"
              :disabled="authStore.isLoading"
              class="w-full btn-google font-semibold py-2.5 px-4 rounded-lg transition-all text-xs flex items-center justify-center gap-2.5 cursor-pointer disabled:opacity-50">
              <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
              </svg>
              <span class="font-semibold text-xs tracking-normal" style="color: #1f2937 !important;">
                {{ authStore.isLoading ? 'Verifying with Google...' : 'Continue with Google' }}
              </span>
            </button>
          </div>
        </div>

        <!-- MODE 2: EMPLOYEE ID / PASSWORD LOGIN -->
        <form v-if="authMode === 'login'" @submit.prevent="handleLogin" class="space-y-3.5">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Employee ID</label>
            <input 
              type="text" 
              required 
              v-model="loginRoll" 
              class="w-full rounded bg-zinc-950 border border-zinc-700 text-white placeholder-zinc-500 py-2.5 px-3 text-xs focus:border-zinc-500 outline-none uppercase tracking-wider font-mono" 
              placeholder="e.g. FX-1001"
            />
          </div>

          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Password</label>
            <input 
              type="password" 
              required 
              v-model="loginPass" 
              class="w-full rounded bg-zinc-950 border border-zinc-700 text-white placeholder-zinc-500 py-2.5 px-3 text-xs focus:border-zinc-500 outline-none" 
              placeholder="••••••••"
            />
          </div>

          <button 
            type="submit" 
            :disabled="authStore.isLoading" 
            class="w-full bg-orange-500 hover:bg-orange-400 text-black font-bold py-2.5 rounded transition-colors text-xs mt-2 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60">
            <span>Sign In to Fixly Workspace</span>
          </button>
        </form>

        <!-- MODE 3: ADMIN / EXECUTIVE ACCESS -->
        <form v-if="authMode === 'admin'" @submit.prevent="handleAdminLogin" class="space-y-3.5">
          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Admin Username</label>
            <input 
              type="text" 
              required 
              v-model="adminUser" 
              class="w-full rounded bg-zinc-950 border border-zinc-700 text-white placeholder-zinc-500 py-2.5 px-3 text-xs focus:border-zinc-500 outline-none" 
              placeholder="admin or viewer"
            />
          </div>

          <div>
            <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider mb-1">Password</label>
            <input 
              type="password" 
              required 
              v-model="adminPass" 
              class="w-full rounded bg-zinc-950 border border-zinc-700 text-white placeholder-zinc-500 py-2.5 px-3 text-xs focus:border-zinc-500 outline-none" 
              placeholder="Enter your password"
            />
          </div>

          <button 
            type="submit" 
            :disabled="authStore.isLoading" 
            class="w-full bg-orange-500 hover:bg-orange-400 text-black font-bold py-2.5 rounded transition-colors text-xs mt-2 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60">
            <span>Access Administrator Portal</span>
          </button>
        </form>

        <!-- Footer Info -->
        <div class="mt-6 pt-4 border-t border-zinc-800 text-center text-xs text-zinc-500 flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            <img src="/logo.png" alt="Fixly" class="w-3.5 h-3.5 object-contain opacity-60" />
            <span>Fixly Enterprise Office</span>
          </div>
          <span class="font-mono text-[10px]">v2.4.0</span>
        </div>

      </div>
    </div>

    <!-- Applicant Onboarding Modal -->
    <div v-if="showOnboardModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80">
      <div class="bg-zinc-900 border border-zinc-800 rounded-lg p-6 max-w-md w-full shadow-xl space-y-4">
        <div class="pb-3 border-b border-zinc-800 flex items-center gap-3">
          <img src="/logo.png" alt="Fixly" class="w-8 h-8 object-contain shrink-0" />
          <div>
            <h3 class="text-base font-bold text-white">Select Your Intern Track</h3>
            <p class="text-xs text-zinc-400 mt-0.5">Welcome, {{ authStore.onboardingName }}. Select your engineering track to complete registration.</p>
          </div>
        </div>

        <div class="space-y-2">
          <label 
            v-for="track in INTERN_TRACKS"
            :key="track.id"
            :class="[
              'block p-3 rounded border text-xs cursor-pointer transition-colors',
              selectedTrack === track.id ? 'bg-orange-500/10 border-orange-500/40 text-white font-semibold' : 'bg-zinc-950 border-zinc-800 text-zinc-300 hover:border-zinc-700'
            ]">
            <input type="radio" :value="track.id" v-model="selectedTrack" class="sr-only" />
            <div class="font-semibold">{{ track.title }}</div>
            <div class="text-[11px] text-zinc-400 mt-0.5">{{ track.description }}</div>
          </label>
        </div>

        <div class="pt-2 flex items-center justify-end gap-2.5">
          <button 
            @click="showOnboardModal = false"
            class="px-3 py-1.5 rounded text-xs text-zinc-400 hover:text-white">
            Cancel
          </button>
          <button 
            @click="submitOnboarding"
            class="bg-orange-500 hover:bg-orange-400 text-black font-bold px-4 py-2 rounded text-xs cursor-pointer">
            Submit for Admin Approval
          </button>
        </div>
      </div>
    </div>

    <!-- Global Persistent Footer for Login Page -->
    <footer class="fixed bottom-0 left-0 right-0 py-2.5 px-4 text-zinc-500 text-xs border-t border-zinc-900 bg-zinc-950/95 backdrop-blur-sm z-20">
      <div class="max-w-6xl mx-auto flex items-center justify-center gap-2 text-zinc-500">
        <img src="/logo.png" alt="Fixly" class="w-3.5 h-3.5 object-contain opacity-40" />
        <span class="text-[11px]">&copy; 2026 Fixly Services &middot; Powered by SyncIntent</span>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { getApiBase } from '@/config'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { supabase } from '@/supabase'

const router = useRouter()
const authStore = useAuthStore()

const authMode = ref('google')
const showManualGoogleInput = ref(false)
const customGoogleEmail = ref('')
const pendingApprovalUser = ref(null)

const loginRoll = ref('')
const loginPass = ref('')

const adminUser = ref('')
const adminPass = ref('')

const showOnboardModal = ref(false)
const selectedTrack = ref('frontend_developer')

const INTERN_TRACKS = [
  { id: 'frontend_developer', title: 'Frontend Developer Intern', description: 'Vue 3, Tailwind CSS, UI/UX Components' },
  { id: 'backend_developer', title: 'Backend Developer Intern', description: 'FastAPI, Python, SQLAlchemy, REST APIs' },
  { id: 'devops_developer', title: 'DevOps Developer Intern', description: 'CI/CD, Docker, Cloud Deployments, Health Monitoring' }
]

const redirectUser = () => {
  router.push('/dashboard')
}

const triggerGoogleSignInPrompt = async () => {
  await authStore.initiateGoogleLogin()
}


const submitOnboarding = async () => {
  const result = await authStore.onboardRole(
    authStore.onboardingName,
    authStore.onboardingEmail,
    selectedTrack.value
  )
  showOnboardModal.value = false
  if (result?.status === 'PENDING_APPROVAL') {
    pendingApprovalUser.value = result.data.user
  }
}

const checkApprovalStatus = async () => {
  if (!pendingApprovalUser.value) return
  const res = await fetch(`${getApiBase()}/api/auth/me?user_id=${pendingApprovalUser.value.id}`)
  if (res.ok) {
    const data = await res.json()
    if (data.user.accountStatus === 'ACTIVE') {
      authStore.user = data.user
      authStore.permissions = data.permissions
      localStorage.setItem('fixlyUser', JSON.stringify(data.user))
      localStorage.setItem('fixlyPermissions', JSON.stringify(data.permissions))
      pendingApprovalUser.value = null
      redirectUser()
    } else {
      alert('Your account is still pending administrator approval.')
    }
  }
}

const handleLogin = async () => {
  const success = await authStore.login(loginRoll.value, loginPass.value)
  if (success) {
    redirectUser()
  }
}

const handleAdminLogin = async () => {
  const success = await authStore.adminLogin(adminUser.value, adminPass.value)
  if (success) {
    redirectUser()
  }
}

onMounted(async () => {
  if (authStore.user && !authStore.isPendingApproval) {
    redirectUser()
    return
  }
  
  // Check for Supabase session after redirect
  const { data: { session } } = await supabase.auth.getSession()
  if (session) {
    const result = await authStore.processSupabaseSession(session)
    if (result?.status === 'SUCCESS') {
      redirectUser()
    } else if (result?.status === 'ONBOARDING_REQUIRED') {
      showOnboardModal.value = true
    } else if (result?.status === 'PENDING_APPROVAL') {
      pendingApprovalUser.value = result.data.user
    }
  }
})
</script>