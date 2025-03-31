<template>
  <div class="personnel">
    <div class="content-container">
      <div class="left-panel">
        <!-- 人员在岗状态 -->
        <data-card title="人员在岗状态">
          <div class="attendance-status">
            <div class="status-item">
              <div class="status-icon on-duty">{{ personnelData.onDuty }}</div>
              <div class="status-name">在岗人数</div>
            </div>
            <div class="status-item">
              <div class="status-icon off-duty">{{ personnelData.offDuty }}</div>
              <div class="status-name">离岗人数</div>
            </div>
            <div class="status-item">
              <div class="status-icon total">{{ personnelData.total }}</div>
              <div class="status-name">总人数</div>
            </div>
          </div>
        </data-card>
        
        <!-- 人员考勤率 -->
        <data-card title="人员考勤率">
          <div class="attendance-chart" ref="attendanceChart"></div>
        </data-card>
        
        <!-- 胶囊模具检测 -->
        <data-card title="胶囊模具检测">
          <div class="inspection-chart" ref="inspectionChart"></div>
        </data-card>
      </div>
      
      <div class="center-panel">
        <!-- 人员实时监控 -->
        <data-card title="人员实时监控">
          <div class="monitor-container">
            <div class="camera-grid">
              <div v-for="n in 4" :key="n" class="camera-item">
                <div class="camera-frame">
                  <img src="@/assets/person-detection.jpg" alt="监控画面" class="camera-image">
                  <div class="camera-overlay">
                    <div class="camera-placeholder">摄像头 {{ n }}</div>
                    <div class="detection-box">
                      <div class="person-box">人员</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </data-card>
        
        <!-- 人员操作记录 -->
        <data-card title="人员操作记录">
          <div class="operation-records">
            <el-table :data="operationLogs" style="width: 100%; background-color: transparent;" :header-cell-style="headerStyle">
              <el-table-column prop="time" label="操作时间" width="180"></el-table-column>
              <el-table-column prop="name" label="操作人员" width="120"></el-table-column>
              <el-table-column prop="operation" label="操作内容"></el-table-column>
              <el-table-column prop="result" label="操作结果" width="100">
                <template slot-scope="scope">
                  <span :style="{color: scope.row.result === '成功' ? '#52c41a' : '#f5222d'}">{{ scope.row.result }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </data-card>
      </div>
      
      <div class="right-panel">
        <!-- 胶囊模具数字化检测 -->
        <data-card title="胶囊模具数字化检测">
          <div class="mold-inspection">
            <div class="inspection-header">
              <div class="inspection-data">
                <div class="inspection-count">
                  <div class="count-label">今日检测数</div>
                  <div class="count-value">256</div>
                </div>
                <div class="inspection-rate">
                  <div class="rate-label">合格率</div>
                  <div class="rate-value">98.4%</div>
                </div>
              </div>
            </div>
            <div class="inspection-content">
              <div class="mold-camera" ref="moldCamera">
                <div class="mold-placeholder">模具检测摄像头</div>
                <div class="mold-detection">
                  <div class="mold-box good">合格</div>
                </div>
              </div>
              <div class="inspection-params">
                <div class="param-item">
                  <div class="param-name">尺寸精度</div>
                  <div class="param-value good">正常</div>
                </div>
                <div class="param-item">
                  <div class="param-name">表面光滑度</div>
                  <div class="param-value good">正常</div>
                </div>
                <div class="param-item">
                  <div class="param-name">结构完整性</div>
                  <div class="param-value good">正常</div>
                </div>
                <div class="param-item">
                  <div class="param-name">材质硬度</div>
                  <div class="param-value good">正常</div>
                </div>
              </div>
            </div>
          </div>
        </data-card>
        
        <!-- 部门人员分布 -->
        <data-card title="部门人员分布">
          <div class="department-distribution" ref="departmentDistChart"></div>
        </data-card>
      </div>
    </div>
  </div>
</template>

<script>
import DataCard from '@/components/DataCard.vue'
import { mapState } from 'vuex'

export default {
  name: 'Personnel',
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
      operationLogs: [
        {
          time: '2023-07-23 10:15:32',
          name: '张三',
          operation: '胶囊模具检测',
          result: '成功'
        },
        {
          time: '2023-07-23 09:42:18',
          name: '李四',
          operation: '设备维护',
          result: '成功'
        },
        {
          time: '2023-07-23 09:30:05',
          name: '王五',
          operation: '原料检验',
          result: '成功'
        },
        {
          time: '2023-07-23 08:55:47',
          name: '赵六',
          operation: '安全巡检',
          result: '成功'
        },
        {
          time: '2023-07-22 17:40:12',
          name: '钱七',
          operation: '模具清洗',
          result: '成功'
        }
      ]
    }
  },
  computed: {
    ...mapState(['personnelData'])
  },
  methods: {
    initAttendanceChart() {
      const chartDom = this.$refs.attendanceChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          textStyle: {
            color: '#fff'
          }
        },
        series: [
          {
            name: '考勤状态',
            type: 'pie',
            radius: '70%',
            data: [
              { value: 82, name: '正常' },
              { value: 12, name: '迟到' },
              { value: 6, name: '请假' }
            ],
            color: ['#52c41a', '#faad14', '#1890ff'],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
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
    initInspectionChart() {
      const chartDom = this.$refs.inspectionChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: [
          {
            type: 'category',
            data: ['7-18', '7-19', '7-20', '7-21', '7-22', '7-23'],
            axisTick: {
              alignWithLabel: true
            },
            axisLine: {
              lineStyle: {
                color: '#fff'
              }
            }
          }
        ],
        yAxis: [
          {
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
          }
        ],
        series: [
          {
            name: '检测数量',
            type: 'bar',
            barWidth: '60%',
            data: [210, 232, 201, 254, 190, 256],
            itemStyle: {
              color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#83bff6' },
                { offset: 0.5, color: '#188df0' },
                { offset: 1, color: '#188df0' }
              ])
            }
          }
        ]
      }
      
      myChart.setOption(option)
      window.addEventListener('resize', () => {
        myChart.resize()
      })
    },
    initDepartmentDistChart() {
      const chartDom = this.$refs.departmentDistChart
      const myChart = this.$echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          bottom: '0%',
          left: 'center',
          textStyle: {
            color: '#fff'
          }
        },
        series: [
          {
            name: '部门分布',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#0a1a3b',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold',
                formatter: '{b}: {c}人'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 15, name: '技术部' },
              { value: 22, name: '生产部' },
              { value: 10, name: '质检部' },
              { value: 8, name: '物流部' },
              { value: 12, name: '研发部' }
            ],
            color: ['#4992ff', '#7cffb2', '#fddd60', '#ff6e76', '#58d9f9']
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
      this.initAttendanceChart()
      this.initInspectionChart()
      this.initDepartmentDistChart()
    })
  }
}
</script>

<style scoped>
.personnel {
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
  height: calc(100% - 20px);
}

.left-panel, .right-panel {
  width: 25%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.center-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
  height: 100%;
}

.left-panel > div, .right-panel > div {
  height: calc(50% - 5px);
}

.center-panel > div:first-child {
  height: 50%;
  max-height: 50%;
  overflow: hidden;
}

.center-panel > div:last-child {
  height: 50%;
  max-height: 50%;
  overflow: auto;
}

.attendance-status {
  height: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.status-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}

.status-icon.on-duty {
  background-color: #52c41a;
  color: #fff;
}

.status-icon.off-duty {
  background-color: #ff4d4f;
  color: #fff;
}

.status-icon.total {
  background-color: #1890ff;
  color: #fff;
}

.status-name {
  font-size: 16px;
  color: #fff;
}

.attendance-chart, .inspection-chart, .department-distribution {
  width: 100%;
  height: 100%;
}

.monitor-container {
  width: 100%;
  height: 100%;
  padding: 10px;
  overflow: hidden;
  box-sizing: border-box;
}

.camera-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 10px;
  width: 100%;
  height: 100%;
  max-height: 100%;
}

.camera-item {
  border: 1px solid rgba(25, 186, 255, 0.3);
  border-radius: 4px;
  overflow: hidden;
  height: 100%;
  max-height: 100%;
}

.camera-frame {
  width: 100%;
  height: 100%;
  position: relative;
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.camera-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.8;
}

.camera-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 10px;
  box-sizing: border-box;
  z-index: 2;
}

.camera-placeholder {
  align-self: flex-start;
  color: rgba(255, 255, 255, 0.8);
  background-color: rgba(0, 0, 0, 0.5);
  padding: 2px 6px;
  border-radius: 2px;
}

.detection-box {
  align-self: flex-start;
  display: flex;
}

.person-box {
  background-color: rgba(82, 196, 26, 0.7);
  padding: 3px 8px;
  border-radius: 2px;
  color: white;
  font-size: 12px;
}

.operation-records {
  height: 100%;
  overflow-y: auto;
}

.mold-inspection {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.inspection-header {
  padding: 10px 0;
}

.inspection-data {
  display: flex;
  justify-content: space-around;
}

.inspection-count, .inspection-rate {
  text-align: center;
}

.count-label, .rate-label {
  font-size: 14px;
  color: #999;
  margin-bottom: 5px;
}

.count-value, .rate-value {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
}

.inspection-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mold-camera {
  height: 150px;
  background-color: #000;
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.mold-placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.mold-detection {
  position: absolute;
  bottom: 10px;
  right: 10px;
}

.mold-box {
  padding: 3px 8px;
  border-radius: 2px;
  color: white;
  font-size: 12px;
}

.mold-box.good {
  background-color: rgba(82, 196, 26, 0.7);
}

.mold-box.bad {
  background-color: rgba(255, 77, 79, 0.7);
}

.inspection-params {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 10px;
}

.param-item {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.param-name {
  font-size: 14px;
  color: #999;
  margin-bottom: 5px;
}

.param-value {
  font-size: 16px;
  font-weight: bold;
}

.param-value.good {
  color: #52c41a;
}

.param-value.bad {
  color: #ff4d4f;
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