<template>
  <div>
    <h2>仪表盘</h2>
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <span>员工总数</span>
              <el-icon><User /></el-icon>
            </div>
          </template>
          <div style="font-size: 28px; text-align: center">{{ stats.employeeCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <span>电脑总数</span>
              <el-icon><Monitor /></el-icon>
            </div>
          </template>
          <div style="font-size: 28px; text-align: center">{{ stats.computerCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <span>显示器总数</span>
              <el-icon><Cpu /></el-icon>
            </div>
          </template>
          <div style="font-size: 28px; text-align: center">{{ stats.monitorCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <template #header>
            <div style="display: flex; justify-content: space-between">
              <span>部门总数</span>
              <el-icon><OfficeBuilding /></el-icon>
            </div>
          </template>
          <div style="font-size: 28px; text-align: center">{{ stats.departmentCount }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, Monitor, Cpu, OfficeBuilding } from '@element-plus/icons-vue'
import { getEmployeeList } from '@/api/employee'
import { getComputerList } from '@/api/computer'
import { getMonitorList } from '@/api/monitor'

const stats = ref({
  employeeCount: 0,
  computerCount: 0,
  monitorCount: 0,
  departmentCount: 0
})

const loadStats = async () => {
  try {
    const [employees, computers, monitors] = await Promise.all([
      getEmployeeList({ skip: 0, limit: 1 }),
      getComputerList({ skip: 0, limit: 1 }),
      getMonitorList({ skip: 0, limit: 1 })
    ])
    stats.value.employeeCount = employees.total
    stats.value.computerCount = computers.total
    stats.value.monitorCount = monitors.total
    stats.value.departmentCount = 3 // 暂时写死
  } catch (error) {
    console.error('加载统计数据失败', error)
  }
}

onMounted(loadStats)
</script>