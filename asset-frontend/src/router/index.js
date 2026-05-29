import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
      { path: 'employees', name: 'Employees', component: () => import('@/views/EmployeeList.vue') },
      { path: 'computers', name: 'Computers', component: () => import('@/views/ComputerList.vue') },
      { path: 'monitors', name: 'Monitors', component: () => import('@/views/MonitorList.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isLoggedIn()) {
    return '/login'   // 直接返回路径
  }
  return true   // 允许导航
})

export default router