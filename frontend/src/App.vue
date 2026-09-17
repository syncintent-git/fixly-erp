<template>
  <div class="min-h-screen bg-zinc-950 text-zinc-100 font-sans antialiased selection:bg-zinc-700 selection:text-white">
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/supabase'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  supabase.auth.onAuthStateChange(async (event, session) => {
    if (event === 'SIGNED_IN') {
      console.log('Supabase user signed in event received')
    } else if (event === 'SIGNED_OUT') {
      console.log('Supabase user signed out event received')
      if (authStore.user) {
        await authStore.logout()
      }
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
    }
  })
})
</script>