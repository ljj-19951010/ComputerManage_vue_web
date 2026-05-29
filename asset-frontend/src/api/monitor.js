import request from './request'

export const getMonitorList = (params) => request.get('/monitors', { params })
export const searchMonitor = (keywords, params) => request.get('/monitors/search', { params: { keywords, ...params } })
export const addMonitor = (data) => request.post('/monitors/add', data)
export const updateMonitor = (assetTag, data) => request.put('/monitors/update', { asset_tag: assetTag, ...data })
export const deleteMonitor = (assetTag) => request.delete('/monitors/del', { params: { asset_tag: assetTag } })