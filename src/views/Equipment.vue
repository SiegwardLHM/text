<template>
  <div class="equipment">
    <div class="content-container">
      <div class="left-panel">
        <!-- 设备运行状况 -->
        <data-card title="设备运行次数">
          <div class="operations-chart" ref="operationsChart"></div>
        </data-card>
        
        <!-- 设备性能指标 -->
        <data-card title="硬件供给统计">
          <div class="radar-chart" ref="radarChart"></div>
        </data-card>
        
        <!-- 设备维护记录 -->
        <data-card title="设备维护次数">
          <div class="maintenance-chart" ref="maintenanceChart"></div>
        </data-card>
      </div>
      
      <div class="center-panel">
        <!-- 设备月度巡检计划 -->
        <data-card title="设备月度巡检计划">
          <div class="plan-container">
            <div class="plan-header">
              <div class="plan-title">完成/计划</div>
              <div class="plan-value">{{ equipmentData.completed }}/{{ equipmentData.planTotal }}</div>
            </div>
            <div class="plan-progress">
              <div class="uncompleted">未完成: {{ equipmentData.uncompleted }}</div>
              <div class="completed">完成率: {{ equipmentData.completionRate }}</div>
            </div>
          </div>
        </data-card>
        
        <!-- 长期运行情况 -->
        <data-card title="长期运行情况">
          <div class="long-term">
            <div class="long-term-chart" ref="longTermChart"></div>
            <div class="long-term-value">{{ longTermRate }}</div>
          </div>
        </data-card>
        
        <!-- 设备报警信息 -->
        <data-card title="设备报警信息">
          <div class="equipment-alert">
            <el-table :data="alertEquipments" style="width: 100%; background-color: transparent;" :header-cell-style="headerStyle">
              <el-table-column prop="reportTime" label="报警时间" width="120"></el-table-column>
              <el-table-column prop="name" label="设备名称" width="150"></el-table-column>
              <el-table-column prop="code" label="设备编号" width="120"></el-table-column>
              <el-table-column prop="person" label="值班人员" width="100"></el-table-column>
              <el-table-column prop="count" label="数量" width="80"></el-table-column>
              <el-table-column prop="status" label="已解决" width="100">
                <template slot-scope="scope">
                  <span style="color: #52c41a;">{{ scope.row.status }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </data-card>
      </div>
      
      <div class="right-panel">
        <!-- 设备状态 -->
        <data-card title="设备状态">
          <div class="equipment-status">
            <el-table :data="normalEquipments" style="width: 100%; background-color: transparent;" :header-cell-style="headerStyle">
              <el-table-column prop="code" label="设备编号" width="120"></el-table-column>
              <el-table-column prop="status" label="状态情况" width="80">
                <template slot-scope="scope">
                  <span :style="{color: scope.row.status === '正常' ? '#52c41a' : '#f5222d'}">{{ scope.row.status }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="runtime" label="持续时间" width="200"></el-table-column>
            </el-table>
          </div>
        </data-card>
      </div>
    </div>
  </div>
</template>

<script>
import DataCard from '@/components/DataCard.vue'
import { mapState } from 'vuex'

export default {
  name: 'Equipment',
  components: {
    DataCard
  },
  data() {
    return {
      headerStyle: {
        color: '#fff',
        backgroundColor: 'rgba(0, 10, 50, 0.5)',
        borderColor: 'rgba(25, 186, 255, 0.1)'
      },
      longTermRate: '9/11'
    }
  },
  computed: {
    ...mapState({
      equipmentData: state => state.equipmentData,
      alertEquipments: state => state.equipmentData.abnormalEquipments,
      normalEquipments: state => state.equipmentData.normalEquipments
    })
  },
  methods: {
    initOperationsChart() {
      const chartDom = this.$refs.operationsChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['10.3', '10.4', '10.5', '10.6', '10.7', '10.8'],
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
            data: [85, 65, 78, 45, 70, 90],
            type: 'line',
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#50d890'
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#50d890'
            },
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
            }
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initRadarChart() {
      const chartDom = this.$refs.radarChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        color: ['#67F9D8', '#FFE434', '#56A3F1', '#FF917C'],
        radar: {
          indicator: [
            { name: '设备', max: 100 },
            { name: '硬件', max: 100 },
            { name: '耗材', max: 100 },
            { name: '人力', max: 100 },
            { name: '服务', max: 100 }
          ],
          radius: 80,
          splitNumber: 4,
          axisName: {
            color: '#fff'
          },
          splitArea: {
            areaStyle: {
              color: ['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.1)']
            }
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          }
        },
        series: [
          {
            name: '预算 vs 开销',
            type: 'radar',
            data: [
              {
                value: [85, 65, 78, 90, 70],
                name: '开发'
              },
              {
                value: [95, 80, 60, 80, 85],
                name: '接收'
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
    initMaintenanceChart() {
      const chartDom = this.$refs.maintenanceChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['1月', '2月', '3月', '4月', '5月', '6月'],
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
            data: [25, 65, 40, 80, 35, 95],
            type: 'line',
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#4992ff'
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#4992ff'
            },
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
                    color: 'rgba(73, 146, 255, 0.6)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(73, 146, 255, 0)'
                  }
                ]
              }
            }
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initLongTermChart() {
      const chartDom = this.$refs.longTermChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        series: [
          {
            type: 'pie',
            radius: ['70%', '90%'],
            avoidLabelOverlap: false,
            startAngle: 225,
            color: ['#4992ff', 'rgba(255, 255, 255, 0.2)'],
            hoverAnimation: false,
            label: {
              show: false
            },
            data: [
              { value: 9, name: '完成' },
              { value: 2, name: '未完成' }
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
      this.initOperationsChart()
      this.initRadarChart()
      this.initMaintenanceChart()
      this.initLongTermChart()
    })
  }
}
</script>

<style scoped>
.equipment {
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

.left-panel, .right-panel {
  width: 30%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.center-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.left-panel > div, .right-panel > div {
  height: calc(33.33% - 7px);
}

.center-panel > div:first-child {
  height: 25%;
}

.center-panel > div:nth-child(2) {
  height: 15%;
}

.center-panel > div:last-child {
  flex: 1;
}

.operations-chart, .radar-chart, .maintenance-chart, .long-term-chart {
  width: 100%;
  height: 100%;
}

.plan-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.plan-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.plan-title {
  font-size: 16px;
  color: #fff;
  margin-bottom: 10px;
}

.plan-value {
  font-size: 60px;
  font-weight: bold;
  color: #fff;
}

.plan-progress {
  display: flex;
  width: 80%;
  justify-content: space-between;
}

.uncompleted {
  color: #f5222d;
  font-size: 18px;
}

.completed {
  color: #52c41a;
  font-size: 18px;
}

.long-term {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.long-term-chart {
  width: 100%;
  height: 100%;
}

.long-term-value {
  position: absolute;
  font-size: 30px;
  font-weight: bold;
  color: #fff;
}

.equipment-alert, .equipment-status {
  height: 100%;
  overflow-y: auto;
}

::v-deep .el-table, 
::v-deep .el-table tr, 
::v-deep .el-table th, 
::v-deep .el-table td {
  background-color: transparent;
  color: #fff;
  border-color: rgba(25, 186, 255, 0.1);
}

::v-deep .el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: rgba(25, 186, 255, 0.1);
}

::v-deep .el-table::before {
  display: none;
}
</style> 