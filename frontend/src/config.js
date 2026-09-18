// Global configuration
export const getApiBase = () => {
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  // In development, default to local backend; in production, use same-origin relative path
  return import.meta.env.DEV ? 'http://localhost:8000' : ''
}
