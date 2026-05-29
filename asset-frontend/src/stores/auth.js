import { defineStore } from 'pinia'
import { login } from '@/api/admin'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    username: localStorage.getItem('username') || ''
  }),
  
  actions: {
    async login(username, password) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      const res = await login(formData)
      this.token = res.access_token
      this.username = username
      
      localStorage.setItem('access_token', res.access_token)
      localStorage.setItem('username', username)
      return res
    },
    
    logout() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('username')
    },
    
    isLoggedIn() {
      return !!this.token
    }
  }
})