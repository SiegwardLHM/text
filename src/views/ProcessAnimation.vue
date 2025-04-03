<template>
  <div class="process-animation">
    <div class="animation-container">
      <ProductionLine3D
        ref="productionLine3D"
        @animation-complete="handleAnimationComplete"
        @device-status-change="handleDeviceStatusChange"
      />
    </div>
    
    <div class="control-panel">
      <h2>胶衣成型生产线模拟</h2>
      
      <div class="controls">
        <button class="start-btn" @click="startAnimation" :disabled="isAnimating">
          开始流程
        </button>
        <button class="reset-btn" @click="resetAnimation" :disabled="isAnimating && !isComplete">
          重置
        </button>
        
        <div class="speed-control">
          <label>动画速度:</label>
          <div class="slider-container">
            <input type="range" min="0.1" max="2" step="0.1" v-model="animationSpeed">
            <span>{{animationSpeed.toFixed(1)}}x</span>
          </div>
        </div>
      </div>
      
      <div class="process-steps">
        <h3>工艺流程</h3>
        <div class="step-indicator">
          <div class="step" :class="{ active: currentStep >= 1, done: currentStep > 1 }">
            <div class="step-number">1</div>
            <div class="step-name">
              溶胶准备
              <div class="step-time" v-if="currentStep === 1">
                {{ stepTimer > 0 ? formatTime(stepTimer) : '' }}
              </div>
            </div>
          </div>
          <div class="step-connector"></div>
          <div class="step" :class="{ active: currentStep >= 2, done: currentStep > 2 }">
            <div class="step-number">2</div>
            <div class="step-name">
              蘸胶过程
              <div class="step-time" v-if="currentStep === 2">
                {{ stepTimer > 0 ? formatTime(stepTimer) : '' }}
              </div>
            </div>
          </div>
          <div class="step-connector"></div>
          <div class="step" :class="{ active: currentStep >= 3, done: currentStep > 3 }">
            <div class="step-number">3</div>
            <div class="step-name">
              干燥固化
              <div class="step-time" v-if="currentStep === 3">
                {{ stepTimer > 0 ? formatTime(stepTimer) : '' }}
              </div>
            </div>
          </div>
          <div class="step-connector"></div>
          <div class="step" :class="{ active: currentStep >= 4, done: currentStep > 4 }">
            <div class="step-number">4</div>
            <div class="step-name">
              质量检测
              <div class="step-time" v-if="currentStep === 4">
                {{ stepTimer > 0 ? formatTime(stepTimer) : '' }}
              </div>
            </div>
          </div>
          <div class="step-connector"></div>
          <div class="step" :class="{ active: currentStep >= 5, done: false }">
            <div class="step-number">5</div>
            <div class="step-name">
              完成
            </div>
          </div>
        </div>
      </div>
          </div>
          
    <!-- 数字孪生监控面板 -->
    <div class="digital-twin-dashboard" v-if="showDashboard">
      <div class="dashboard-header">
        <h3>数字孪生监控</h3>
        <div class="dashboard-controls">
          <button class="minimize-btn" @click="toggleDashboard">
            {{ showDashboard ? '隐藏' : '显示' }}
          </button>
        </div>
          </div>
          
      <div class="charts-container">
        <div class="chart-box temperature-chart">
          <h4>温度监控 (°C)</h4>
          <div ref="temperatureChart" class="chart"></div>
        </div>
        
        <div class="chart-box quality-chart">
          <h4>质量监控 (%)</h4>
          <div ref="qualityChart" class="chart"></div>
            </div>
          </div>
          
      <div class="alerts-section">
        <div class="alerts-header">
          <h4>生产警报</h4>
          <div class="alert-count" v-if="alerts.length > 0">{{ alerts.length }}</div>
          <div class="no-alerts" v-else>无警报</div>
        </div>
        
        <div class="alert-list">
          <div v-for="(alert, index) in alerts" :key="index" class="alert-item" :class="alert.level">
            <div class="alert-icon"></div>
            <div class="alert-content">
              <div class="alert-title">{{ alert.title }}</div>
              <div class="alert-message">{{ alert.message }}</div>
              <div class="alert-time">{{ alert.time }}</div>
            </div>
            <button class="dismiss-btn" @click="dismissAlert(index)">×</button>
          </div>
            </div>
          </div>
          
      <div class="production-stats">
        <h4>生产统计</h4>
        <div class="stats-grid">
          <div class="stats-item">
            <div class="stats-label">良品率</div>
            <div class="stats-value">{{ qualityRate.toFixed(1) }}%</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">生产批次</div>
            <div class="stats-value">{{ batchCount }}</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">平均温度</div>
            <div class="stats-value">{{ averageTemperature.toFixed(1) }}°C</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">平均周期</div>
            <div class="stats-value">{{ averageCycleTime.toFixed(1) }}分钟</div>
          </div>
        </div>
          </div>
          
      <div class="parameter-monitor">
        <h4>实时参数</h4>
        <div class="param-grid">
          <div class="param-item" :class="{ 'param-alert': temperature > thresholds.temperature.high || temperature < thresholds.temperature.low }">
            <div class="param-label">温度</div>
            <div class="param-value">{{ temperature.toFixed(1) }}°C</div>
          </div>
          <div class="param-item" :class="{ 'param-alert': pressure > thresholds.pressure.high || pressure < thresholds.pressure.low }">
            <div class="param-label">压力</div>
            <div class="param-value">{{ pressure.toFixed(1) }}MPa</div>
          </div>
          <div class="param-item" :class="{ 'param-alert': viscosity > thresholds.viscosity.high || viscosity < thresholds.viscosity.low }">
            <div class="param-label">粘度</div>
            <div class="param-value">{{ viscosity.toFixed(0) }}mPa·s</div>
          </div>
          <div class="param-item">
            <div class="param-label">循环时间</div>
            <div class="param-value">{{ cycleTime.toFixed(1) }}分钟</div>
          </div>
        </div>
      </div>
          </div>
          
    <!-- 添加面板控制按钮 -->
    <div class="dashboard-toggle" v-if="!showDashboard" @click="toggleDashboard">
      显示监控面板
          </div>
          
    <!-- 警报设置对话框 -->
    <div class="alert-settings-dialog" v-show="showAlertSettings">
      <div class="dialog-header">
        <h3>警报阈值设置</h3>
        <button class="close-btn" @click="showAlertSettings = false">×</button>
      </div>
      <div class="dialog-content">
        <div class="threshold-item">
          <label>温度警报范围 (°C)</label>
          <div class="threshold-inputs">
            <input type="number" v-model="tempSettings.low" placeholder="最小值">
            <span>-</span>
            <input type="number" v-model="tempSettings.high" placeholder="最大值">
        </div>
      </div>
      
        <div class="threshold-item">
          <label>压力警报范围 (MPa)</label>
          <div class="threshold-inputs">
            <input type="number" v-model="pressureSettings.low" placeholder="最小值">
            <span>-</span>
            <input type="number" v-model="pressureSettings.high" placeholder="最大值">
        </div>
        </div>
        
        <div class="threshold-item">
          <label>粘度警报范围 (mPa·s)</label>
          <div class="threshold-inputs">
            <input type="number" v-model="viscositySettings.low" placeholder="最小值">
            <span>-</span>
            <input type="number" v-model="viscositySettings.high" placeholder="最大值">
        </div>
        </div>
        
        <div class="threshold-item">
          <label>良品率警报阈值 (%)</label>
          <div class="threshold-inputs">
            <input type="number" v-model="qualitySettings.low" placeholder="最小值">
        </div>
        </div>
      </div>
      <div class="dialog-footer">
        <button class="save-btn" @click="saveAlertSettings">保存设置</button>
        <button class="reset-btn" @click="resetAlertSettings">重置默认</button>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import ProductionLine3D from '../components/ProductionLine3D.vue';

export default {
  name: 'ProcessAnimation',
  components: {
    ProductionLine3D
  },
  data() {
    return {
      currentStep: 0,
      stepTimer: 0,
      isAnimating: false,
      isComplete: false,
      waitingForAnimation: false,
      animationSpeed: 1,
      timerInterval: null,
      stepTimings: {
        1: 15, // 溶胶准备 (秒)
        2: 20, // 蘸胶过程 (秒)
        3: 30, // 干燥固化 (秒)
        4: 10  // 质量检测 (秒)
      },
      
      // 数字孪生数据
      charts: {
        temperature: null,
        quality: null
      },
      temperatureData: [],
      qualityData: [],
      pressureData: [],
      timeData: [],
      temperature: 75.0,
      pressure: 1.2,
      viscosity: 200,
      cycleTime: 12.5,
      qualityRate: 97.5,
      alerts: [],
      batchCount: 0,
      averageTemperature: 75.0,
      averageCycleTime: 12.5,
      thresholds: {
        temperature: { low: 65, high: 85 },
        pressure: { low: 0.8, high: 1.5 },
        viscosity: { low: 180, high: 220 },
        quality: { low: 95 }
      },
      tempSettings: { low: 65, high: 85 },
      pressureSettings: { low: 0.8, high: 1.5 },
      viscositySettings: { low: 180, high: 220 },
      qualitySettings: { low: 95 },
      showAlertSettings: false,
      dataCollectionInterval: null,
      processParameters: {
        temperature: 75.0,
        pressure: 1.2,
        viscosity: 200
      },
      showDashboard: true
    };
  },
  mounted() {
    this.initCharts();
    window.addEventListener('resize', this.onResize);
  },
  beforeDestroy() {
    this.stopDataCollection();
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
    window.removeEventListener('resize', this.onResize);
    
    // 销毁图表以防内存泄漏
    Object.keys(this.charts).forEach(chart => {
      if (this.charts[chart]) {
        this.charts[chart].dispose();
      }
    });
  },
  methods: {
    startAnimation() {
      this.isAnimating = true;
      this.isComplete = false;
      this.currentStep = 1;
      this.batchCount++;
      this.startRealTimeDataCollection();
      this.startStepTimer();
      
      // 调用3D组件的动画方法
      if (this.$refs.productionLine3D) {
        try {
          console.log('重置3D组件动画');
          // 检查方法是否存在
          if (typeof this.$refs.productionLine3D.resetAnimation === 'function') {
            this.$refs.productionLine3D.resetAnimation();
          } else {
            console.warn('ProductionLine3D组件中没有resetAnimation方法');
          }
        } catch (error) {
          console.error('调用resetAnimation方法时出错:', error);
        }
      } else {
        console.warn('找不到productionLine3D引用');
      }
    },
    
    resetAnimation() {
      this.isAnimating = false;
      this.isComplete = false;
      this.currentStep = 0;
      this.stopStepTimer();
      this.stopDataCollection();
      
      // 重置3D组件的动画
      if (this.$refs.productionLine3D) {
        try {
          // 检查方法是否存在
          if (typeof this.$refs.productionLine3D.resetAnimation === 'function') {
            this.$refs.productionLine3D.resetAnimation();
          } else {
            console.warn('ProductionLine3D组件中没有resetAnimation方法');
          }
        } catch (error) {
          console.error('调用resetAnimation方法时出错:', error);
        }
      }
    },
    
    startStepTimer() {
      this.stopStepTimer();
      
      const stepTime = this.stepTimings[this.currentStep];
      if (!stepTime) return;
      
      this.stepTimer = stepTime;
      
      this.timerInterval = setInterval(() => {
        this.stepTimer -= 0.1;
        
        if (this.stepTimer <= 0) {
          this.stopStepTimer();
          
          // 处理步骤完成
          if (this.currentStep < 4) {
            // 自动进入下一步
            this.advanceStep();
          } else {
            // 等待动画完成事件
            this.waitingForAnimation = true;
          }
        }
      }, 100 / this.animationSpeed);
    },
    
    stopStepTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    },
    
    advanceStep() {
      if (this.currentStep < 5) {
        this.currentStep++;
        
        if (this.currentStep <= 4) {
          this.startStepTimer();
        } else {
          this.completeProcess();
        }
      }
    },
    
    completeProcess() {
        this.isAnimating = false;
      this.isComplete = true;
      this.stopDataCollection();
      
      // 生成生产报告
      this.generateProductionReport();
    },
    
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs.toString().padStart(2, '0')}`;
    },
    
    // 数字孪生监控相关方法
    initCharts() {
      // 初始化温度图表
      this.charts.temperature = echarts.init(this.$refs.temperatureChart);
      const temperatureOption = {
        grid: { top: 10, right: 10, bottom: 20, left: 40 },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: { fontSize: 10 }
        },
        yAxis: {
          type: 'value',
          min: 50,
          max: 100,
          axisLabel: { fontSize: 10 }
        },
        series: [{
          type: 'line',
          data: [],
          smooth: true,
          symbol: 'none',
          lineStyle: { width: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(80, 141, 255, 0.5)' },
              { offset: 1, color: 'rgba(80, 141, 255, 0.1)' }
            ])
          },
          markLine: {
            silent: true,
            lineStyle: { color: '#ff4d4f', type: 'dashed', width: 1 },
            data: [
              { yAxis: 85, name: '上限' },
              { yAxis: 65, name: '下限' }
            ],
            label: { fontSize: 10 }
          }
        }]
      };
      this.charts.temperature.setOption(temperatureOption);
      
      // 初始化质量图表
      this.charts.quality = echarts.init(this.$refs.qualityChart);
      const qualityOption = {
        grid: { top: 10, right: 10, bottom: 20, left: 40 },
        xAxis: {
          type: 'category',
          data: [],
          axisLabel: { fontSize: 10 }
        },
        yAxis: {
          type: 'value',
          min: 80,
          max: 100,
          axisLabel: { fontSize: 10 }
        },
        series: [{
          type: 'line',
          data: [],
          smooth: true,
          symbol: 'none',
          lineStyle: { width: 2 },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(82, 196, 26, 0.5)' },
              { offset: 1, color: 'rgba(82, 196, 26, 0.1)' }
            ])
          },
          markLine: {
            silent: true,
            lineStyle: { color: '#ff4d4f', type: 'dashed', width: 1 },
            data: [{ yAxis: 95, name: '最低标准' }],
            label: { fontSize: 10 }
          }
        }]
      };
      this.charts.quality.setOption(qualityOption);
    },
    
    startRealTimeDataCollection() {
      this.stopDataCollection();
      
      // 初始化数据数组
      this.timeData = [];
      this.temperatureData = [];
      this.qualityData = [];
      this.pressureData = [];
      
      // 设置初始值
      this.processParameters = {
        temperature: 75.0,
        pressure: 1.2,
        viscosity: 200
      };
      
      // 模拟数据点收集
      this.dataCollectionInterval = setInterval(() => {
        const now = new Date();
        const timeStr = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
        
        // 模拟参数变化
        // 根据当前步骤设置不同的参数波动范围
        let tempVariation = 0.5;
        let pressureVariation = 0.05;
        let viscosityVariation = 5;
        
        switch(this.currentStep) {
          case 1: // 溶胶准备
            tempVariation = 1.0;
            pressureVariation = 0.1;
            viscosityVariation = 10;
            break;
          case 2: // 蘸胶过程
            tempVariation = 0.5;
            pressureVariation = 0.15;
            viscosityVariation = 15;
            break;
          case 3: // 干燥固化
            tempVariation = 1.5;
            pressureVariation = 0.05;
            viscosityVariation = 3;
            break;
          case 4: // 质量检测
            tempVariation = 0.3;
            pressureVariation = 0.02;
            viscosityVariation = 2;
            break;
        }
        
        // 更新参数值
        this.temperature = this.processParameters.temperature + (Math.random() * 2 - 1) * tempVariation;
        this.pressure = this.processParameters.pressure + (Math.random() * 2 - 1) * pressureVariation;
        this.viscosity = this.processParameters.viscosity + (Math.random() * 2 - 1) * viscosityVariation;
        
        // 计算质量率，基于参数偏差
        const tempFactor = Math.max(0, 1 - Math.abs(this.temperature - 75) / 20);
        const pressureFactor = Math.max(0, 1 - Math.abs(this.pressure - 1.2) / 0.8);
        const viscosityFactor = Math.max(0, 1 - Math.abs(this.viscosity - 200) / 50);
        this.qualityRate = 85 + 15 * (tempFactor * 0.4 + pressureFactor * 0.3 + viscosityFactor * 0.3);
        
        // 存储数据
        this.timeData.push(timeStr);
        this.temperatureData.push(this.temperature);
        this.qualityData.push(this.qualityRate);
        this.pressureData.push(this.pressure);
        
        // 限制数据点数量
        if (this.timeData.length > 20) {
          this.timeData.shift();
          this.temperatureData.shift();
          this.qualityData.shift();
          this.pressureData.shift();
        }
        
        // 更新图表
        this.updateCharts();
        
        // 检查警报阈值
        this.checkAlerts();
        
        // 记录参数变化
        this.logParameterChange();
        }, 1000);
    },
    
    stopDataCollection() {
      if (this.dataCollectionInterval) {
        clearInterval(this.dataCollectionInterval);
        this.dataCollectionInterval = null;
      }
    },
    
    updateCharts() {
      if (this.charts.temperature) {
        this.charts.temperature.setOption({
          xAxis: { data: this.timeData },
          series: [{ data: this.temperatureData }]
        });
      }
      
      if (this.charts.quality) {
        this.charts.quality.setOption({
          xAxis: { data: this.timeData },
          series: [{ data: this.qualityData }]
        });
      }
    },
    
    checkAlerts() {
      const now = new Date();
      const timeStr = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      
      // 检查温度警报
      if (this.temperature > this.thresholds.temperature.high) {
        this.addAlert('警告', `温度过高: ${this.temperature.toFixed(1)}°C`, 'warning', timeStr);
      } else if (this.temperature < this.thresholds.temperature.low) {
        this.addAlert('警告', `温度过低: ${this.temperature.toFixed(1)}°C`, 'warning', timeStr);
      }
      
      // 检查压力警报
      if (this.pressure > this.thresholds.pressure.high) {
        this.addAlert('警告', `压力过高: ${this.pressure.toFixed(1)}MPa`, 'warning', timeStr);
      } else if (this.pressure < this.thresholds.pressure.low) {
        this.addAlert('警告', `压力过低: ${this.pressure.toFixed(1)}MPa`, 'warning', timeStr);
      }
      
      // 检查质量率警报
      if (this.qualityRate < this.thresholds.quality.low) {
        this.addAlert('严重', `良品率低于标准: ${this.qualityRate.toFixed(1)}%`, 'critical', timeStr);
      }
    },
    
    addAlert(title, message, level, time) {
      // 检查是否已有相同的警报
      const hasSimilarAlert = this.alerts.some(alert => 
        alert.title === title && 
        alert.message === message && 
        Date.now() - new Date(alert.timestamp).getTime() < 60000
      );
      
      if (!hasSimilarAlert) {
        this.alerts.unshift({
          title,
          message,
          level,
          time,
          timestamp: new Date()
        });
        
        // 限制警报数量
        if (this.alerts.length > 10) {
          this.alerts.pop();
        }
        
        // 播放警报声音
        this.playAlertSound(level);
      }
    },
    
    dismissAlert(index) {
      this.alerts.splice(index, 1);
    },
    
    playAlertSound(level) {
      // 实际应用中可以播放不同级别的警报声音
      console.log(`播放${level}级别警报声音`);
    },
    
    generateProductionReport() {
      // 计算生产过程的统计数据
      this.averageTemperature = this.temperatureData.reduce((a, b) => a + b, 0) / this.temperatureData.length;
      this.averageCycleTime = (this.stepTimings[1] + this.stepTimings[2] + this.stepTimings[3] + this.stepTimings[4]) / 60;
      
      // 生成生产报告
      console.log('生产报告生成完成');
      
      // 添加报告通知
      const now = new Date();
      const timeStr = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      this.addAlert('信息', `批次 #${this.batchCount} 生产完成，良品率: ${this.qualityRate.toFixed(1)}%`, 'info', timeStr);
    },
    
    toggleAlertSettings() {
      this.showAlertSettings = !this.showAlertSettings;
      
      if (this.showAlertSettings) {
        // 初始化设置值
        this.tempSettings.low = this.thresholds.temperature.low;
        this.tempSettings.high = this.thresholds.temperature.high;
        this.pressureSettings.low = this.thresholds.pressure.low;
        this.pressureSettings.high = this.thresholds.pressure.high;
        this.viscositySettings.low = this.thresholds.viscosity.low;
        this.viscositySettings.high = this.thresholds.viscosity.high;
        this.qualitySettings.low = this.thresholds.quality.low;
      }
    },
    
    saveAlertSettings() {
      // 保存设置
      this.thresholds.temperature.low = parseFloat(this.tempSettings.low);
      this.thresholds.temperature.high = parseFloat(this.tempSettings.high);
      this.thresholds.pressure.low = parseFloat(this.pressureSettings.low);
      this.thresholds.pressure.high = parseFloat(this.pressureSettings.high);
      this.thresholds.viscosity.low = parseFloat(this.viscositySettings.low);
      this.thresholds.viscosity.high = parseFloat(this.viscositySettings.high);
      this.thresholds.quality.low = parseFloat(this.qualitySettings.low);
      
      // 更新图表标记线
      if (this.charts.temperature) {
        this.charts.temperature.setOption({
          series: [{
            markLine: {
              data: [
                { yAxis: this.thresholds.temperature.high, name: '上限' },
                { yAxis: this.thresholds.temperature.low, name: '下限' }
              ]
            }
          }]
        });
      }
      
      if (this.charts.quality) {
        this.charts.quality.setOption({
          series: [{
            markLine: {
              data: [{ yAxis: this.thresholds.quality.low, name: '最低标准' }]
            }
          }]
        });
      }
      
      this.showAlertSettings = false;
    },
    
    resetAlertSettings() {
      // 重置为默认值
      this.tempSettings.low = 65;
      this.tempSettings.high = 85;
      this.pressureSettings.low = 0.8;
      this.pressureSettings.high = 1.5;
      this.viscositySettings.low = 180;
      this.viscositySettings.high = 220;
      this.qualitySettings.low = 95;
    },
    
    onResize() {
      // 调整图表大小
      Object.keys(this.charts).forEach(key => {
        if (this.charts[key]) {
          this.charts[key].resize();
        }
      });
    },
    
    logParameterChange() {
      // 记录参数变化日志
      if (this.processParameters) {
        const tempChange = this.temperature !== undefined ? this.temperature.toFixed(1) : 'N/A';
        const pressureChange = this.pressure !== undefined ? this.pressure.toFixed(1) : 'N/A';
        const viscosityChange = this.viscosity !== undefined ? this.viscosity.toFixed(0) : 'N/A';
        
        console.log(`参数变化 - 温度: ${tempChange}°C, 压力: ${pressureChange}MPa, 粘度: ${viscosityChange}mPa·s`);
      }
    },

    // 处理3D动画完成事件
    handleAnimationComplete(data) {
      console.log('收到动画完成事件:', data);
      
      if (this.waitingForAnimation && this.currentStep === 4) {
        this.waitingForAnimation = false;
        
        // 获取动画传递的数据
        if (data && data.processData) {
          this.processParameters = data.processData;
        }
        
        // 进入完成步骤
        this.advanceStep();
      }
    },
    
    // 处理设备状态变化事件
    handleDeviceStatusChange(status) {
      console.log('设备状态变化:', status);
      
      // 根据设备状态添加警报
      const now = new Date();
      const timeStr = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
      
      if (status === '异常') {
        this.addAlert('严重', '设备状态异常，请检查设备', 'critical', timeStr);
      } else if (status === '注意') {
        this.addAlert('警告', '设备状态需要注意，请关注参数变化', 'warning', timeStr);
      }
    },
    
    // 添加面板切换方法
    toggleDashboard() {
      this.showDashboard = !this.showDashboard;
    }
  }
};
</script>

<style scoped>
.process-animation {
  display: flex;
  flex-wrap: wrap;
  height: 100%;
  position: relative;
  overflow: hidden;
  background-color: #141e30;
  color: #fff;
}

.animation-container {
  flex: 1;
  min-width: 300px;
  height: 100%;
  position: relative;
}

.control-panel {
  width: 300px;
  height: 100%;
  background: rgba(22, 34, 51, 0.8);
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  border-left: 1px solid rgba(24, 144, 255, 0.2);
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #1890ff;
  text-align: center;
}

h3 {
  margin-top: 5px;
  margin-bottom: 10px;
  font-size: 16px;
  color: #1890ff;
}

.controls {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.start-btn {
  background-color: #52c41a;
  color: white;
}

.start-btn:hover {
  background-color: #73d13d;
}

.start-btn:disabled {
  background-color: #91d361;
  cursor: not-allowed;
}

.reset-btn {
  background-color: #ff4d4f;
  color: white;
}

.reset-btn:hover {
  background-color: #ff7875;
}

.reset-btn:disabled {
  background-color: #ffa39e;
  cursor: not-allowed;
}

.speed-control {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-top: 10px;
}

.speed-control label {
  font-size: 14px;
  color: #d9d9d9;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.slider-container input[type="range"] {
  flex: 1;
}

.slider-container span {
  width: 40px;
  text-align: right;
  font-size: 14px;
}

.process-steps {
  flex: 1;
  margin-top: 20px;
}

.step-indicator {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.step {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.2);
  transition: all 0.3s;
}

.step.active {
  background: rgba(24, 144, 255, 0.2);
  border-left: 3px solid #1890ff;
}

.step.done {
  background: rgba(82, 196, 26, 0.2);
  border-left: 3px solid #52c41a;
}

.step-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  font-size: 12px;
}

.step.active .step-number {
  background: #1890ff;
  color: white;
}

.step.done .step-number {
  background: #52c41a;
  color: white;
}

.step-name {
  flex: 1;
  font-size: 14px;
  position: relative;
}

.step-time {
  position: absolute;
  right: 0;
  top: 0;
  font-size: 12px;
  color: #d9d9d9;
}

.step-connector {
  width: 2px;
  height: 10px;
  background: rgba(255, 255, 255, 0.1);
  margin-left: 11px;
}

/* 数字孪生面板样式 */
.digital-twin-dashboard {
  position: absolute;
  bottom: 10px;
  right: 10px;
  width: 200px;
  max-height: calc(70% - 20px);
  overflow-y: auto;
  background: rgba(0, 20, 40, 0.85);
  border-radius: 8px;
  color: #fff;
  font-size: 11px;
  padding: 10px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(24, 144, 255, 0.3);
  box-shadow: 0 0 15px rgba(24, 144, 255, 0.2);
  z-index: 10;
  transition: all 0.3s ease;
  opacity: 0.85;
}

.digital-twin-dashboard:hover {
  opacity: 1;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.dashboard-header h3 {
  margin: 0;
  font-size: 12px;
  color: #1890ff;
}

.dashboard-controls {
  display: flex;
  gap: 5px;
}

.minimize-btn {
  padding: 2px 6px;
  font-size: 10px;
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.charts-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 10px;
}

.chart-box {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  padding: 5px;
}

.chart-box h4 {
  margin: 0 0 5px 0;
  font-size: 11px;
  color: #d9d9d9;
}

.chart {
  height: 100px;
  width: 100%;
}

.alerts-section {
  margin-bottom: 10px;
}

.alerts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.alerts-header h4 {
  margin: 0;
  font-size: 11px;
  color: #d9d9d9;
}

.alert-count {
  background: #ff4d4f;
  color: white;
  border-radius: 10px;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 10px;
  font-weight: bold;
}

.no-alerts {
  font-size: 10px;
  color: #52c41a;
}

.alert-list {
  max-height: 120px;
  overflow-y: auto;
}

.alert-item {
  display: flex;
  gap: 5px;
  padding: 5px;
  border-radius: 4px;
  margin-bottom: 5px;
  background: rgba(0, 0, 0, 0.2);
  font-size: 10px;
}

.alert-item.warning {
  border-left: 2px solid #faad14;
}

.alert-item.critical {
  border-left: 2px solid #ff4d4f;
}

.alert-item.info {
  border-left: 2px solid #1890ff;
}

.alert-icon {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 2px;
}

.warning .alert-icon {
  background-color: #faad14;
}

.critical .alert-icon {
  background-color: #ff4d4f;
}

.info .alert-icon {
  background-color: #1890ff;
}

.alert-content {
  flex: 1;
}

.alert-title {
  font-weight: bold;
  margin-bottom: 2px;
}

.alert-message {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2px;
}

.alert-time {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.5);
}

.dismiss-btn {
  padding: 0;
  width: 16px;
  height: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  color: #fff;
  font-size: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dismiss-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.production-stats {
  margin-bottom: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5px;
}

.stats-item {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  padding: 5px;
  text-align: center;
}

.stats-label {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2px;
}

.stats-value {
  font-weight: bold;
  font-size: 12px;
}

.parameter-monitor {
  margin-bottom: 10px;
}

.param-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5px;
}

.param-item {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  padding: 5px;
  text-align: center;
}

.param-label {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2px;
}

.param-value {
  font-weight: bold;
  font-size: 12px;
}

.param-alert {
  background: rgba(255, 77, 79, 0.2);
  animation: param-blink 1s infinite;
}

@keyframes param-blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.alert-settings-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  background: rgba(0, 20, 40, 0.95);
  border-radius: 8px;
  border: 1px solid rgba(24, 144, 255, 0.5);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  border-bottom: 1px solid rgba(24, 144, 255, 0.2);
}

.dialog-header h3 {
  margin: 0;
  font-size: 14px;
}

.close-btn {
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  font-size: 14px;
  color: #fff;
  cursor: pointer;
}

.dialog-content {
  padding: 15px;
}

.threshold-item {
  margin-bottom: 15px;
}

.threshold-item label {
  display: block;
  font-size: 12px;
  margin-bottom: 5px;
  color: #d9d9d9;
}

.threshold-inputs {
  display: flex;
  align-items: center;
  gap: 5px;
}

.threshold-inputs input {
  flex: 1;
  padding: 5px;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #fff;
  font-size: 12px;
}

.dialog-footer {
  padding: 10px 15px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  border-top: 1px solid rgba(24, 144, 255, 0.2);
}

.save-btn {
  background-color: #1890ff;
  color: white;
  padding: 5px 10px;
  font-size: 12px;
}

.save-btn:hover {
  background-color: #40a9ff;
}

/* 添加面板切换按钮样式 */
.dashboard-toggle {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 20, 40, 0.7);
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  z-index: 11;
  border: 1px solid rgba(24, 144, 255, 0.5);
  transition: all 0.3s ease;
}

.dashboard-toggle:hover {
  background: rgba(24, 144, 255, 0.7);
}
</style> 
