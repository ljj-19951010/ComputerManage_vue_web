<template>
  <div>
    <div class="header">
      <h2>员工管理</h2>
      <el-button type="primary" @click="handleAdd">新增员工</el-button>
    </div>
    
    <!-- 搜索栏 -->
    <el-input
      v-model="searchKeyword"
      placeholder="搜索姓名/邮箱"
      style="width: 300px; margin-right: 10px"
      clearable
      @keyup.enter="handleSearch"
    />
    <el-button type="primary" @click="handleSearch">搜索</el-button>
    
    <!-- 表格 -->
    <el-table :data="tableData" border stripe style="margin-top: 20px">
      <el-table-column prop="name" label="姓名" />
      <el-table-column prop="english_name" label="英文名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="department_name" label="部门" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status === 1 ? 'success' : 'danger'">
            {{ row.status === 1 ? '在职' : '离职' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页 -->
    <el-pagination
        v-model:current-page="pagination.page"
        :page-size="10"
        :total="pagination.total"
        layout="total, prev, pager, next, jumper"
        @current-change="loadData"
        style="margin-top: 20px"
    />
    
    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="formData" :rules="rules" ref="dialogFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="formData.name" />
        </el-form-item>
        <el-form-item label="英文名" prop="english_name">
          <el-input v-model="formData.english_name" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" />
        </el-form-item>
        <el-form-item label="部门" prop="department_id">
          <el-select v-model="formData.department_id" placeholder="请选择部门" clearable>
            <el-option label="技术部" :value="1" />
            <el-option label="销售部" :value="2" />
            <el-option label="人事部" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">在职</el-radio>
            <el-radio :label="0">离职</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getEmployeeList, searchEmployee, addEmployee, updateEmployee, deleteEmployee } from '@/api/employee'

const tableData = ref([])
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const dialogFormRef = ref()

const pagination = reactive({ page: 1, limit: 10, total: 0 })
const formData = reactive({ name: '', english_name: '', email: '', department_id: null, status: 1 })

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  english_name: [{ required: true, message: '请输入英文名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }]
}

const loadData = async () => {
  const params = { skip: (pagination.page - 1) * pagination.limit, limit: pagination.limit }
  const res = searchKeyword.value 
    ? await searchEmployee(searchKeyword.value, params)
    : await getEmployeeList(params)
  tableData.value = res.data
  pagination.total = res.total
}

const handleSearch = () => { pagination.page = 1; loadData() }
const handleAdd = () => { isEdit.value = false; dialogTitle.value = '新增员工'; Object.keys(formData).forEach(k => formData[k] = null); formData.status = 1; dialogVisible.value = true }
const handleEdit = (row) => { isEdit.value = true; dialogTitle.value = '编辑员工'; Object.assign(formData, row); dialogVisible.value = true }
const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该员工吗？').then(async () => {
    await deleteEmployee(row.name)
    ElMessage.success('删除成功')
    loadData()
  })
}
const handleSubmit = async () => {
  await dialogFormRef.value.validate()
  if (isEdit.value) await updateEmployee(formData.name, formData)
  else await addEmployee(formData)
  ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>