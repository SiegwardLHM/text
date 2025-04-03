<template>
  <div class="production-line">
    <div class="page-title">
      <h1>胶模具生产线模拟</h1>
      <p>实时监控生产线运行状态</p>
    </div>

    <!-- 状态卡片 -->
    <div class="status-cards">
      <div class="status-card">
        <div class="card-title">
          <i class="el-icon-data-line"></i>
          <span>蘸胶状态</span>
        </div>
        <div class="card-content">
          <div class="status-row">
            <span>温度:</span>
            <span data-field="glue-temperature" :class="{ updating: updatingFields.has('glue-temperature') }">
              {{ glueStatus.temperature }}°C
            </span>
          </div>
          <div class="status-row">
            <span>浓度:</span>
            <span data-field="glue-concentration" :class="{ updating: updatingFields.has('glue-concentration') }">
              {{ glueStatus.concentration }}%
            </span>
          </div>
          <div class="status-row">
            <span>粘度:</span>
            <span data-field="glue-viscosity" :class="{ updating: updatingFields.has('glue-viscosity') }">
              {{ glueStatus.viscosity }}mPa·s
            </span>
          </div>
        </div>
      </div>

      <div class="status-card">
        <div class="card-title">
          <i class="el-icon-s-platform"></i>
          <span>模具状态</span>
        </div>
        <div class="card-content">
          <div class="status-row">
            <span>温度:</span>
            <span data-field="mold-temperature" :class="{ updating: updatingFields.has('mold-temperature') }">
              {{ moldStatus.temperature }}°C
            </span>
          </div>
          <div class="status-row">
            <span>湿度:</span>
            <span data-field="mold-humidity" :class="{ updating: updatingFields.has('mold-humidity') }">
              {{ moldStatus.humidity }}%
            </span>
          </div>
          <div class="status-row">
            <span>压力:</span>
            <span data-field="mold-pressure" :class="{ updating: updatingFields.has('mold-pressure') }">
              {{ moldStatus.pressure }} MPa
            </span>
          </div>
        </div>
      </div>

      <div class="status-card">
        <div class="card-title">
          <i class="el-icon-s-data"></i>
          <span>生产统计</span>
        </div>
        <div class="card-content">
          <div class="status-row">
            <span>今日产量:</span>
            <span data-field="daily-production" :class="{ updating: updatingFields.has('daily-production') }">
              {{ dailyProduction }} 个
            </span>
          </div>
          <div class="status-row">
            <span>合格品:</span>
            <span data-field="qualified-products" :class="{ updating: updatingFields.has('qualified-products') }">
              {{ qualifiedProducts }} 个
            </span>
          </div>
          <div class="status-row">
            <span>不合格品:</span>
            <span data-field="unqualified-products" :class="{ updating: updatingFields.has('unqualified-products') }">
              {{ unqualifiedProducts }} 个
            </span>
          </div>
        </div>
      </div>

      <div class="status-card">
        <div class="card-title">
          <i class="el-icon-warning"></i>
          <span>质量检测</span>
        </div>
        <div class="card-content">
          <div class="status-row">
            <span>外观检测:</span>
            <span data-field="appearance-check" 
                  :class="[qualityStatus.appearance.class, { updating: updatingFields.has('appearance-check') }]">
              {{ qualityStatus.appearance.status }}
            </span>
          </div>
          <div class="status-row">
            <span>尺寸检测:</span>
            <span data-field="size-check"
                  :class="[qualityStatus.size.class, { updating: updatingFields.has('size-check') }]">
              {{ qualityStatus.size.status }}
            </span>
          </div>
          <div class="status-row">
            <span>完整性:</span>
            <span data-field="integrity-check"
                  :class="[qualityStatus.integrity.class, { updating: updatingFields.has('integrity-check') }]">
              {{ qualityStatus.integrity.value }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 生产线流程 -->
    <div class="production-flow">
      <div class="flow-stages">
        <div v-for="(stage, index) in stages" :key="index" class="flow-stage">
          <div class="stage-box" :class="{ active: stage.active }">
            <div class="stage-icon">
              <i :class="stage.icon"></i>
            </div>
            <div class="stage-label">{{ stage.name }}</div>
            <div class="stage-status">{{ stage.status }}</div>
            <div v-if="stage.name === '模具监测'" class="mold-inspection">
              <div class="mold-array">
                <div v-for="i in 100" :key="i" class="mold-point" 
                     :class="{ 'inspecting': stage.active && isInspecting(i) }">
                </div>
              </div>
              <div class="inspection-progress" v-if="stage.active"></div>
            </div>
            <div v-else class="stage-params">
              <div v-for="(value, key) in stage.parameters" :key="key" class="param-row">
                {{ key }}: {{ value }}
              </div>
            </div>
          </div>
          <div v-if="index < stages.length - 1" class="flow-connector" :class="{ active: stage.active }"></div>
        </div>
      </div>
    </div>

    <!-- 控制面板 -->
    <div class="control-section">
      <div class="control-panel">
        <div class="panel-buttons">
          <el-button type="primary" size="small" @click="startProduction">
            <i class="el-icon-video-play"></i> 恢复生产
          </el-button>
          <el-button type="warning" size="small" @click="pauseProduction">
            <i class="el-icon-timer"></i> 暂停
          </el-button>
          <el-button type="info" size="small" @click="resetProduction">
            <i class="el-icon-refresh"></i> 重置
          </el-button>
        </div>
        <div class="panel-sliders">
          <div class="slider-item">
            <span>溶胶温度</span>
            <el-slider v-model="solTemperature" :min="20" :max="30"></el-slider>
          </div>
          <div class="slider-item">
            <span>搅拌速度</span>
            <el-slider v-model="stirringSpeed" :min="40" :max="80"></el-slider>
          </div>
          <div class="slider-item">
            <span>蘸胶温度</span>
            <el-slider v-model="temperatureControl" :min="20" :max="40"></el-slider>
          </div>
          <div class="slider-item">
            <span>干燥时间</span>
            <el-slider v-model="dryingTime" :min="15" :max="45"></el-slider>
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-section">
      <div class="chart-container">
        <h3>实时产量监控</h3>
        <div ref="productionChart" class="chart"></div>
      </div>
      <div class="chart-container">
        <h3>质量分析</h3>
        <div ref="qualityChart" class="chart"></div>
      </div>
      <div class="chart-container">
        <h3>温度趋势监控</h3>
        <div ref="temperatureChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'ProductionLine',
  data() {
    return {
      productionStatus: {
        running: false,
        speed: 100,
        qualityRate: 98.5
      },
      temperature: 25,
      humidity: 45,
      pressure: 1.0,
      dailyProduction: 0,
      qualifiedProducts: 0,
      unqualifiedProducts: 0,
      alarms: [],
      stages: [
        {
          name: '溶胶',
          icon: 'el-icon-coffee-cup',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '温度': '25°C',
            '时间': '20min',
            '搅拌速度': '60rpm'
          }
        },
        {
          name: '蘸胶',
          icon: 'el-icon-receiving',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '温度': '25°C',
            '浓度': '98%',
            '粘度': '350mPa·s'
          }
        },
        {
          name: '产品检测1',
          icon: 'el-icon-view',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '外观': '正常',
            '尺寸': '标准',
            '完整性': '100%'
          }
        },
        {
          name: '干燥',
          icon: 'el-icon-sunny',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '温度': '60°C',
            '时间': '30min',
            '湿度': '45%'
          }
        },
        {
          name: '模具监测',
          icon: 'el-icon-monitor',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '模具状态': '正常',
            '运行时间': '0h',
            '维护状态': '正常'
          }
        },
        {
          name: '产品检测2',
          icon: 'el-icon-view',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '外观': '正常',
            '硬度': '标准',
            '完整性': '100%'
          }
        },
        {
          name: '投壳',
          icon: 'el-icon-box',
          active: false,
          warning: false,
          error: false,
          status: '待机中',
          parameters: {
            '包装状态': '待包装',
            '入库数量': '0',
            '批次号': '-'
          }
        }
      ],
      speedControl: 100,
      selectedFault: '',
      productionChart: null,
      qualityChart: null,
      temperatureControl: 25,
      dryingTime: 30,
      temperatureData: [],
      simulationInterval: null,
      updatingParams: [],
      statusCards: [
        { title: '蘸胶状态', icon: 'el-icon-s-data' },
        { title: '模具状态', icon: 'el-icon-s-platform' },
        { title: '生产统计', icon: 'el-icon-s-marketing' },
        { title: '质量检测', icon: 'el-icon-warning-outline' }
      ],
      glueStatus: {
        temperature: 24.5,
        concentration: 98,
        viscosity: 350
      },
      moldStatus: {
        temperature: 24.5,
        humidity: 45,
        pressure: 1.0
      },
      updatingFields: new Set(),
      qualityStatus: {
        appearance: {
          status: '正常',
          class: 'status-tag success'
        },
        size: {
          status: '合格',
          class: 'status-tag success'
        },
        integrity: {
          value: 100,
          class: 'status-tag success'
        }
      },
      solTemperature: 25,
      stirringSpeed: 60
    }
  },
  mounted() {
    this.initCharts()
    this.startDataCollection()
  },
  beforeDestroy() {
    this.stopSimulation()
    if (this.productionChart) {
      this.productionChart.dispose()
    }
    if (this.qualityChart) {
      this.qualityChart.dispose()
    }
  },
  methods: {
    initCharts() {
      const chartTheme = {
        backgroundColor: 'transparent',
        textStyle: {
          color: 'rgba(255, 255, 255, 0.65)'
        },
        title: {
          textStyle: {
            color: 'rgba(255, 255, 255, 0.85)'
          }
        },
        legend: {
          textStyle: {
            color: 'rgba(255, 255, 255, 0.65)'
          }
        },
        xAxis: {
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.15)'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.08)'
            }
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.65)'
          }
        },
        yAxis: {
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.15)'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.08)'
            }
          },
          axisLabel: {
            color: 'rgba(255, 255, 255, 0.65)'
          }
        }
      };

      // 初始化产量图表
      this.productionChart = echarts.init(this.$refs.productionChart);
      this.productionChart.setOption({
        ...chartTheme,
        grid: {
          top: 40,
          right: 20,
          bottom: 40,
          left: 60
        },
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          borderColor: 'rgba(255, 255, 255, 0.15)',
          textStyle: {
            color: '#fff'
          }
        },
        xAxis: {
          type: 'time',
          splitLine: { show: false }
        },
        yAxis: {
          type: 'value',
          name: '产量(个)'
        },
        series: [{
          name: '产量',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            color: '#1890ff',
            width: 2
          },
          itemStyle: {
            color: '#1890ff',
            borderWidth: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
              offset: 0,
              color: 'rgba(24, 144, 255, 0.3)'
            }, {
              offset: 1,
              color: 'rgba(24, 144, 255, 0)'
            }])
          },
          data: this.productionData
        }]
      });

      // 初始化质量图表
      this.qualityChart = echarts.init(this.$refs.qualityChart);
      this.qualityChart.setOption({
        ...chartTheme,
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          borderColor: 'rgba(255, 255, 255, 0.15)',
          textStyle: {
            color: '#fff'
          }
        },
        legend: {
          orient: 'vertical',
          right: 10,
          top: 'center'
        },
        series: [{
          name: '产品质量',
          type: 'pie',
          radius: ['50%', '70%'],
          center: ['40%', '50%'],
          itemStyle: {
            borderColor: 'rgba(0, 0, 0, 0.2)',
            borderWidth: 1
          },
          label: {
            show: false
          },
          data: [
            {
              value: this.qualifiedProducts,
              name: '合格品',
              itemStyle: { color: '#52c41a' }
            },
            {
              value: this.unqualifiedProducts,
              name: '不合格品',
              itemStyle: { color: '#f5222d' }
            }
          ]
        }]
      });

      // 初始化温度趋势图
      this.temperatureChart = echarts.init(this.$refs.temperatureChart);
      this.temperatureChart.setOption({
        ...chartTheme,
        grid: {
          top: 40,
          right: 20,
          bottom: 40,
          left: 60
        },
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(0, 0, 0, 0.75)',
          borderColor: 'rgba(255, 255, 255, 0.15)',
          textStyle: {
            color: '#fff'
          }
        },
        xAxis: {
          type: 'time',
          splitLine: { show: false }
        },
        yAxis: {
          type: 'value',
          name: '温度(°C)'
        },
        series: [{
          name: '温度',
          type: 'line',
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            color: '#faad14',
            width: 2
          },
          itemStyle: {
            color: '#faad14',
            borderWidth: 2
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
              offset: 0,
              color: 'rgba(250, 173, 20, 0.3)'
            }, {
              offset: 1,
              color: 'rgba(250, 173, 20, 0)'
            }])
          },
          data: this.temperatureData
        }]
      });
    },
    startProduction() {
      this.productionStatus.running = true
      this.startSimulation()
      this.$message.success('生产线已启动')
    },
    stopProduction() {
      this.productionStatus.running = false
      this.stopSimulation()
      this.$message.warning('生产线已停止')
    },
    pauseProduction() {
      this.productionStatus.running = false
      this.stopSimulation()
      this.$message.info('生产线已暂停')
    },
    resetProduction() {
      this.stopSimulation()
      this.resetData()
      this.$message.success('系统已重置')
    },
    startSimulation() {
      if (this.simulationInterval) {
        clearInterval(this.simulationInterval)
      }
      this.simulationInterval = setInterval(() => {
        this.updateSimulation()
      }, 2000)
    },
    stopSimulation() {
      if (this.simulationInterval) {
        clearInterval(this.simulationInterval)
        this.simulationInterval = null
      }
    },
    updateSimulation() {
      // 更新各阶段状态
      this.updateStages()
      
      // 更新生产数据
      this.updateProductionData()
      
      // 更新环境参数
      this.updateEnvironmentData()
      
      // 更新图表
      this.updateCharts()
    },
    updateStages() {
      const stageKeys = Object.keys(this.stages)
      const currentStageIndex = stageKeys.findIndex(key => this.stages[key].active)
      
      if (currentStageIndex === -1) {
        this.stages[0].active = true
        this.stages[0].status = '运行中'
        this.updateStageParameters(0)
        return
      }

      if (currentStageIndex < this.stages.length - 1) {
        setTimeout(() => {
          this.stages[currentStageIndex].active = false
          this.stages[currentStageIndex].status = '完成'
          this.stages[currentStageIndex + 1].active = true
          this.stages[currentStageIndex + 1].status = '运行中'
          this.updateStageParameters(currentStageIndex + 1)
        }, 1000)
      } else {
        this.stages[currentStageIndex].active = false
        this.stages[currentStageIndex].status = '完成'
        this.stages[0].active = true
        this.stages[0].status = '运行中'
        this.updateStageParameters(0)
      }
    },
    updateProductionData() {
      // 生成随机的生产数据
      const newProduction = Math.floor(Math.random() * 3) + 1 // 每次增加1-3个
      const qualityRate = 0.95 + Math.random() * 0.05 // 95%-100%的合格率
      
      // 更新生产统计
      const oldDailyProduction = this.dailyProduction
      const oldQualified = this.qualifiedProducts
      const oldUnqualified = this.unqualifiedProducts
      
      this.dailyProduction += newProduction
      const qualifiedCount = Math.floor(newProduction * qualityRate)
      this.qualifiedProducts += qualifiedCount
      this.unqualifiedProducts += (newProduction - qualifiedCount)
      
      // 触发数值更新动画
      if (oldDailyProduction !== this.dailyProduction) {
        this.updateValue('daily-production', oldDailyProduction, this.dailyProduction)
      }
      if (oldQualified !== this.qualifiedProducts) {
        this.updateValue('qualified-products', oldQualified, this.qualifiedProducts)
      }
      if (oldUnqualified !== this.unqualifiedProducts) {
        this.updateValue('unqualified-products', oldUnqualified, this.unqualifiedProducts)
      }
      
      // 更新质量检测状态
      this.updateQualityStatus()
    },
    updateQualityStatus() {
      // 随机生成质量检测结果
      const randomQuality = Math.random()
      
      // 更新外观检测
      const oldAppearance = this.qualityStatus.appearance.status
      if (randomQuality > 0.98) {
        this.qualityStatus.appearance.status = '异常'
        this.qualityStatus.appearance.class = 'status-tag error'
      } else if (randomQuality > 0.95) {
        this.qualityStatus.appearance.status = '警告'
        this.qualityStatus.appearance.class = 'status-tag warning'
      } else {
        this.qualityStatus.appearance.status = '正常'
        this.qualityStatus.appearance.class = 'status-tag success'
      }
      if (oldAppearance !== this.qualityStatus.appearance.status) {
        this.updateValue('appearance-check', oldAppearance, this.qualityStatus.appearance.status)
      }
      
      // 更新尺寸检测
      const oldSize = this.qualityStatus.size.status
      if (randomQuality > 0.97) {
        this.qualityStatus.size.status = '不合格'
        this.qualityStatus.size.class = 'status-tag error'
      } else {
        this.qualityStatus.size.status = '合格'
        this.qualityStatus.size.class = 'status-tag success'
      }
      if (oldSize !== this.qualityStatus.size.status) {
        this.updateValue('size-check', oldSize, this.qualityStatus.size.status)
      }
      
      // 更新完整性
      const oldIntegrity = this.qualityStatus.integrity.value
      const newIntegrity = 95 + Math.floor(Math.random() * 6) // 95-100%
      this.qualityStatus.integrity.value = newIntegrity
      if (newIntegrity < 97) {
        this.qualityStatus.integrity.class = 'status-tag warning'
      } else {
        this.qualityStatus.integrity.class = 'status-tag success'
      }
      if (oldIntegrity !== newIntegrity) {
        this.updateValue('integrity-check', oldIntegrity, newIntegrity)
      }
    },
    updateEnvironmentData() {
      // 更新蘸胶状态
      const newGlueTemp = +(24.5 + Math.random() * 1 - 0.5).toFixed(1)
      const newGlueConc = +(98 + Math.random() * 0.4 - 0.2).toFixed(1)
      const newGlueVisc = +(350 + Math.random() * 10 - 5).toFixed(0)
      
      if (this.glueStatus.temperature !== newGlueTemp) {
        this.updateValue('glue-temperature', this.glueStatus.temperature, newGlueTemp)
        this.glueStatus.temperature = newGlueTemp
      }
      
      if (this.glueStatus.concentration !== newGlueConc) {
        this.updateValue('glue-concentration', this.glueStatus.concentration, newGlueConc)
        this.glueStatus.concentration = newGlueConc
      }
      
      if (this.glueStatus.viscosity !== newGlueVisc) {
        this.updateValue('glue-viscosity', this.glueStatus.viscosity, newGlueVisc)
        this.glueStatus.viscosity = newGlueVisc
      }

      // 更新模具状态
      const newMoldTemp = +(24.5 + Math.random() * 1 - 0.5).toFixed(1)
      const newMoldHum = +(45 + Math.random() * 2 - 1).toFixed(1)
      const newMoldPress = +(1.0 + Math.random() * 0.1 - 0.05).toFixed(2)
      
      if (this.moldStatus.temperature !== newMoldTemp) {
        this.updateValue('mold-temperature', this.moldStatus.temperature, newMoldTemp)
        this.moldStatus.temperature = newMoldTemp
      }
      
      if (this.moldStatus.humidity !== newMoldHum) {
        this.updateValue('mold-humidity', this.moldStatus.humidity, newMoldHum)
        this.moldStatus.humidity = newMoldHum
      }
      
      if (this.moldStatus.pressure !== newMoldPress) {
        this.updateValue('mold-pressure', this.moldStatus.pressure, newMoldPress)
        this.moldStatus.pressure = newMoldPress
      }

      // 检查是否需要触发报警
      this.checkAlarms()
    },
    updateValue(field, oldValue, newValue) {
      // 添加到更新集合
      this.updatingFields.add(field)
      
      // 获取对应的DOM元素
      const element = document.querySelector(`[data-field="${field}"]`)
      if (element) {
        element.classList.add('updating')
        
        // 500ms后移除动画效果
        setTimeout(() => {
          element.classList.remove('updating')
          this.updatingFields.delete(field)
        }, 500)
      }
    },
    updateCharts() {
      if (this.productionChart && this.qualityChart) {
        // 添加图表更新动画
        const chartWrappers = document.querySelectorAll('.chart-wrapper')
        chartWrappers.forEach(wrapper => {
          wrapper.classList.add('updating')
          setTimeout(() => {
            wrapper.classList.remove('updating')
          }, 2000)
        })

        // 更新图表数据
        this.productionChart.setOption({
          series: [{
            data: this.productionData
          }]
        })
        
        this.qualityChart.setOption({
          series: [{
            data: [
              { value: this.qualifiedProducts, name: '合格品' },
              { value: this.unqualifiedProducts, name: '不合格品' }
            ]
          }]
        })
      }
    },
    checkAlarms() {
      this.alarms = []
      
      if (this.temperature > 30) {
        this.alarms.push({
          type: '温度警告',
          message: '设备温度过高'
        })
      }
      
      if (this.humidity > 70) {
        this.alarms.push({
          type: '湿度警告',
          message: '环境湿度异常'
        })
      }
      
      if (this.pressure < 0.8 || this.pressure > 1.2) {
        this.alarms.push({
          type: '压力警告',
          message: '系统压力异常'
        })
      }
    },
    updateSpeed(value) {
      this.productionStatus.speed = value
      this.$message.success(`生产速度已调整为 ${value} 个/小时`)
    },
    triggerFault() {
      switch (this.selectedFault) {
        case 'high-temp':
          this.temperature = 35
          break
        case 'pressure-fault':
          this.pressure = 1.5
          break
        case 'device-stuck':
          this.stopProduction()
          this.stages.forEach(stage => {
            stage.error = true
            stage.status = '故障'
          })
          break
      }
      this.$message.error(`已触发故障: ${this.selectedFault}`)
    },
    resetData() {
      this.productionStatus.running = false
      this.dailyProduction = 0
      this.qualifiedProducts = 0
      this.unqualifiedProducts = 0
      this.alarms = []
      this.productionData = []
      this.stages.forEach(stage => {
        stage.active = false
        stage.warning = false
        stage.error = false
        stage.status = '待机中'
      })
      this.updateCharts()
    },
    startDataCollection() {
      // 启动数据采集
      setInterval(() => {
        if (this.productionStatus.running) {
          this.updateEnvironmentData()
        }
      }, 5000)
    },
    updateTemperature(value) {
      this.temperatureControl = value
      this.$message.success(`蘸胶温度已调整为 ${value}°C`)
    },
    updateDryingTime(value) {
      this.dryingTime = value
      this.$message.success(`干燥时间已调整为 ${value}分钟`)
    },
    isUpdating(stageName, paramKey) {
      // 根据参数变化返回是否正在更新
      return this.updatingParams.includes(`${stageName}-${paramKey}`);
    },
    updateStageParameters(stageIndex) {
      const stage = this.stages[stageIndex]
      const params = stage.parameters
      
      // 记录正在更新的参数
      this.updatingParams = []
      
      Object.keys(params).forEach(key => {
        this.updatingParams.push(`${stage.name}-${key}`)
        
        // 模拟参数变化
        setTimeout(() => {
          const index = this.updatingParams.indexOf(`${stage.name}-${key}`)
          if (index > -1) {
            this.updatingParams.splice(index, 1)
          }
        }, 500)
      })
      
      if (stage.name === '模具监测') {
        // 更新模具监测的参数
        const inspectedCount = Math.floor(Math.random() * 20) + 980; // 980-1000之间
        const runtime = Math.floor(Math.random() * 10); // 0-10小时
        
        stage.parameters = {
          '检测数量': `${inspectedCount}/1000`,
          '运行时间': `${runtime}h`,
          '维护状态': inspectedCount > 990 ? '正常' : '需维护'
        };
      }
    },
    isInspecting(index) {
      // 创建一个移动的检测窗口效果
      const time = Date.now() / 1000; // 当前时间（秒）
      const cycleLength = 3; // 循环周期（秒）
      const position = (time % cycleLength) / cycleLength; // 0 到 1 之间的值
      
      // 计算当前检测的点的范围
      const inspectionWidth = 0.2; // 检测窗口宽度（占总宽度的比例）
      const startPoint = position * 100; // 开始检测的点
      const endPoint = startPoint + (inspectionWidth * 100); // 结束检测的点
      
      return index >= startPoint && index <= endPoint;
    }
  }
}
</script>

<style scoped>
.production-line {
  padding: 20px;
  background-color: #001529;
  min-height: 100vh;
  color: #fff;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
}

.page-title h1 {
  font-size: 24px;
  color: #fff;
  margin: 0;
}

.page-title p {
  color: rgba(255, 255, 255, 0.65);
  margin-top: 8px;
}

.status-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.status-card {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 4px;
  padding: 16px;
}

.card-title {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  color: rgba(255, 255, 255, 0.85);
}

.card-title i {
  font-size: 20px;
  margin-right: 8px;
  color: #1890ff;
}

.status-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.status-row span:first-child {
  color: rgba(255, 255, 255, 0.65);
}

.status-row span:last-child {
  color: rgba(255, 255, 255, 0.85);
  transition: all 0.3s;
  position: relative;
}

.status-row span.updating {
  animation: valueUpdate 0.5s ease;
  color: #1890ff;
}

@keyframes valueUpdate {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.status-tag {
  padding: 2px 8px;
  border-radius: 2px;
  font-size: 12px;
}

.status-tag.success {
  background: rgba(82, 196, 26, 0.15);
  border: 1px solid #52c41a;
  color: #52c41a;
}

.status-tag.warning {
  background: rgba(250, 173, 20, 0.15);
  border: 1px solid #faad14;
  color: #faad14;
}

.status-tag.error {
  background: rgba(245, 34, 45, 0.15);
  border: 1px solid #f5222d;
  color: #f5222d;
}

.production-flow {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 4px;
  padding: 20px 16px;
  margin-bottom: 30px;
}

.flow-stages {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.flow-stage {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 0 4px;
}

.stage-box {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 12px 8px;
  width: 120px;
  min-width: 120px;
  text-align: center;
  transition: all 0.3s;
  &[data-stage="模具监测"] {
    width: 140px;
    min-width: 140px;
  }
}

.stage-box.active {
  background: rgba(24, 144, 255, 0.2);
  box-shadow: 0 0 10px rgba(24, 144, 255, 0.3);
}

.stage-icon {
  font-size: 20px;
  color: #1890ff;
  margin-bottom: 6px;
}

.stage-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  margin-bottom: 3px;
}

.stage-status {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.45);
  margin-bottom: 6px;
}

.stage-params {
  text-align: left;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.65);
}

.param-row {
  margin-bottom: 2px;
}

.flow-connector {
  flex: 0 0 20px;
  height: 2px;
  background: rgba(255, 255, 255, 0.08);
  position: relative;
  margin: 0 4px;
}

.flow-connector.active::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #1890ff;
  animation: flowLine 2s infinite linear;
}

@keyframes flowLine {
  0% {
    transform: scaleX(0);
    transform-origin: left center;
  }
  50% {
    transform: scaleX(1);
    transform-origin: left center;
  }
  50.1% {
    transform: scaleX(1);
    transform-origin: right center;
  }
  100% {
    transform: scaleX(0);
    transform-origin: right center;
  }
}

.control-section {
  margin-bottom: 30px;
}

.control-panel {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 4px;
  padding: 20px;
}

.panel-buttons {
  margin-bottom: 20px;
}

.panel-buttons .el-button {
  margin-right: 10px;
}

.panel-sliders {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.slider-item {
  color: rgba(255, 255, 255, 0.85);
}

.slider-item span {
  display: block;
  margin-bottom: 8px;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.chart-container {
  background: rgba(255, 255, 255, 0.04);
  border-radius: 4px;
  padding: 16px;
}

.chart-container h3 {
  color: rgba(255, 255, 255, 0.85);
  font-size: 14px;
  margin: 0 0 16px 0;
}

.chart {
  height: 300px;
}

/* Element UI 组件样式覆盖 */
:deep(.el-slider__runway) {
  background-color: rgba(255, 255, 255, 0.1);
}

:deep(.el-slider__bar) {
  background-color: #1890ff;
}

:deep(.el-slider__button) {
  border-color: #1890ff;
}

:deep(.el-button) {
  border: none;
}

:deep(.el-button--primary) {
  background: #1890ff;
}

:deep(.el-button--warning) {
  background: #faad14;
}

:deep(.el-button--info) {
  background: #8c8c8c;
}

.mold-inspection {
  width: 100%;
  height: 100px;
  position: relative;
  margin-top: 8px;
}

.mold-array {
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: 2px;
  padding: 4px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.mold-point {
  width: 8px;
  height: 8px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transition: all 0.3s;
}

.mold-point.inspecting {
  background: #1890ff;
  box-shadow: 0 0 4px #1890ff;
  animation: pulse 1s infinite;
}

.inspection-progress {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    rgba(24, 144, 255, 0.1), 
    rgba(24, 144, 255, 0.2)
  );
  animation: scanProgress 3s linear infinite;
  pointer-events: none;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes scanProgress {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style> 