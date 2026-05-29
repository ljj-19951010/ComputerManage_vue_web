import request from './request'

// 登录
export const login = (data) => request.post('/admin/login', data)

// 获取当前用户信息
export const getCurrentAdmin = () => request.get('/admin/me')

// 获取管理员列表
export const getAdminList = (params) => request.get('/admin', { params })

// 更新管理员
export const updateAdmin = (username, data) => request.put(`/admin/${username}`, data)

// 删除管理员
export const deleteAdmin = (username) => request.delete(`/admin/${username}`)