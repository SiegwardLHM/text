<template>
  <div class="defect-detection">
    <div class="page-title">
      <h1>胶囊模具缺陷检测系统</h1>
    </div>
    
    <div class="detection-container">
      <div class="panel-container">
        <!-- 左侧面板 - 相机控制和设置 -->
        <div class="left-panel">
          <div class="panel-title">相机控制</div>
          
          <div class="camera-controls">
            <div class="control-group">
              <div class="group-title">相机状态</div>
              <div class="status-indicator">
                <div class="indicator" :class="{ 'active': cameraConnected }"></div>
                <div class="status-text">{{ cameraConnected ? '已连接' : '未连接' }}</div>
              </div>
              <el-button 
                type="primary" 
                :disabled="cameraConnected" 
                @click="connectCamera">
                连接相机
              </el-button>
              <el-button 
                type="danger" 
                :disabled="!cameraConnected" 
                @click="disconnectCamera">
                断开连接
              </el-button>
            </div>
            
            <div class="control-group">
              <div class="group-title">相机参数</div>
              <div class="param-control">
                <div class="param-name">曝光时间</div>
                <el-slider 
                  v-model="cameraParams.exposure" 
                  :min="1" 
                  :max="100" 
                  :disabled="!cameraConnected"
                  @change="updateCameraParams">
                </el-slider>
                <div class="param-value">{{ cameraParams.exposure }}ms</div>
              </div>
              
              <div class="param-control">
                <div class="param-name">增益</div>
                <el-slider 
                  v-model="cameraParams.gain" 
                  :min="0" 
                  :max="24" 
                  :disabled="!cameraConnected"
                  @change="updateCameraParams">
                </el-slider>
                <div class="param-value">{{ cameraParams.gain }}dB</div>
              </div>
              
              <div class="param-control">
                <div class="param-name">对比度</div>
                <el-slider 
                  v-model="cameraParams.contrast" 
                  :min="0" 
                  :max="100" 
                  :disabled="!cameraConnected"
                  @change="updateCameraParams">
                </el-slider>
                <div class="param-value">{{ cameraParams.contrast }}%</div>
              </div>
            </div>
            
            <div class="control-group">
              <div class="group-title">采集控制</div>
              <el-button 
                type="success" 
                :disabled="!cameraConnected || isCapturing" 
                @click="startCapture">
                开始采集
              </el-button>
              <el-button 
                type="warning" 
                :disabled="!isCapturing" 
                @click="stopCapture">
                停止采集
              </el-button>
              <el-button 
                type="primary" 
                :disabled="!cameraConnected || isCapturing" 
                @click="singleCapture">
                单次采集
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 中间面板 - 图像显示区域 -->
        <div class="center-panel">
          <div class="panel-title">实时图像</div>
          
          <div class="image-display" ref="imageDisplay">
            <div v-if="!cameraConnected" class="no-camera">
              <i class="el-icon-video-camera-solid"></i>
              <div class="hint-text">请连接工业相机</div>
            </div>
            <div v-else-if="!isCapturing && !currentImage" class="no-capture">
              <i class="el-icon-picture"></i>
              <div class="hint-text">点击"开始采集"按钮查看实时图像</div>
            </div>
            <img v-else-if="currentImage" :src="currentImage" class="camera-image" alt="相机采集图像" />
            
            <!-- 检测到的缺陷标记覆盖层 -->
            <div class="detection-overlay" v-if="currentImage && detectionResult.processed">
              <div 
                v-for="(defect, index) in detectionResult.defects" 
                :key="index"
                class="defect-marker"
                :style="{
                  left: `${defect.x}px`,
                  top: `${defect.y}px`,
                  width: `${defect.width}px`,
                  height: `${defect.height}px`
                }">
              </div>
            </div>
          </div>
          
          <div class="capture-controls" v-if="currentImage">
            <el-button type="primary" size="small" @click="saveImage">
              <i class="el-icon-download"></i> 保存图像
            </el-button>
            <el-button type="success" size="small" @click="detectDefects">
              <i class="el-icon-search"></i> 检测缺陷
            </el-button>
            <el-button type="warning" size="small" @click="clearImage">
              <i class="el-icon-delete"></i> 清除图像
            </el-button>
          </div>
        </div>
        
        <!-- 右侧面板 - 检测结果和统计信息 -->
        <div class="right-panel">
          <div class="panel-title">检测结果</div>
          
          <div class="detection-results">
            <div class="result-status">
              <div class="status-title">检测状态</div>
              <div class="status-value" :class="{ 
                'success': detectionResult.processed && detectionResult.defects.length === 0,
                'error': detectionResult.processed && detectionResult.defects.length > 0,
                'neutral': !detectionResult.processed
              }">
                {{ getStatusText() }}
              </div>
            </div>
            
            <div class="result-summary">
              <div class="summary-item">
                <div class="item-label">检测时间</div>
                <div class="item-value">{{ detectionResult.timestamp || '-' }}</div>
              </div>
              <div class="summary-item">
                <div class="item-label">缺陷数量</div>
                <div class="item-value" :class="{ 'error': detectionResult.defects.length > 0 }">
                  {{ detectionResult.processed ? detectionResult.defects.length : '-' }}
                </div>
              </div>
              <div class="summary-item">
                <div class="item-label">处理耗时</div>
                <div class="item-value">
                  {{ detectionResult.processTime ? detectionResult.processTime + 'ms' : '-' }}
                </div>
              </div>
            </div>
            
            <div class="defect-list" v-if="detectionResult.defects.length > 0">
              <div class="list-title">缺陷列表</div>
              <div class="list-items">
                <div class="defect-item" v-for="(defect, index) in detectionResult.defects" :key="index">
                  <div class="defect-id">缺陷 #{{ index + 1 }}</div>
                  <div class="defect-info">
                    <div class="info-item">
                      <span class="label">位置:</span>
                      <span class="value">{{ `(${defect.x}, ${defect.y})` }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">尺寸:</span>
                      <span class="value">{{ `${defect.width}x${defect.height}px` }}</span>
                    </div>
                    <div class="info-item">
                      <span class="label">类型:</span>
                      <span class="value">{{ defect.type }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="detection-stats">
              <div class="stats-title">检测统计</div>
              <div class="stats-chart" ref="statsChart"></div>
              <div class="stats-summary">
                <div class="summary-row">
                  <div class="label">今日检测</div>
                  <div class="value">{{ stats.todayCount }}</div>
                </div>
                <div class="summary-row">
                  <div class="label">合格数量</div>
                  <div class="value success">{{ stats.passCount }}</div>
                </div>
                <div class="summary-row">
                  <div class="label">不合格数量</div>
                  <div class="value error">{{ stats.failCount }}</div>
                </div>
                <div class="summary-row">
                  <div class="label">合格率</div>
                  <div class="value">{{ stats.passRate }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DefectDetection',
  data() {
    return {
      // 相机状态
      cameraConnected: false,
      isCapturing: false,
      
      // 相机参数
      cameraParams: {
        exposure: 30,
        gain: 10,
        contrast: 50
      },
      
      // 当前图像
      currentImage: null,
      
      // 检测结果
      detectionResult: {
        processed: false,
        timestamp: null,
        processTime: null,
        defects: []
      },
      
      // 检测统计
      stats: {
        todayCount: 0,
        passCount: 0,
        failCount: 0,
        passRate: '0.0'
      },
      
      // 模拟数据 - 实际项目中应从后端API获取
      sampleImages: [
        '/sample-images/mold1.jpg',
        '/sample-images/mold2.jpg',
        '/sample-images/mold3_defect.jpg'
      ],
      captureInterval: null
    }
  },
  mounted() {
    // 初始化统计图表
    this.initStatsChart();
    
    // 在实际项目中这里应该初始化与工业相机的通信
  },
  beforeDestroy() {
    this.disconnectCamera();
  },
  methods: {
    // 相机控制方法
    connectCamera() {
      // 实际项目中应该建立与工业相机的连接
      // 这里使用模拟数据
      setTimeout(() => {
        this.cameraConnected = true;
        this.$message.success('相机连接成功');
      }, 1000);
    },
    
    disconnectCamera() {
      // 实际项目中应该断开与工业相机的连接
      this.stopCapture();
      this.cameraConnected = false;
      this.$message.info('相机已断开连接');
    },
    
    updateCameraParams() {
      // 实际项目中应该向相机发送参数更新
      this.$message.success('相机参数更新成功');
    },
    
    // 图像采集方法
    startCapture() {
      if (!this.cameraConnected) return;
      
      this.isCapturing = true;
      
      // 模拟实时图像流 - 实际项目中应该从相机获取流数据
      let imageIndex = 0;
      this.captureInterval = setInterval(() => {
        // 循环使用样本图像
        this.currentImage = this.sampleImages[imageIndex % this.sampleImages.length];
        imageIndex++;
        
        // 自动检测缺陷（可选）
        if (imageIndex % 5 === 0) {
          this.detectDefects();
        }
      }, 2000);
    },
    
    stopCapture() {
      clearInterval(this.captureInterval);
      this.isCapturing = false;
    },
    
    singleCapture() {
      if (!this.cameraConnected) return;
      
      // 模拟单次采集 - 随机使用一张样本图像
      const randomIndex = Math.floor(Math.random() * this.sampleImages.length);
      this.currentImage = this.sampleImages[randomIndex];
    },
    
    // 图像处理方法
    saveImage() {
      // 实际项目中应该保存图像到服务器或本地
      this.$message.success('图像已保存');
    },
    
    clearImage() {
      this.currentImage = null;
      this.detectionResult.processed = false;
      this.detectionResult.defects = [];
    },
    
    detectDefects() {
      if (!this.currentImage) return;
      
      // 模拟检测过程 - 实际项目中应使用计算机视觉算法
      const startTime = Date.now();
      
      // 随机模拟检测结果
      this.detectionResult.processed = true;
      this.detectionResult.timestamp = new Date().toLocaleString();
      
      // 如果使用了带"defect"标记的样本图像，则模拟检测到缺陷
      if (this.currentImage.includes('defect')) {
        this.detectionResult.defects = [
          {
            x: 120,
            y: 80,
            width: 30,
            height: 30,
            type: '胶囊缺失'
          },
          {
            x: 200,
            y: 150,
            width: 25,
            height: 25,
            type: '胶囊缺失'
          }
        ];
        this.stats.failCount++;
      } else {
        this.detectionResult.defects = [];
        this.stats.passCount++;
      }
      
      // 更新统计数据
      this.stats.todayCount++;
      this.stats.passRate = ((this.stats.passCount / this.stats.todayCount) * 100).toFixed(1);
      
      // 模拟处理时间
      setTimeout(() => {
        this.detectionResult.processTime = Date.now() - startTime;
        this.updateStatsChart();
        
        // 显示检测结果提示
        if (this.detectionResult.defects.length > 0) {
          this.$message.error(`检测到 ${this.detectionResult.defects.length} 处缺陷`);
        } else {
          this.$message.success('模具质量良好，未检测到缺陷');
        }
      }, 500);
    },
    
    // 辅助方法
    getStatusText() {
      if (!this.detectionResult.processed) {
        return '未检测';
      }
      return this.detectionResult.defects.length === 0 ? '合格' : '不合格';
    },
    
    // 图表相关方法
    initStatsChart() {
      // 在实际项目中应使用ECharts或其他图表库
      // 这里简单模拟图表初始化
      // 实际项目中应该在组件挂载后初始化图表
      console.log('图表已初始化');
    },
    
    updateStatsChart() {
      // 更新图表数据
      console.log('图表数据已更新');
    }
  }
}
</script>

<style scoped>
.defect-detection {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-title {
  margin-bottom: 20px;
  text-align: center;
}

.page-title h1 {
  color: #409EFF;
  font-size: 24px;
}

.detection-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(0, 20, 60, 0.5);
  border-radius: 8px;
  padding: 20px;
  overflow: hidden;
}

.panel-container {
  display: flex;
  height: 100%;
  gap: 20px;
}

/* 面板共用样式 */
.left-panel, .center-panel, .right-panel {
  background: rgba(0, 10, 30, 0.7);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.left-panel {
  width: 280px;
}

.center-panel {
  flex: 1;
}

.right-panel {
  width: 300px;
}

.panel-title {
  font-size: 18px;
  color: #409EFF;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 左侧面板 - 相机控制 */
.camera-controls {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.control-group {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 12px;
}

.group-title {
  font-size: 16px;
  color: #eee;
  margin-bottom: 12px;
}

.status-indicator {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #e74c3c;
  margin-right: 8px;
}

.indicator.active {
  background-color: #2ecc71;
  box-shadow: 0 0 8px rgba(46, 204, 113, 0.8);
}

.status-text {
  color: #eee;
}

.param-control {
  margin-bottom: 12px;
}

.param-name {
  color: #eee;
  margin-bottom: 4px;
}

.param-value {
  color: #409EFF;
  text-align: right;
  font-size: 14px;
}

/* 中间面板 - 图像显示 */
.image-display {
  flex: 1;
  background: #000;
  border-radius: 6px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  position: relative;
}

.no-camera, .no-capture {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.3);
}

.no-camera i, .no-capture i {
  font-size: 48px;
  margin-bottom: 12px;
}

.hint-text {
  font-size: 14px;
}

.camera-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.detection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.defect-marker {
  position: absolute;
  border: 2px solid #e74c3c;
  background-color: rgba(231, 76, 60, 0.3);
  border-radius: 4px;
  animation: pulse 1.5s infinite;
}

.capture-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 15px;
}

/* 右侧面板 - 检测结果 */
.detection-results {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-status {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 12px;
  text-align: center;
}

.status-title {
  color: #eee;
  margin-bottom: 10px;
}

.status-value {
  font-size: 24px;
  font-weight: bold;
}

.status-value.success {
  color: #2ecc71;
}

.status-value.error {
  color: #e74c3c;
}

.status-value.neutral {
  color: #bbb;
}

.result-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.summary-item {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 10px;
  flex: 1;
  min-width: 80px;
  text-align: center;
}

.item-label {
  color: #eee;
  font-size: 12px;
  margin-bottom: 6px;
}

.item-value {
  color: #409EFF;
  font-size: 18px;
  font-weight: bold;
}

.item-value.error {
  color: #e74c3c;
}

.defect-list {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 12px;
}

.list-title {
  color: #eee;
  margin-bottom: 10px;
}

.list-items {
  max-height: 150px;
  overflow-y: auto;
}

.defect-item {
  background: rgba(231, 76, 60, 0.1);
  border-left: 3px solid #e74c3c;
  border-radius: 0 4px 4px 0;
  padding: 8px;
  margin-bottom: 8px;
}

.defect-id {
  color: #e74c3c;
  font-weight: bold;
  margin-bottom: 6px;
}

.defect-info {
  font-size: 12px;
}

.info-item {
  display: flex;
  margin-bottom: 4px;
}

.info-item .label {
  color: #bbb;
  width: 50px;
}

.info-item .value {
  color: #eee;
  flex: 1;
}

.detection-stats {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  padding: 12px;
}

.stats-title {
  color: #eee;
  margin-bottom: 10px;
}

.stats-chart {
  height: 150px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  margin-bottom: 12px;
}

.stats-summary {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
}

.summary-row .label {
  color: #bbb;
}

.summary-row .value {
  color: #409EFF;
  font-weight: bold;
}

.summary-row .value.success {
  color: #2ecc71;
}

.summary-row .value.error {
  color: #e74c3c;
}

/* 动画 */
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(231, 76, 60, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(231, 76, 60, 0);
  }
}
</style> 