<template>
  <div class="video-monitor">
    <div class="content-container">
      <div class="video-grid">
        <div v-for="(item, index) in videoList" :key="index" class="video-item">
          <div class="video-frame">
            <img :src="item.imgSrc" class="video-image" />
            <div v-if="item.alert" class="alert-box">
              <span class="alert-text">{{ item.alertText }}</span>
            </div>
            <div class="video-time">{{ item.time }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VideoImage from '@/assets/video-frame.jpg'

export default {
  name: 'VideoMonitor',
  data() {
    return {
      videoList: Array(9).fill().map((_, index) => ({
        id: index + 1,
        imgSrc: VideoImage, // 假设所有图像都相同，实际使用时可以替换为不同的图片
        time: '2023-01-12 16:34:08',
        alert: true,
        alertText: 'fire: 0.39'
      }))
    }
  }
}
</script>

<style scoped>
.video-monitor {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #0a1a3b;
}

.content-container {
  flex: 1;
  padding: 10px;
  overflow: auto;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 10px;
  height: 100%;
}

.video-item {
  border: 1px solid rgba(25, 186, 255, 0.3);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.video-frame {
  width: 100%;
  height: 100%;
  position: relative;
}

.video-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.alert-box {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(255, 0, 0, 0.7);
  padding: 3px 8px;
  border-radius: 2px;
}

.alert-text {
  color: white;
  font-size: 12px;
}

.video-time {
  position: absolute;
  left: 10px;
  top: 10px;
  color: white;
  font-size: 12px;
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.5);
}
</style> 