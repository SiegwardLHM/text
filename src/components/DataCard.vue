<template>
  <div class="data-card">
    <div class="card-header">
      <span class="title">{{ title }}</span>
      <div class="header-right">
        <span class="update-time" v-if="updateTime">更新时间：{{ updateTime }}</span>
      </div>
    </div>
    <div class="card-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataCard',
  props: {
    title: {
      type: String,
      required: true
    },
    updateTime: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.data-card {
  width: 100%;
  height: 100%;
  border: 1px solid rgba(25, 186, 255, 0.3);
  border-radius: 4px;
  background-color: rgba(0, 10, 50, 0.3);
  box-shadow: 0 0 10px rgba(25, 186, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-header {
  height: 40px;
  line-height: 40px;
  padding: 0 15px;
  background: linear-gradient(to right, rgba(25, 186, 255, 0.3), transparent);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 16px;
  font-weight: bold;
  color: #fff;
}

.update-time {
  font-size: 12px;
  color: #7eb6ff;
}

.card-content {
  flex: 1;
  padding: 15px;
  overflow: auto;
}
</style> 