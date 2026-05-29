<template>
  <div>
    <div class="header" style="display: flex; justify-content: space-between; margin-bottom: 20px">
      <h2>电脑管理</h2>
      <el-button type="primary" @click="handleAdd">新增电脑</el-button>
    </div>

    <el-table :data="tableData" border stripe>
      <el-table-column prop="asset_tag" label="资产编号" />
      <el-table-column prop="serial_number" label="序列号" />
      <el-table-column prop="model_id" label="型号ID" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status === 'available' ? 'success' : 'danger'">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="employee_name" label="使用人" />
      <el-table-column prop="price" label="价格" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

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
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="资产编号" prop="asset_tag">
          <el-input v-model="formData.asset_tag" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="序列号" prop="serial_number">
          <el-input v-model="formData.serial_number" />
        </el-form-item>
        <el-form-item label="型号ID" prop="model_id">
          <el-input-number v-model="formData.model_id" :min="1" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status">
            <el-option label="可用" value="available" />
            <el-option label="使用中" value="in_use" />
            <el-option label="维修" value="repair" />
            <el-option label="退役" value="retired" />
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model="formData.price" />
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="formData.remark" type="textarea" />
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
import { getComputerList, addComputer, updateComputer, deleteComputer } from '@/api/computer'

const tableData = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const formRef = ref()

const pagination = reactive({ page: 1, limit: 10, total: 0 })
const formData = reactive({
  asset_tag: '',
  serial_number: '',
  model_id: null,
  status: 'available',
  price: '',
  remark: ''
})

const rules = {
  asset_tag: [{ required: true, message: '资产编号不能为空', trigger: 'blur' }],
  serial_number: [{ required: true, message: '序列号不能为空', trigger: 'blur' }],
  model_id: [{ required: true, message: '型号ID不能为空', trigger: 'blur' }]
}

const loadData = async () => {
  const params = { skip: (pagination.page - 1) * pagination.limit, limit: pagination.limit }
  const res = await getComputerList(params)
  tableData.value = res.data
  pagination.total = res.total
}

const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增电脑'
  Object.assign(formData, { asset_tag: '', serial_number: '', model_id: null, status: 'available', price: '', remark: '' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑电脑'
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该电脑吗？').then(async () => {
    await deleteComputer(row.asset_tag)
    ElMessage.success('删除成功')
    loadData()
  })
}

const handleSubmit = async () => {
  await formRef.value.validate()
  if (isEdit.value) {
    await updateComputer(formData.asset_tag, formData)
    ElMessage.success('更新成功')
  } else {
    await addComputer(formData)
    ElMessage.success('添加成功')
  }
  dialogVisible.value = false
  loadData()
}

onMounted(loadData)
</script>