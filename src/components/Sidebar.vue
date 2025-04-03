<template>
  <div class="sidebar">
    <el-menu
      :default-active="$route.path"
      class="sidebar-menu"
      :collapse="isCollapse"
      router
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF">
      
      <el-menu-item index="/dashboard">
        <i class="el-icon-s-home"></i>
        <span slot="title">控制台</span>
      </el-menu-item>

      <!-- 生产监控子菜单 -->
      <el-submenu index="production">
        <template slot="title">
          <i class="el-icon-s-platform"></i>
          <span>生产监控</span>
        </template>
        
        <el-menu-item index="/production">
          <i class="el-icon-video-play"></i>
          <span>生产线模拟</span>
        </el-menu-item>

        <el-menu-item index="/process-animation">
          <i class="el-icon-film"></i>
          <span>溶胶蘸胶过程</span>
        </el-menu-item>

        <el-menu-item index="/defect-detection">
          <i class="el-icon-warning"></i>
          <span>缺陷检测</span>
        </el-menu-item>
      </el-submenu>

      <el-menu-item index="/equipment">
        <i class="el-icon-s-cooperation"></i>
        <span slot="title">设备监控</span>
      </el-menu-item>

      <el-menu-item index="/video">
        <i class="el-icon-video-camera"></i>
        <span slot="title">视频监控</span>
      </el-menu-item>

      <el-menu-item index="/personnel">
        <i class="el-icon-user"></i>
        <span slot="title">人员管理</span>
      </el-menu-item>

      <el-menu-item index="/profile">
        <i class="el-icon-s-custom"></i>
        <span slot="title">个人信息</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  data() {
    return {
      isCollapse: false
    }
  }
}
</script>

<style scoped>
.sidebar {
  height: 100%;
  background-color: #304156;
}

.sidebar-menu {
  height: 100%;
  border-right: none;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 200px;
}

/* 添加图标和文字的间距 */
.el-menu-item [class^="el-icon-"] {
  margin-right: 5px;
  width: 24px;
  text-align: center;
  font-size: 18px;
  vertical-align: middle;
}

/* 子菜单图标样式 */
.el-submenu [class^="el-icon-"] {
  vertical-align: middle;
  margin-right: 5px;
  width: 24px;
  text-align: center;
  font-size: 18px;
}

/* 激活菜单项的样式 */
.el-menu-item.is-active {
  background-color: #263445 !important;
}
</style> 