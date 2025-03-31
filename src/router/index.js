import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { 
      title: '登录/注册',
      public: true // 公开路由，不需要登录
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { 
      title: '控制台',
      requiresAuth: true // 需要登录
    }
  },
  {
    path: '/equipment',
    name: 'Equipment',
    component: () => import('../views/Equipment.vue'),
    meta: { 
      title: '设备监控',
      requiresAuth: true
    }
  },
  {
    path: '/video',
    name: 'Video',
    component: () => import('../views/Video.vue'),
    meta: { 
      title: '视频监控',
      requiresAuth: true
    }
  },
  {
    path: '/personnel',
    name: 'Personnel',
    component: () => import('../views/Personnel.vue'),
    meta: { 
      title: '人员在岗管理',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { 
      title: '个人信息',
      requiresAuth: true
    }
  },
  {
    path: '/process-animation',
    name: 'ProcessAnimation',
    component: () => import('../views/ProcessAnimation.vue'),
    meta: { 
      title: '溶胶蘸胶过程动画',
      requiresAuth: true
    }
  },
  {
    path: '/defect-detection',
    name: 'DefectDetection',
    component: () => import('../views/DefectDetection.vue'),
    meta: { 
      title: '模具缺陷检测',
      requiresAuth: true
    }
  },
  {
    path: '*',
    redirect: '/dashboard'
  }
]

const router = new VueRouter({
  routes
})

// 全局路由守卫，验证是否需要登录
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 胶囊模具数字化检测系统` : '胶囊模具数字化检测系统'
  
  // 判断是否需要登录权限
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否已登录
    if (!store.state.user) {
      // 未登录，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 保存原始访问路径，登录后可以跳转回去
      })
    } else {
      // 已登录，继续
      next()
    }
  } else {
    // 不需要登录权限的页面
    next()
  }
})

export default router 