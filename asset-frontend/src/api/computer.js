import request from './request'

export const getComputerList = (params) => request.get('/computers', { params })
export const searchComputer = (keywords, params) => request.get('/computers/search', { params: { keywords, ...params } })
export const addComputer = (data) => request.post('/computers/add', data)
export const updateComputer = (assetTag, data) => request.put(`/computers/update/${assetTag}`, data)
export const deleteComputer = (assetTag) => request.delete('/computers/del', { params: { asset_tag: assetTag } })