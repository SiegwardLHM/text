<template>
  <div class="dashboard">
    <div class="content-container">
      <div class="left-panel">
        <!-- 企业安全生产状况 -->
        <data-card title="企业安全生产人员行为监控" :update-time="currentDate">
          <div class="bubble-chart" ref="bubbleChart"></div>
        </data-card>
        
        <!-- 企业各部门生产安全行为统计 -->
        <data-card title="企业各部门生产安全行为统计" :update-time="currentDate">
          <div class="department-chart" ref="departmentChart"></div>
        </data-card>
        
        <!-- 设备数据趋势 -->
        <data-card title="安全设备预警等级" :update-time="currentDate">
          <div class="scatter-chart" ref="scatterChart"></div>
        </data-card>
      </div>
      
      <div class="center-panel">
        <!-- 生产安全指数 -->
        <div class="indicator-container">
          <div class="indicator-box">
            <h3>平均生产安全指数值</h3>
            <div class="indicator-value" :style="{color: getColorByValue(safetyData.productionIndex)}">
              {{ safetyData.productionIndex }}
            </div>
            <div class="indicator-trend">
              较上月：<span :class="{'up': true}">↑ 2%</span>
            </div>
          </div>
          <div class="indicator-box">
            <h3>平均产品质量指数值</h3>
            <div class="indicator-value" :style="{color: getColorByValue(safetyData.qualityIndex)}">
              {{ safetyData.qualityIndex }}
            </div>
            <div class="indicator-trend">
              较上月：<span :class="{'down': true}">↓ 3%</span>
            </div>
          </div>
        </div>
        
        <!-- 监测风险趋势图 -->
        <div class="indicator-container">
          <div class="indicator-box">
            <h3>安全生产风险监测值</h3>
            <div class="indicator-value" :style="{color: getColorByValue(safetyData.riskIndex, true)}">
              {{ safetyData.riskIndex }}
            </div>
            <div class="indicator-trend">
              较上月：<span :class="{'up': true, 'bad': true}">↑ 5%</span>
            </div>
          </div>
          <div class="indicator-box">
            <h3>生产环境监测值</h3>
            <div class="indicator-value" :style="{color: getColorByValue(safetyData.environmentIndex)}">
              {{ safetyData.environmentIndex }}
            </div>
            <div class="indicator-trend">
              较上月：<span :class="{'down': true}">↓ 2%</span>
            </div>
          </div>
        </div>
        
        <!-- 能源监测 -->
        <div class="energy-container">
          <div class="indicator-box wider">
            <h3>安全生产能源监测值</h3>
            <div class="indicator-value" :style="{color: getColorByValue(safetyData.energyIndex)}">
              {{ safetyData.energyIndex }}
            </div>
            <div class="indicator-trend">
              较上月：<span :class="{'down': true}">↓ 2%</span>
            </div>
          </div>
        </div>
        
        <!-- 质量管理框架图 -->
        <div class="quality-framework">
          <data-card title="质量管理框架图">
            <div class="framework-chart" ref="frameworkChart"></div>
          </data-card>
        </div>
      </div>
      
      <div class="right-panel">
        <!-- 预警信息 -->
        <data-card title="预警信息分布">
          <div class="alert-list">
            <div v-for="(alert, index) in alertList" :key="index" class="alert-item">
              <div class="alert-dot"></div>
              <div class="alert-info">
                <div class="alert-name">预警类型：{{ alert.name }}</div>
                <div class="alert-time">预警时间：{{ alert.time }}</div>
                <div class="alert-location">预警位置：{{ alert.location }}</div>
              </div>
            </div>
          </div>
        </data-card>
        
        <!-- 能耗趋势 -->
        <data-card title="周能耗趋势变化" :update-time="currentDate">
          <div class="energy-chart" ref="energyChart"></div>
        </data-card>
        
        <!-- 指标统计 -->
        <data-card title="安全生产能力指标体系图" :update-time="currentDate">
          <div class="capacity-chart" ref="capacityChart"></div>
        </data-card>
      </div>
    </div>
  </div>
</template>

<script>
import DataCard from '@/components/DataCard.vue'
import { mapState } from 'vuex'

export default {
  name: 'Dashboard',
  components: {
    DataCard
  },
  data() {
    return {
      currentDate: '2025-03-27'
    }
  },
  computed: {
    ...mapState(['safetyData', 'alertList'])
  },
  methods: {
    getColorByValue(value, isReverse = false) {
      if (!isReverse) {
        if (value >= 80) return '#52c41a'
        if (value >= 60) return '#fadb14'
        return '#f5222d'
      } else {
        if (value >= 80) return '#f5222d'
        if (value >= 60) return '#fadb14'
        return '#52c41a'
      }
    },
    initBubbleChart() {
      const chartDom = this.$refs.bubbleChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        grid: {
          left: '10%',
          right: '10%',
          top: '10%',
          bottom: '10%'
        },
        tooltip: {
          trigger: 'item'
        },
        series: [{
          type: 'graph',
          layout: 'force',
          symbolSize: 50,
          roam: true,
          label: {
            show: true
          },
          force: {
            repulsion: 200,
            edgeLength: 100
          },
          data: [
            {
              name: '安全帽',
              value: 60,
              itemStyle: {
                color: '#4992ff'
              }
            },
            {
              name: '反光衣',
              value: 70,
              itemStyle: {
                color: '#7cffb2'
              }
            },
            {
              name: '工具',
              value: 40,
              itemStyle: {
                color: '#fddd60'
              }
            },
            {
              name: '操作',
              value: 80,
              itemStyle: {
                color: '#ff6e76'
              }
            },
            {
              name: '设备',
              value: 50,
              itemStyle: {
                color: '#58d9f9'
              }
            }
          ],
          links: [
            {
              source: '安全帽',
              target: '操作'
            },
            {
              source: '反光衣',
              target: '操作'
            },
            {
              source: '工具',
              target: '操作'
            },
            {
              source: '设备',
              target: '操作'
            }
          ]
        }]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initDepartmentChart() {
      const chartDom = this.$refs.departmentChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        color: ['#4992ff', '#7cffb2', '#fddd60', '#ff6e76', '#58d9f9'],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '15%',
          containLabel: true
        },
        legend: {
          data: ['安全帽', '反光衣', '安全用具', '操作规范', '设备检查'],
          textStyle: {
            color: '#fff'
          }
        },
        xAxis: {
          type: 'category',
          data: ['生产部', '质检部', '物流部', '研发部', '安全部'],
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: [
          {
            name: '安全帽',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            data: [320, 302, 301, 334, 390]
          },
          {
            name: '反光衣',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            data: [120, 132, 101, 134, 90]
          },
          {
            name: '安全用具',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            data: [220, 182, 191, 234, 290]
          },
          {
            name: '操作规范',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            data: [150, 212, 201, 154, 190]
          },
          {
            name: '设备检查',
            type: 'bar',
            stack: 'total',
            emphasis: {
              focus: 'series'
            },
            data: [820, 832, 901, 934, 1290]
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initScatterChart() {
      const chartDom = this.$refs.scatterChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        color: ['#ff6e76', '#7cffb2'],
        grid: {
          left: '5%',
          right: '5%',
          bottom: '10%',
          top: '10%',
          containLabel: true
        },
        tooltip: {
          trigger: 'item'
        },
        xAxis: {
          type: 'value',
          name: '使用寿命（千小时）',
          nameGap: 25,
          nameTextStyle: {
            color: '#fff'
          },
          max: 80,
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: '预警率（%）',
          nameTextStyle: {
            color: '#fff'
          },
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: [
          {
            name: '2020',
            type: 'scatter',
            data: [
              [10, 60],
              [20, 80],
              [30, 60],
              [40, 70],
              [50, 45],
              [60, 30],
              [70, 20]
            ],
            symbolSize: function(data) {
              return data[1] / 4
            }
          },
          {
            name: '2021',
            type: 'scatter',
            data: [
              [15, 50],
              [25, 65],
              [35, 55],
              [45, 60],
              [55, 40],
              [65, 25],
              [75, 15]
            ],
            symbolSize: function(data) {
              return data[1] / 4
            }
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initEnergyChart() {
      const chartDom = this.$refs.energyChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['7-17', '7-18', '7-19', '7-20', '7-21', '7-22', '7-23'],
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#fff'
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: [
          {
            type: 'line',
            data: [90, 110, 95, 125, 130, 180, 210],
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: 'rgba(80, 216, 144, 0.6)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(80, 216, 144, 0)'
                  }
                ]
              }
            },
            lineStyle: {
              width: 3,
              color: '#50d890'
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#50d890'
            }
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initFrameworkChart() {
      const chartDom = this.$refs.frameworkChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        color: ['#4992ff', '#7cffb2', '#fddd60', '#ff6e76', '#58d9f9'],
        tooltip: {
          trigger: 'item'
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            force: {
              repulsion: 200,
              edgeLength: 50
            },
            roam: true,
            symbolSize: 50,
            label: {
              show: true
            },
            data: [
              {
                name: '质量管理',
                symbolSize: 60,
                itemStyle: {
                  color: '#4992ff'
                }
              },
              {
                name: '生产安全',
                itemStyle: {
                  color: '#7cffb2'
                }
              },
              {
                name: '制度执行',
                itemStyle: {
                  color: '#fddd60'
                }
              },
              {
                name: '人员培训',
                itemStyle: {
                  color: '#ff6e76'
                }
              },
              {
                name: '设备管理',
                itemStyle: {
                  color: '#58d9f9'
                }
              }
            ],
            links: [
              {
                source: '质量管理',
                target: '生产安全'
              },
              {
                source: '质量管理',
                target: '制度执行'
              },
              {
                source: '质量管理',
                target: '人员培训'
              },
              {
                source: '质量管理',
                target: '设备管理'
              }
            ]
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initCapacityChart() {
      const chartDom = this.$refs.capacityChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        color: ['#4992ff', '#58d9f9'],
        series: [
          {
            name: '安全生产能力',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: true,
              formatter: '{b}: {c}%'
            },
            labelLine: {
              show: true
            },
            data: [
              { value: 65, name: '安全生产率' },
              { value: 35, name: '安全管理率' }
            ]
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initBubbleChart()
      this.initDepartmentChart()
      this.initScatterChart()
      this.initEnergyChart()
      this.initFrameworkChart()
      this.initCapacityChart()
    })
  }
}
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content-container {
  flex: 1;
  display: flex;
  padding: 10px;
  gap: 10px;
  overflow: hidden;
}

.left-panel, .center-panel, .right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
}

.left-panel > div, .right-panel > div {
  height: calc(33.33% - 7px);
}

.indicator-container, .energy-container, .quality-framework {
  height: calc(25% - 8px);
  display: flex;
  gap: 10px;
}

.indicator-box {
  flex: 1;
  border: 1px solid rgba(25, 186, 255, 0.3);
  border-radius: 4px;
  background-color: rgba(0, 10, 50, 0.3);
  box-shadow: 0 0 10px rgba(25, 186, 255, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

.indicator-box.wider {
  width: 100%;
}

.indicator-box h3 {
  margin: 0;
  font-size: 16px;
  color: #fff;
  margin-bottom: 10px;
}

.indicator-value {
  font-size: 50px;
  font-weight: bold;
  margin-bottom: 10px;
}

.indicator-trend {
  font-size: 14px;
  color: #999;
}

.up {
  color: #52c41a;
}

.down {
  color: #1890ff;
}

.up.bad {
  color: #f5222d;
}

.down.bad {
  color: #52c41a;
}

.bubble-chart, .department-chart, .scatter-chart, .energy-chart, .framework-chart, .capacity-chart {
  width: 100%;
  height: 100%;
}

.alert-list {
  height: 100%;
  overflow-y: auto;
}

.alert-item {
  display: flex;
  align-items: flex-start;
  padding: 10px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.alert-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #f5222d;
  margin-right: 10px;
  margin-top: 6px;
}

.alert-info {
  flex: 1;
}

.alert-name, .alert-time, .alert-location {
  margin-bottom: 5px;
  font-size: 14px;
  color: #fff;
}

.alert-time, .alert-location {
  color: #7eb6ff;
  font-size: 12px;
}
</style> 