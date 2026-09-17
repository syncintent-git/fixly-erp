import { getApiBase } from '@/config'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { supabase } from '@/supabase'


export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('fixlyUser') || localStorage.getItem('trackerUser')) || null)
  const permissions = ref(JSON.parse(localStorage.getItem('fixlyPermissions')) || {
    canAccessAdmin: false,
    isViewOnly: false,
    canManageScrum: false,
    isIntern: false
  })
  const authError = ref('')
  const isLoading = ref(false)
  const onboardingEmail = ref('')
  const onboardingName = ref('')

  // Computed Role Capabilities
  const canAccessAdmin = computed(() => {
    if (!user.value) return false
    const r = (user.value.role || '').toLowerCase()
    return ['admin', 'ceo', 'cto', 'mentor', 'cdc', 'coo', 'cfo', 'cmo', 'viewer'].includes(r)
  })

  const isViewOnly = computed(() => {
    if (!user.value) return false
    const r = (user.value.role || '').toLowerCase()
    return ['cdc', 'mentor', 'viewer', 'cfo', 'cmo'].includes(r)
  })

  const canManageScrum = computed(() => {
    if (!user.value) return false
    const r = (user.value.role || '').toLowerCase()
    return ['scrum_head', 'admin', 'ceo', 'cto', 'coo'].includes(r)
  })

  const isIntern = computed(() => {
    if (!user.value) return false
    const r = (user.value.role || '').toLowerCase()
    return ['frontend_developer', 'backend_developer', 'devops_developer', 'intern', 'student', 'user'].includes(r)
  })

  const isPendingApproval = computed(() => {
    return user.value?.accountStatus === 'PENDING_APPROVAL'
  })

  function setSession(userData, permsData) {
    user.value = userData
    localStorage.setItem('fixlyUser', JSON.stringify(userData))
    localStorage.setItem('trackerUser', JSON.stringify(userData))
    if (permsData) {
      permissions.value = permsData
      localStorage.setItem('fixlyPermissions', JSON.stringify(permsData))
    }
  }

  // 1. Google OAuth Sign-In
  async function initiateGoogleLogin() {
    isLoading.value = true
    authError.value = ''
    try {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: window.location.origin + '/login',
          queryParams: {
            prompt: 'select_account' // Forces Google to show the account picker
          }
        }
      })
      if (error) throw error
    } catch (err) {
      authError.value = 'Unable to initiate Google sign-in.'
      isLoading.value = false
    }
  }

  async function processSupabaseSession(session) {
    isLoading.value = true
    authError.value = ''
    try {
      // Send the Supabase access token to our Python backend
      const res = await fetch(`${getApiBase()}/api/auth/google`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          credential: session.access_token,
          email: session.user?.email
        })
      })
      const data = await res.json()

      if (res.ok) {
        if (data.status === 'ONBOARDING_REQUIRED') {
          onboardingEmail.value = data.email
          onboardingName.value = data.name
          return { status: 'ONBOARDING_REQUIRED', data }
        }

        if (data.status === 'PENDING_APPROVAL') {
          setSession(data.user, data.permissions)
          return { status: 'PENDING_APPROVAL', data }
        }

        setSession(data.user, data.permissions)
        return { status: 'SUCCESS', data }
      } else {
        authError.value = data.detail || 'Google sign-in failed. Please try again.'
        return { status: 'ERROR', error: authError.value }
      }
    } catch (err) {
      authError.value = 'Unable to connect to authentication server.'
      return { status: 'ERROR', error: authError.value }
    } finally {
      isLoading.value = false
    }
  }

  // 2. Onboard Intern Role
  async function onboardRole(name, email, requestedRole) {
    isLoading.value = true
    authError.value = ''
    try {
      const res = await fetch(`${getApiBase()}/api/auth/onboard-role`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, requestedRole })
      })
      const data = await res.json()
      if (res.ok) {
        setSession(data.user, data.permissions)
        return { status: 'PENDING_APPROVAL', data }
      } else {
        authError.value = data.detail || 'Failed to submit role selection.'
        return { status: 'ERROR', error: authError.value }
      }
    } catch (err) {
      authError.value = 'Server connection error.'
      return { status: 'ERROR', error: authError.value }
    } finally {
      isLoading.value = false
    }
  }

  // 3. Demo 1-Click Role Login
  async function demoLogin(role, email = null) {
    isLoading.value = true
    authError.value = ''
    try {
      const res = await fetch(`${getApiBase()}/api/auth/demo`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role, email })
      })
      if (res.ok) {
        const data = await res.json()
        setSession(data.user, data.permissions)
        return true
      } else {
        const errData = await res.json().catch(() => ({}))
        authError.value = errData.detail || 'Demo login failed'
        return false
      }
    } catch (err) {
      authError.value = 'Unable to connect to server.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 4. Existing Roll Number / Password Login
  async function login(rollNumber, password) {
    isLoading.value = true
    authError.value = ''
    try {
      const res = await fetch(`${getApiBase()}/api/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rollNumber: rollNumber.trim().toUpperCase(), password })
      })
      if (res.ok) {
        const data = await res.json()
        setSession(data, null)
        return true
      } else {
        const errData = await res.json().catch(() => ({}))
        authError.value = errData.detail || 'Employee ID not found or password incorrect.'
        return false
      }
    } catch (err) {
      authError.value = 'Unable to connect to server.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 5. Existing Admin Login
  async function adminLogin(username, password) {
    isLoading.value = true
    authError.value = ''
    try {
      const res = await fetch(`${getApiBase()}/api/users/admin-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username.trim(), password })
      })
      if (res.ok) {
        const data = await res.json()
        setSession(data, { canAccessAdmin: true, isViewOnly: data.role === 'viewer', canManageScrum: true, isIntern: false })
        return true
      } else {
        authError.value = 'Invalid administrator credentials.'
        return false
      }
    } catch (err) {
      authError.value = 'Unable to connect to server.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  function logout() {
    user.value = null
    permissions.value = { canAccessAdmin: false, isViewOnly: false, canManageScrum: false, isIntern: false }
    localStorage.removeItem('fixlyUser')
    localStorage.removeItem('trackerUser')
    localStorage.removeItem('fixlyPermissions')
  }

  return {
    user,
    permissions,
    authError,
    isLoading,
    onboardingEmail,
    onboardingName,
    canAccessAdmin,
    isViewOnly,
    canManageScrum,
    isIntern,
    isPendingApproval,
    initiateGoogleLogin,
    processSupabaseSession,
    onboardRole,
    demoLogin,
    login,
    adminLogin,
    logout
  }
})