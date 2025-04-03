<template>
  <div class="production-page">
    <div class="page-header">
      <h2>胶囊模具生产线模拟</h2>
      <p class="description">实时监控生产线运行状态</p>
    </div>
    
    <!-- 引入生产线动画组件 -->
    <production-line />
    
    <div class="page-footer">
      <p>注：此模拟数据仅供参考，实际生产参数请以实际设备数据为准</p>
    </div>
  </div>
</template>

<script>
import ProductionLine from '@/components/ProductionLine.vue'

export default {
  name: 'Production',
  components: {
    ProductionLine
  }
}
</script>

<style scoped>
.production-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 10px;
}

.description {
  color: #606266;
  font-size: 14px;
}

.page-footer {
  text-align: center;
  margin-top: 20px;
  color: #909399;
  font-size: 12px;
}
</style> 