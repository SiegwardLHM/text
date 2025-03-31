<template>
  <div id="app">
    <nav-menu v-if="isAuthenticated && !isLoginPage"></nav-menu>
    <div class="content-container" :class="{ 'no-nav': !isAuthenticated || isLoginPage }">
      <router-view/>
    </div>
  </div>
</template>

<script>
import NavMenu from '@/components/NavMenu.vue'
import { mapState } from 'vuex'

export default {
  components: {
    NavMenu
  },
  computed: {
    ...mapState(['user']),
    isAuthenticated() {
      return !!this.user
    },
    isLoginPage() {
      return this.$route.path === '/login'
    }
  }
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

#app {
  font-family: 'Microsoft YaHei', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  width: 100%;
  background-color: #0a1a3b;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.content-container {
  flex: 1;
  overflow: hidden;
}

.content-container.no-nav {
  height: 100%;
}
</style> 