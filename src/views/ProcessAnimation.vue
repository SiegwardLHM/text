<template>
  <div class="process-animation">
    <div class="page-title">
      <h1>胶囊模具溶胶蘸胶过程模拟</h1>
    </div>
    
    <div class="animation-container">
      <div class="animation-controls">
        <el-button type="primary" @click="startAnimation">开始动画</el-button>
        <el-button @click="resetAnimation">重置</el-button>
        <el-slider v-model="animationSpeed" :min="0.5" :max="2" :step="0.1" 
                   :format-tooltip="formatSpeedTooltip" @change="updateAnimationSpeed">
          <template #default>
            <div>速度: {{animationSpeed.toFixed(1)}}x</div>
          </template>
        </el-slider>
      </div>
      
      <div class="animation-stage">
        <div class="animation-frame">
          <!-- 机器框架结构 -->
          <div class="machine-frame">
            <div class="frame-vertical left"></div>
            <div class="frame-vertical right"></div>
            <div class="frame-horizontal top"></div>
            <div class="frame-horizontal bottom"></div>
            <div class="frame-support left-support"></div>
            <div class="frame-support right-support"></div>
          </div>
          
          <!-- 底部模具支撑平台 -->
          <div class="mold-platform">
            <div class="mold-platform-slots"></div>
          </div>
          
          <!-- 中间传动机构 -->
          <div class="transmission-mechanism">
            <div class="transmission-bar"></div>
            <div class="hydraulic-cylinder"></div>
            <div class="control-box">
              <div class="indicator-light" :class="{ 'active': isAnimating }"></div>
            </div>
          </div>
          
          <!-- 上部压力装置 -->
          <div class="press-device" :class="{ 'pressing-animation': isAnimating }">
            <div class="press-plate"></div>
            <div class="press-mold-holder">
              <div class="mold-pins"></div>
            </div>
          </div>
          
          <!-- 液压系统导轨 -->
          <div class="hydraulic-rails">
            <div class="rail left-rail"></div>
            <div class="rail right-rail"></div>
          </div>
          
          <!-- 溶胶容器（隐含在模具平台下方） -->
          <div class="gel-tank" :class="{ 'gel-active': isAnimating && currentStep >= 3 }">
            <div class="gel-liquid"></div>
          </div>
          
          <!-- 工作过程指示 -->
          <div class="process-indicator">
            <div class="step" :class="{ 'active': currentStep >= 1 }">设备准备</div>
            <div class="step" :class="{ 'active': currentStep >= 2 }">模具装载</div>
            <div class="step" :class="{ 'active': currentStep >= 3 }">溶胶加注</div>
            <div class="step" :class="{ 'active': currentStep >= 4 }">压力成型</div>
            <div class="step" :class="{ 'active': currentStep >= 5 }">脱模完成</div>
          </div>
          
          <!-- 操作人员指示 -->
          <div class="operator" :class="{ 'operator-active': isAnimating && (currentStep == 2 || currentStep == 5) }"></div>
        </div>
      </div>
      
      <div class="process-description">
        <div class="step-description" v-if="currentStep === 0">
          <h3>胶囊模具溶胶蘸胶过程说明</h3>
          <p>点击"开始动画"按钮观看胶囊模具溶胶蘸胶设备的整个工作过程演示。</p>
        </div>
        <div class="step-description" v-if="currentStep === 1">
          <h3>步骤 1: 设备准备</h3>
          <p>设备启动，液压系统加压，控制系统就绪，确保所有传感器及执行机构正常工作。</p>
        </div>
        <div class="step-description" v-if="currentStep === 2">
          <h3>步骤 2: 模具装载</h3>
          <p>操作人员将清洁干燥的模具阵列放置在设备底部支撑平台上，确保安全锁定。</p>
        </div>
        <div class="step-description" v-if="currentStep === 3">
          <h3>步骤 3: 溶胶加注</h3>
          <p>溶胶自动注入设备底部容器中，同时保持适当温度，确保溶胶的流动性和粘度符合工艺要求。</p>
        </div>
        <div class="step-description" v-if="currentStep === 4">
          <h3>步骤 4: 压力成型</h3>
          <p>上部压力装置下降，将模具精确浸入溶胶中，施加均匀压力，确保溶胶均匀附着在模具表面。</p>
        </div>
        <div class="step-description" v-if="currentStep === 5">
          <h3>步骤 5: 脱模完成</h3>
          <p>压力释放，上部装置上升，操作人员取出完成蘸胶的模具，送入下一工序进行凝固和干燥处理。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProcessAnimation',
  data() {
    return {
      isAnimating: false,
      currentStep: 0,
      animationSpeed: 1,
      animationTimer: null,
      stepTimers: []
    }
  },
  methods: {
    startAnimation() {
      if (this.isAnimating) return;
      
      this.resetAnimation();
      this.isAnimating = true;
      this.currentStep = 1;
      
      // 定时器控制各个步骤的进展
      const stepDuration = 2000 / this.animationSpeed; // 基础步骤持续时间
      
      // 第二步：模具装载
      this.stepTimers.push(setTimeout(() => {
        this.currentStep = 2;
      }, stepDuration));
      
      // 第三步：溶胶加注
      this.stepTimers.push(setTimeout(() => {
        this.currentStep = 3;
      }, stepDuration * 2));
      
      // 第四步：压力成型
      this.stepTimers.push(setTimeout(() => {
        this.currentStep = 4;
      }, stepDuration * 3));
      
      // 第五步：脱模完成
      this.stepTimers.push(setTimeout(() => {
        this.currentStep = 5;
      }, stepDuration * 5));
      
      // 动画结束后重置
      this.animationTimer = setTimeout(() => {
        this.isAnimating = false;
        setTimeout(() => {
          this.resetAnimation();
        }, 1000);
      }, stepDuration * 6);
    },
    resetAnimation() {
      this.isAnimating = false;
      this.currentStep = 0;
      
      // 清除所有定时器
      if (this.animationTimer) {
        clearTimeout(this.animationTimer);
      }
      
      this.stepTimers.forEach(timer => {
        clearTimeout(timer);
      });
      
      this.stepTimers = [];
    },
    updateAnimationSpeed(speed) {
      this.animationSpeed = speed;
      // 如果正在动画中，重启动画以应用新速度
      if (this.isAnimating) {
        this.startAnimation();
      }
    },
    formatSpeedTooltip(val) {
      return `${val.toFixed(1)}x`;
    }
  },
  beforeDestroy() {
    this.resetAnimation();
  }
}
</script>

<style scoped>
.process-animation {
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.page-title {
  margin-bottom: 20px;
  text-align: center;
}

.page-title h1 {
  color: #409EFF;
  font-size: 24px;
}

.animation-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(0, 20, 60, 0.5);
  border-radius: 8px;
  padding: 20px;
  overflow: hidden;
}

.animation-controls {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.animation-stage {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 10, 30, 0.7);
  border-radius: 8px;
  margin-bottom: 20px;
  position: relative;
  min-height: 350px;
}

.animation-frame {
  position: relative;
  width: 90%;
  height: 90%;
  display: flex;
  justify-content: center;
  perspective: 800px;
}

/* 机器框架 */
.machine-frame {
  position: absolute;
  width: 400px;
  height: 300px;
  transform-style: preserve-3d;
}

.frame-vertical {
  position: absolute;
  width: 15px;
  height: 300px;
  background: #333;
  border: 1px solid #555;
}

.frame-vertical.left {
  left: 0;
}

.frame-vertical.right {
  right: 0;
}

.frame-horizontal {
  position: absolute;
  width: 400px;
  height: 15px;
  background: #333;
  border: 1px solid #555;
}

.frame-horizontal.top {
  top: 0;
}

.frame-horizontal.bottom {
  bottom: 0;
}

.frame-support {
  position: absolute;
  width: 40px;
  height: 280px;
  background: #444;
  border: 1px solid #666;
  bottom: 15px;
}

.frame-support.left-support {
  left: 40px;
}

.frame-support.right-support {
  right: 40px;
}

/* 底部模具支撑平台 */
.mold-platform {
  position: absolute;
  width: 320px;
  height: 40px;
  background: #666;
  border: 2px solid #777;
  border-radius: 2px;
  bottom: 30px;
  z-index: 2;
}

.mold-platform-slots {
  position: absolute;
  width: 280px;
  height: 20px;
  background: #444;
  border-top: 1px solid #888;
  top: 10px;
  left: 20px;
}

.mold-platform-slots:before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(90deg, #444, #444 8px, #333 8px, #333 16px);
}

/* 中间传动机构 */
.transmission-mechanism {
  position: absolute;
  width: 320px;
  height: 100px;
  top: 80px;
  z-index: 3;
}

.transmission-bar {
  position: absolute;
  width: 260px;
  height: 12px;
  background: #555;
  border: 1px solid #999;
  left: 30px;
  top: 44px;
}

.hydraulic-cylinder {
  position: absolute;
  width: 30px;
  height: 80px;
  background: #777;
  border: 1px solid #aaa;
  border-radius: 4px;
  left: 145px;
  top: 10px;
}

.control-box {
  position: absolute;
  width: 40px;
  height: 25px;
  background: #2c3e50;
  border: 1px solid #34495e;
  border-radius: 2px;
  right: 30px;
  top: 40px;
}

.indicator-light {
  position: absolute;
  width: 8px;
  height: 8px;
  background: #e74c3c;
  border-radius: 50%;
  top: 8px;
  left: 8px;
  box-shadow: 0 0 2px rgba(231, 76, 60, 0.5);
}

.indicator-light.active {
  background: #2ecc71;
  box-shadow: 0 0 6px rgba(46, 204, 113, 0.8);
}

/* 上部压力装置 */
.press-device {
  position: absolute;
  width: 280px;
  height: 120px;
  top: 20px;
  z-index: 4;
  transition: transform 2s ease-in-out;
}

.press-plate {
  position: absolute;
  width: 280px;
  height: 15px;
  background: #555;
  border: 1px solid #777;
  top: 0;
}

.press-mold-holder {
  position: absolute;
  width: 240px;
  height: 80px;
  background: #666;
  border: 1px solid #888;
  top: 15px;
  left: 20px;
}

.mold-pins {
  position: absolute;
  width: 200px;
  height: 25px;
  background: #444;
  bottom: 0;
  left: 20px;
}

.mold-pins:before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(90deg, #444, #444 6px, #333 6px, #333 12px);
}

.press-device.pressing-animation {
  animation: press-motion 6s ease-in-out forwards;
}

/* 液压系统导轨 */
.hydraulic-rails {
  position: absolute;
  width: 320px;
  height: 260px;
  z-index: 1;
}

.rail {
  position: absolute;
  width: 8px;
  height: 260px;
  background: #555;
  border: 1px solid #777;
}

.rail.left-rail {
  left: 80px;
}

.rail.right-rail {
  right: 80px;
}

/* 溶胶容器 */
.gel-tank {
  position: absolute;
  width: 240px;
  height: 0;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(100, 100, 100, 0.5);
  bottom: 70px;
  left: 80px;
  z-index: 0;
  overflow: hidden;
  transition: height 1s ease-in-out;
}

.gel-tank.gel-active {
  height: 50px;
}

.gel-liquid {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(52, 152, 219, 0.3), rgba(41, 128, 185, 0.6));
  animation: gel-bubble 4s ease-in-out infinite;
}

/* 工作过程指示 */
.process-indicator {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  z-index: 10;
}

.process-indicator .step {
  padding: 5px 10px;
  background: rgba(0, 0, 0, 0.3);
  color: rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.process-indicator .step.active {
  background: rgba(64, 158, 255, 0.7);
  color: white;
}

/* 操作人员 */
.operator {
  position: absolute;
  width: 20px;
  height: 40px;
  background: #3498db;
  border-radius: 50% 50% 0 0;
  bottom: 15px;
  right: -50px;
  opacity: 0;
  transition: all 0.5s ease;
}

.operator:before {
  content: '';
  position: absolute;
  width: 15px;
  height: 15px;
  background: #f1c40f;
  border-radius: 50%;
  top: -10px;
  left: 2.5px;
}

.operator.operator-active {
  opacity: 1;
  right: 50px;
}

/* 描述部分 */
.process-description {
  height: 100px;
  background: rgba(0, 10, 30, 0.5);
  border-radius: 8px;
  padding: 15px;
  color: #eee;
}

.step-description h3 {
  color: #409EFF;
  margin-top: 0;
  margin-bottom: 10px;
}

.step-description p {
  margin: 0;
  line-height: 1.5;
}

/* 动画定义 */
@keyframes gel-bubble {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}

@keyframes press-motion {
  0% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(120px);
  }
  70% {
    transform: translateY(120px);
  }
  100% {
    transform: translateY(0);
  }
}
</style> 