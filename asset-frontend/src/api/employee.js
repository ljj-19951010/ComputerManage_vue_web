import request from './request'

// 获取员工列表（分页）
export const getEmployeeList = (params) => request.get('/employee/', { params })

// 搜索员工
export const searchEmployee = (keyword, params) => 
  request.get('/employee/search', { params: { keyword, ...params } })

// 添加员工
export const addEmployee = (data) => request.post('/employee/add', data)

// 更新员工
export const updateEmployee = (name, data) => request.put(`/employee/${name}`, data)

// 删除员工
export const deleteEmployee = (name) => request.delete(`/employee/${name}`)