<template>
  <div class="nav-menu">
    <div class="logo">
      <img src="../assets/logo.png" alt="Logo" class="logo-img" v-if="logoSrc">
      <div class="logo-text">胶囊模具数字化检测系统</div>
    </div>
    <el-menu
      mode="horizontal"
      background-color="transparent"
      text-color="#fff"
      active-text-color="#409EFF"
      :default-active="activeIndex"
      router
      class="menu"
    >
      <el-menu-item index="/dashboard">安全生产监管平台</el-menu-item>
      <el-menu-item index="/equipment">设备监测大屏</el-menu-item>
      <el-menu-item index="/video">视频监控平台</el-menu-item>
      <el-menu-item index="/personnel">人员在岗管理</el-menu-item>
      <el-menu-item index="/process-animation">溶胶蘸胶过程动画</el-menu-item>
      <el-menu-item index="/defect-detection">模具缺陷检测</el-menu-item>
    </el-menu>
    <div class="user-info" v-if="user">
      <span class="username">{{ user.realname }}</span>
      <el-dropdown trigger="click" @command="handleCommand">
        <span class="el-dropdown-link">
          <el-avatar :size="32" :src="user.avatar"></el-avatar>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="profile">
            <i class="el-icon-user"></i> 个人信息
          </el-dropdown-item>
          <el-dropdown-item command="changePassword">
            <i class="el-icon-key"></i> 修改密码
          </el-dropdown-item>
          <el-dropdown-item divided command="logout">
            <i class="el-icon-switch-button"></i> 退出登录
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'NavMenu',
  props: {
    logoSrc: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      activeIndex: '/dashboard'
    }
  },
  computed: {
    ...mapState(['user'])
  },
  mounted() {
    this.activeIndex = this.$route.path
  },
  watch: {
    $route(to) {
      this.activeIndex = to.path
    }
  },
  methods: {
    handleCommand(command) {
      switch(command) {
        case 'profile':
          this.$router.push('/profile')
          break
        case 'changePassword':
          // 暂未实现，可以打开一个修改密码的对话框
          this.$message.info('修改密码功能暂未实现')
          break
        case 'logout':
          this.$confirm('确认退出登录?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            // 调用store中的logout action
            this.$store.dispatch('logout').then(() => {
              this.$message.success('退出登录成功')
              this.$router.push('/login')
            })
          }).catch(() => {})
          break
      }
    }
  }
}
</script>

<style scoped>
.nav-menu {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: rgba(0, 10, 50, 0.8);
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  height: 40px;
  margin-right: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #fff;
}

.menu {
  border-bottom: none;
}

.user-info {
  display: flex;
  align-items: center;
}

.username {
  color: #fff;
  margin-right: 10px;
}

.el-dropdown-link {
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
}

::v-deep .el-menu--horizontal > .el-menu-item {
  height: 60px;
  line-height: 60px;
}

::v-deep .el-menu--horizontal > .el-menu-item.is-active {
  border-bottom: 2px solid #409EFF;
  background-color: rgba(64, 158, 255, 0.1) !important;
}

::v-deep .el-menu--horizontal > .el-menu-item:hover {
  background-color: rgba(64, 158, 255, 0.1) !important;
}
</style> 