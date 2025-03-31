import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex) 

export default new Vuex.Store({
  state: {
    // 用户信息
    user: JSON.parse(localStorage.getItem('user')) || null,
    
    // 安全生产监管数据
    safetyData: {
      productionIndex: 50,
      qualityIndex: 32,
      riskIndex: 73,
      environmentIndex: 36,
      energyIndex: 58
    },
    // 警报信息
    alertList: [
      { 
        name: '高温预警',
        time: '2023-07-22 09:13:00',
        location: 'ABC车间南区C25'
      },
      { 
        name: '设备压力异常',
        time: '2023-07-22 10:08:00',
        location: 'XYZ车间工业车间'
      },
      { 
        name: '启动超过预警',
        time: '2023-07-22 11:45:00',
        location: '江门生产线18号区'
      },
      { 
        name: '烟雾浓度预警',
        time: '2023-07-22 13:30:00',
        location: 'DEF车间工厂区域'
      },
      { 
        name: '火焰检测预警',
        time: '2023-07-22 14:15:00',
        location: 'GHI车间'
      }
    ],
    // 设备巡检数据
    equipmentData: {
      planTotal: 36,
      completed: 27,
      uncompleted: 15,
      completionRate: '75%',
      abnormalEquipments: [
        {
          reportTime: '2023-7-06',
          name: '监控摄像头',
          code: 'XS0165420',
          person: '李建',
          count: 5,
          status: '80%'
        }
      ],
      normalEquipments: [
        {
          code: 'XS0163420',
          status: '正常',
          runtime: '671天8时72分20秒'
        },
        {
          code: 'XQ1630217',
          status: '正常',
          runtime: '243天18时13分38秒'
        },
        {
          code: 'XP2105457',
          status: '正常',
          runtime: '330天8时7分26秒'
        }
      ]
    },
    // 人员在岗数据
    personnelData: {
      onDuty: 9,
      offDuty: 2,
      total: 11,
      departments: ['技术部', '生产部', '质检部', '物流部', '研发部']
    }
  },
  mutations: {
    // 设置用户信息
    setUser(state, user) {
      state.user = user
    },
    
    updateSafetyData(state, payload) {
      state.safetyData = {...state.safetyData, ...payload}
    },
    updateEquipmentData(state, payload) {
      state.equipmentData = {...state.equipmentData, ...payload}
    },
    updatePersonnelData(state, payload) {
      state.personnelData = {...state.personnelData, ...payload}
    }
  },
  actions: {
    // 登录操作
    login({ commit }, userInfo) {
      return new Promise((resolve) => {
        // 模拟API请求
        setTimeout(() => {
          // 创建用户对象
          const user = {
            id: 1,
            username: userInfo.username,
            realname: '测试用户',
            department: '技术部',
            avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
            role: 'admin',
            token: 'mock-token-' + Date.now()
          }
          
          // 提交到state
          commit('setUser', user)
          
          // 存储到localStorage
          if(userInfo.remember) {
            localStorage.setItem('user', JSON.stringify(user))
          }
          
          resolve(user)
        }, 1000)
      })
    },
    
    // 注册操作
    register({ commit }, userInfo) {
      return new Promise((resolve) => {
        // 模拟API请求
        setTimeout(() => {
          // 创建用户对象
          const user = {
            id: Date.now(),
            username: userInfo.username,
            realname: userInfo.realname,
            department: userInfo.department,
            avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
            role: 'user',
            token: 'mock-token-' + Date.now()
          }
          
          // 提交到state
          commit('setUser', user)
          
          // 存储到localStorage
          localStorage.setItem('user', JSON.stringify(user))
          
          resolve(user)
        }, 1000)
      })
    },
    
    // 退出登录
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('setUser', null)
        localStorage.removeItem('user')
        resolve()
      })
    }
  },
  modules: {
  }
}) 