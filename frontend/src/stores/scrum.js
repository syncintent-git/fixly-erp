import { getApiBase } from '@/config'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'


export const useScrumStore = defineStore('scrum', () => {
  // State
  const sprints = ref([])
  const activeSprint = ref(null)
  const stories = ref([])
  const tasks = ref([])
  const pendingUsers = ref([])
  const notifications = ref([])
  const auditLogs = ref([])
  const loading = ref(false)
  const error = ref('')

  // Computed
  const unreadNotificationCount = computed(() => {
    return notifications.value.filter(n => !n.isRead).length
  })

  const pendingApprovalsCount = computed(() => {
    return tasks.value.filter(t => t.status === 'PENDING_APPROVAL').length
  })

  // --- SPRINT ACTIONS ---
  async function fetchSprints() {
    loading.value = true
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/sprints`)
      if (res.ok) {
        sprints.value = await res.json()
        if (sprints.value.length > 0 && !activeSprint.value) {
          activeSprint.value = sprints.value.find(s => s.status === 'ACTIVE') || sprints.value[0]
        }
      }
    } catch (err) {
      console.error('Error fetching sprints:', err)
    } finally {
      loading.value = false
    }
  }

  async function createSprint(sprintData, userId = null) {
    loading.value = true
    try {
      const url = userId ? `${getApiBase()}/api/scrum/sprints?user_id=${userId}` : `${getApiBase()}/api/scrum/sprints`
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sprintData)
      })
      if (res.ok) {
        const newSprint = await res.json()
        sprints.value.unshift(newSprint)
        activeSprint.value = newSprint
        return newSprint
      }
    } catch (err) {
      console.error('Error creating sprint:', err)
    } finally {
      loading.value = false
    }
  }

  async function updateSprint(sprintId, updateData) {
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/sprints/${sprintId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData)
      })
      if (res.ok) {
        const updated = await res.json()
        const idx = sprints.value.findIndex(s => s.id === sprintId)
        if (idx !== -1) sprints.value[idx] = updated
        if (activeSprint.value?.id === sprintId) activeSprint.value = updated
        return updated
      }
    } catch (err) {
      console.error('Error updating sprint:', err)
    }
  }

  async function rolloverSprint(sprintId, targetSprintId) {
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/sprints/${sprintId}/rollover?target_sprint_id=${targetSprintId}`, {
        method: 'POST'
      })
      if (res.ok) {
        await fetchSprints()
        await fetchTasks()
        return await res.json()
      }
    } catch (err) {
      console.error('Error rolling over sprint:', err)
    }
  }

  // --- STORY ACTIONS ---
  async function fetchStories(sprintId = null) {
    try {
      const url = sprintId ? `${getApiBase()}/api/scrum/stories?sprint_id=${sprintId}` : `${getApiBase()}/api/scrum/stories`
      const res = await fetch(url)
      if (res.ok) {
        stories.value = await res.json()
      }
    } catch (err) {
      console.error('Error fetching stories:', err)
    }
  }

  async function createStory(storyData, userId = null) {
    try {
      const url = userId ? `${getApiBase()}/api/scrum/stories?user_id=${userId}` : `${getApiBase()}/api/scrum/stories`
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(storyData)
      })
      if (res.ok) {
        const newStory = await res.json()
        stories.value.unshift(newStory)
        return newStory
      }
    } catch (err) {
      console.error('Error creating story:', err)
    }
  }

  async function updateStory(storyId, updateData) {
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/stories/${storyId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updateData)
      })
      if (res.ok) {
        const updated = await res.json()
        const idx = stories.value.findIndex(s => s.id === storyId)
        if (idx !== -1) stories.value[idx] = updated
        return updated
      }
    } catch (err) {
      console.error('Error updating story:', err)
    }
  }

  async function deleteStory(storyId) {
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/stories/${storyId}`, {
        method: 'DELETE'
      })
      if (res.ok) {
        stories.value = stories.value.filter(s => s.id !== storyId)
        tasks.value = tasks.value.filter(t => t.storyId !== storyId)
        return true
      }
    } catch (err) {
      console.error('Error deleting story:', err)
    }
  }

  // --- TASK ACTIONS ---
  async function fetchTasks(sprintId = null, assignedToId = null) {
    try {
      let params = []
      if (sprintId) params.push(`sprint_id=${sprintId}`)
      if (assignedToId) params.push(`assigned_to_id=${assignedToId}`)
      const query = params.length ? `?${params.join('&')}` : ''
      const res = await fetch(`${getApiBase()}/api/scrum/tasks${query}`)
      if (res.ok) {
        tasks.value = await res.json()
      }
    } catch (err) {
      console.error('Error fetching tasks:', err)
    }
  }

  async function createTask(taskData, userId = null) {
    try {
      const url = userId ? `${getApiBase()}/api/scrum/tasks?user_id=${userId}` : `${getApiBase()}/api/scrum/tasks`
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData)
      })
      if (res.ok) {
        const newTask = await res.json()
        tasks.value.unshift(newTask)
        return newTask
      }
    } catch (err) {
      console.error('Error creating task:', err)
    }
  }

  async function updateTaskStatus(taskId, status, userId = null) {
    try {
      const url = userId ? `${getApiBase()}/api/scrum/tasks/${taskId}/status?user_id=${userId}` : `${getApiBase()}/api/scrum/tasks/${taskId}/status`
      const res = await fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status })
      })
      if (res.ok) {
        const updated = await res.json()
        const idx = tasks.value.findIndex(t => t.id === taskId)
        if (idx !== -1) tasks.value[idx] = updated
        return updated
      }
    } catch (err) {
      console.error('Error updating task status:', err)
    }
  }

  async function submitTask(taskId, submissionNotes, submissionLink = '', userId = null) {
    try {
      const url = userId ? `${getApiBase()}/api/scrum/tasks/${taskId}/submit?user_id=${userId}` : `${getApiBase()}/api/scrum/tasks/${taskId}/submit`
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ submissionNotes, submissionLink })
      })
      if (res.ok) {
        const updated = await res.json()
        const idx = tasks.value.findIndex(t => t.id === taskId)
        if (idx !== -1) tasks.value[idx] = updated
        return updated
      }
    } catch (err) {
      console.error('Error submitting task:', err)
    }
  }

  async function reviewTask(taskId, decision, feedback, reviewerId) {
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/tasks/${taskId}/review?reviewer_id=${reviewerId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decision, feedback })
      })
      if (res.ok) {
        const updated = await res.json()
        const idx = tasks.value.findIndex(t => t.id === taskId)
        if (idx !== -1) tasks.value[idx] = updated
        return updated
      } else {
        const errData = await res.json().catch(() => ({}))
        throw new Error(errData.detail || 'Review action failed')
      }
    } catch (err) {
      console.error('Error reviewing task:', err)
      throw err
    }
  }

  // --- USER APPROVAL ACTIONS ---
  async function fetchPendingUsers() {
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/pending-users`)
      if (res.ok) {
        pendingUsers.value = await res.json()
      }
    } catch (err) {
      console.error('Error fetching pending users:', err)
    }
  }

  async function approveUser(userId, approveData = {}, reviewerId = null) {
    try {
      const url = reviewerId ? `${getApiBase()}/api/scrum/users/${userId}/approve?reviewer_id=${reviewerId}` : `${getApiBase()}/api/scrum/users/${userId}/approve`
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(approveData)
      })
      if (res.ok) {
        pendingUsers.value = pendingUsers.value.filter(u => u.id !== userId)
        return await res.json()
      }
    } catch (err) {
      console.error('Error approving user:', err)
    }
  }

  async function rejectUser(userId, reviewerId = null) {
    try {
      const url = reviewerId ? `${getApiBase()}/api/scrum/users/${userId}/reject?reviewer_id=${reviewerId}` : `${getApiBase()}/api/scrum/users/${userId}/reject`
      const res = await fetch(url, { method: 'POST' })
      if (res.ok) {
        pendingUsers.value = pendingUsers.value.filter(u => u.id !== userId)
        return await res.json()
      }
    } catch (err) {
      console.error('Error rejecting user:', err)
    }
  }

  // --- NOTIFICATIONS & AUDIT ---
  async function fetchNotifications(recipientId) {
    if (!recipientId) return
    try {
      const res = await fetch(`${getApiBase()}/api/scrum/notifications?recipient_id=${recipientId}`)
      if (res.ok) {
        notifications.value = await res.json()
      }
    } catch (err) {
      console.error('Error fetching notifications:', err)
    }
  }

  async function markNotificationRead(notifId) {
    try {
      await fetch(`${getApiBase()}/api/scrum/notifications/${notifId}/read`, { method: 'PUT' })
      const notif = notifications.value.find(n => n.id === notifId)
      if (notif) notif.isRead = true
    } catch (err) {
      console.error('Error marking notification read:', err)
    }
  }

  async function markAllNotificationsRead(recipientId) {
    try {
      await fetch(`${getApiBase()}/api/scrum/notifications/read-all?recipient_id=${recipientId}`, { method: 'PUT' })
      notifications.value.forEach(n => n.isRead = true)
    } catch (err) {
      console.error('Error marking all notifications read:', err)
    }
  }

  async function fetchAuditLogs(entityType = null) {
    try {
      const url = entityType ? `${getApiBase()}/api/scrum/audit-logs?entity_type=${entityType}` : `${getApiBase()}/api/scrum/audit-logs`
      const res = await fetch(url)
      if (res.ok) {
        auditLogs.value = await res.json()
      }
    } catch (err) {
      console.error('Error fetching audit logs:', err)
    }
  }

  return {
    sprints,
    activeSprint,
    stories,
    tasks,
    pendingUsers,
    notifications,
    auditLogs,
    loading,
    error,
    unreadNotificationCount,
    pendingApprovalsCount,
    fetchSprints,
    createSprint,
    updateSprint,
    rolloverSprint,
    fetchStories,
    createStory,
    updateStory,
    deleteStory,
    fetchTasks,
    createTask,
    updateTaskStatus,
    submitTask,
    reviewTask,
    fetchPendingUsers,
    approveUser,
    rejectUser,
    fetchNotifications,
    markNotificationRead,
    markAllNotificationsRead,
    fetchAuditLogs
  }
})
