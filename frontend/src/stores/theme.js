import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const storedTheme = localStorage.getItem('fixly_theme') || 'dark'
  const currentTheme = ref(storedTheme)
  const isDark = ref(storedTheme === 'dark')

  const applyTheme = (theme) => {
    currentTheme.value = theme
    isDark.value = theme === 'dark'
    localStorage.setItem('fixly_theme', theme)

    const root = document.documentElement
    if (theme === 'light') {
      root.classList.add('light')
      root.classList.remove('dark')
    } else {
      root.classList.add('dark')
      root.classList.remove('light')
    }
    root.setAttribute('data-theme', theme)
  }

  const toggleTheme = () => {
    applyTheme(currentTheme.value === 'dark' ? 'light' : 'dark')
  }

  const initTheme = () => {
    applyTheme(currentTheme.value)
  }

  return {
    currentTheme,
    isDark,
    toggleTheme,
    applyTheme,
    initTheme
  }
})
