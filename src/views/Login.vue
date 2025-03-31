<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>胶囊模具数字化检测系统</h2>
      </div>
      <div class="login-tabs">
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'login' }" 
          @click="activeTab = 'login'"
        >
          登录
        </div>
        <div 
          class="tab-item" 
          :class="{ active: activeTab === 'register' }" 
          @click="activeTab = 'register'"
        >
          注册
        </div>
      </div>
      
      <!-- 登录表单 -->
      <el-form v-if="activeTab === 'login'" ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            prefix-icon="el-icon-user" 
            placeholder="用户名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            prefix-icon="el-icon-lock" 
            placeholder="密码" 
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
          <span class="forget-password">忘记密码?</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" class="login-btn">登录</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 注册表单 -->
      <el-form v-else ref="registerForm" :model="registerForm" :rules="registerRules" class="register-form">
        <el-form-item prop="username">
          <el-input 
            v-model="registerForm.username" 
            prefix-icon="el-icon-user" 
            placeholder="用户名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="realname">
          <el-input 
            v-model="registerForm.realname" 
            prefix-icon="el-icon-s-custom" 
            placeholder="真实姓名"
          ></el-input>
        </el-form-item>
        <el-form-item prop="department">
          <el-select v-model="registerForm.department" placeholder="选择部门" style="width: 100%">
            <el-option
              v-for="dept in departments"
              :key="dept.value"
              :label="dept.label"
              :value="dept.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="registerForm.password" 
            prefix-icon="el-icon-lock" 
            placeholder="密码" 
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            prefix-icon="el-icon-lock" 
            placeholder="确认密码" 
            type="password"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleRegister" class="login-btn">注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    // 密码确认验证
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'));
      } else {
        callback();
      }
    };
    
    return {
      activeTab: 'login',
      loading: false,
      loginForm: {
        username: '',
        password: '',
        remember: false
      },
      registerForm: {
        username: '',
        realname: '',
        department: '',
        password: '',
        confirmPassword: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur' }
        ]
      },
      registerRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        realname: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少为 6 个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]
      },
      departments: [
        { value: '技术部', label: '技术部' },
        { value: '生产部', label: '生产部' },
        { value: '质检部', label: '质检部' },
        { value: '物流部', label: '物流部' },
        { value: '研发部', label: '研发部' }
      ]
    };
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true;
          
          // 模拟登录请求，实际项目中应调用API
          setTimeout(() => {
            // 创建一个用户对象
            const user = {
              id: 1,
              username: this.loginForm.username,
              realname: '测试用户',
              department: '技术部',
              avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
              role: 'admin',
              token: 'mock-token-' + Date.now()
            };
            
            // 存储到Vuex和localStorage
            this.$store.commit('setUser', user);
            if (this.loginForm.remember) {
              localStorage.setItem('user', JSON.stringify(user));
            }
            
            this.loading = false;
            this.$message.success('登录成功');
            this.$router.push('/dashboard');
          }, 1000);
        }
      });
    },
    handleRegister() {
      this.$refs.registerForm.validate(valid => {
        if (valid) {
          this.loading = true;
          
          // 模拟注册请求，实际项目中应调用API
          setTimeout(() => {
            // 创建一个用户对象
            const user = {
              id: Date.now(),
              username: this.registerForm.username,
              realname: this.registerForm.realname,
              department: this.registerForm.department,
              avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
              role: 'user',
              token: 'mock-token-' + Date.now()
            };
            
            // 存储到Vuex和localStorage
            this.$store.commit('setUser', user);
            localStorage.setItem('user', JSON.stringify(user));
            
            this.loading = false;
            this.$message.success('注册成功，已自动登录');
            this.$router.push('/dashboard');
          }, 1000);
        }
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #05173b 0%, #0b2a5e 100%);
  background-size: 100% 100%;
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../assets/bg-pattern.png');
  background-repeat: repeat;
  background-size: 20px;
  opacity: 0.05;
  z-index: 0;
}

.login-box {
  width: 400px;
  background-color: rgba(10, 26, 59, 0.8);
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  padding: 30px;
  z-index: 1;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(25, 186, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #fff;
  font-size: 24px;
  font-weight: 500;
  margin: 0;
}

.login-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(25, 186, 255, 0.2);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 10px 0;
  color: #919bb0;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.tab-item:hover {
  color: #fff;
}

.tab-item.active {
  color: #fff;
  border-bottom: 2px solid #1890ff;
}

.login-form, .register-form {
  margin-top: 20px;
}

.login-btn {
  width: 100%;
  height: 42px;
  font-size: 16px;
}

.forget-password {
  float: right;
  color: #1890ff;
  cursor: pointer;
}

::v-deep .el-input__inner {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(25, 186, 255, 0.3);
  color: #fff;
  height: 42px;
}

::v-deep .el-input__inner:focus {
  border-color: #1890ff;
}

::v-deep .el-input__prefix {
  color: #919bb0;
}

::v-deep .el-checkbox__label {
  color: #fff;
}

::v-deep .el-form-item__error {
  color: #ff4d4f;
}

::v-deep .el-select .el-input.is-focus .el-input__inner {
  border-color: #1890ff;
}

::v-deep .el-select-dropdown {
  background-color: #0a1a3b;
  border: 1px solid rgba(25, 186, 255, 0.3);
}

::v-deep .el-select-dropdown__item {
  color: #fff;
}

::v-deep .el-select-dropdown__item.hover, 
::v-deep .el-select-dropdown__item:hover {
  background-color: rgba(25, 186, 255, 0.1);
}

::v-deep .el-select-dropdown__item.selected {
  color: #1890ff;
  background-color: rgba(25, 186, 255, 0.1);
}
</style> 