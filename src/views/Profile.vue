<template>
  <div class="profile-container">
    <div class="profile-header">
      <h2>个人信息</h2>
    </div>
    <div class="profile-content">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="profile-sidebar">
            <div class="avatar-container">
              <div class="avatar-wrapper">
                <img :src="user.avatar" alt="用户头像" class="user-avatar">
                <div class="avatar-overlay">
                  <i class="el-icon-camera"></i>
                </div>
              </div>
              <div class="user-info">
                <div class="username">{{ user.realname }}</div>
                <div class="role">{{ user.role === 'admin' ? '管理员' : '普通用户' }}</div>
              </div>
            </div>
            <div class="user-stats">
              <div class="stat-item">
                <div class="stat-value">12</div>
                <div class="stat-label">任务完成</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">98.5%</div>
                <div class="stat-label">通过率</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">优秀</div>
                <div class="stat-label">绩效等级</div>
              </div>
            </div>
            <div class="action-buttons">
              <el-button type="primary" icon="el-icon-edit" @click="editMode = true" v-if="!editMode">编辑信息</el-button>
              <el-button type="danger" icon="el-icon-switch-button" @click="handleLogout">退出登录</el-button>
            </div>
          </div>
        </el-col>
        <el-col :span="18">
          <div class="profile-detail">
            <div class="section-title">
              <span class="text">基本信息</span>
              <div class="line"></div>
            </div>
            
            <!-- 信息显示模式 -->
            <div class="info-display" v-if="!editMode">
              <el-row :gutter="20" class="info-row">
                <el-col :span="12">
                  <div class="info-item">
                    <div class="info-label">用户名</div>
                    <div class="info-value">{{ user.username }}</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="info-item">
                    <div class="info-label">真实姓名</div>
                    <div class="info-value">{{ user.realname }}</div>
                  </div>
                </el-col>
              </el-row>
              <el-row :gutter="20" class="info-row">
                <el-col :span="12">
                  <div class="info-item">
                    <div class="info-label">所属部门</div>
                    <div class="info-value">{{ user.department }}</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="info-item">
                    <div class="info-label">职位</div>
                    <div class="info-value">质检工程师</div>
                  </div>
                </el-col>
              </el-row>
              <el-row :gutter="20" class="info-row">
                <el-col :span="12">
                  <div class="info-item">
                    <div class="info-label">手机号码</div>
                    <div class="info-value">138****6543</div>
                  </div>
                </el-col>
                <el-col :span="12">
                  <div class="info-item">
                    <div class="info-label">邮箱</div>
                    <div class="info-value">user@example.com</div>
                  </div>
                </el-col>
              </el-row>
            </div>
            
            <!-- 信息编辑模式 -->
            <div class="info-edit" v-else>
              <el-form :model="userForm" :rules="rules" ref="userForm" label-width="100px">
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="用户名" prop="username">
                      <el-input v-model="userForm.username" disabled></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="真实姓名" prop="realname">
                      <el-input v-model="userForm.realname"></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="所属部门" prop="department">
                      <el-select v-model="userForm.department" style="width: 100%">
                        <el-option
                          v-for="dept in departments"
                          :key="dept.value"
                          :label="dept.label"
                          :value="dept.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="职位" prop="position">
                      <el-input v-model="userForm.position"></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="手机号码" prop="phone">
                      <el-input v-model="userForm.phone"></el-input>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="邮箱" prop="email">
                      <el-input v-model="userForm.email"></el-input>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item>
                  <el-button type="primary" @click="updateProfile">保存</el-button>
                  <el-button @click="cancelEdit">取消</el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <div class="section-title" style="margin-top: 30px;">
              <span class="text">最近操作记录</span>
              <div class="line"></div>
            </div>
            
            <el-table
              :data="operationLogs"
              style="width: 100%; background-color: transparent;"
              :header-cell-style="headerStyle">
              <el-table-column prop="time" label="操作时间" width="180"></el-table-column>
              <el-table-column prop="operation" label="操作内容"></el-table-column>
              <el-table-column prop="result" label="操作结果" width="100">
                <template slot-scope="scope">
                  <span :style="{color: scope.row.result === '成功' ? '#52c41a' : '#f5222d'}">{{ scope.row.result }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Profile',
  data() {
    return {
      editMode: false,
      userForm: {
        username: '',
        realname: '',
        department: '',
        position: '质检工程师',
        phone: '13812346543',
        email: 'user@example.com'
      },
      rules: {
        realname: [
          { required: true, message: '请输入真实姓名', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
        ]
      },
      departments: [
        { value: '技术部', label: '技术部' },
        { value: '生产部', label: '生产部' },
        { value: '质检部', label: '质检部' },
        { value: '物流部', label: '物流部' },
        { value: '研发部', label: '研发部' }
      ],
      operationLogs: [
        {
          time: '2023-07-23 10:15:32',
          operation: '胶囊模具检测',
          result: '成功'
        },
        {
          time: '2023-07-23 09:42:18',
          operation: '设备维护',
          result: '成功'
        },
        {
          time: '2023-07-23 09:30:05',
          operation: '原料检验',
          result: '成功'
        },
        {
          time: '2023-07-22 17:40:12',
          operation: '模具清洗',
          result: '成功'
        }
      ],
      headerStyle: {
        color: '#fff',
        backgroundColor: 'rgba(0, 10, 50, 0.5)',
        borderColor: 'rgba(25, 186, 255, 0.1)'
      }
    }
  },
  computed: {
    ...mapState(['user'])
  },
  created() {
    // 初始化表单数据
    this.userForm = {
      username: this.user.username,
      realname: this.user.realname,
      department: this.user.department,
      position: '质检工程师',
      phone: '13812346543',
      email: 'user@example.com'
    }
  },
  methods: {
    updateProfile() {
      this.$refs.userForm.validate(valid => {
        if (valid) {
          // 更新用户信息
          const updatedUser = {
            ...this.user,
            realname: this.userForm.realname,
            department: this.userForm.department
          }
          
          this.$store.commit('setUser', updatedUser)
          localStorage.setItem('user', JSON.stringify(updatedUser))
          
          this.$message.success('个人信息更新成功')
          this.editMode = false
        }
      })
    },
    cancelEdit() {
      this.editMode = false
      // 重置表单
      this.userForm = {
        username: this.user.username,
        realname: this.user.realname,
        department: this.user.department,
        position: '质检工程师',
        phone: '13812346543',
        email: 'user@example.com'
      }
    },
    handleLogout() {
      this.$confirm('确认退出登录?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 清除用户信息
        this.$store.commit('setUser', null)
        localStorage.removeItem('user')
        
        this.$message.success('退出登录成功')
        this.$router.push('/login')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
  height: 100%;
  overflow: auto;
}

.profile-header {
  margin-bottom: 20px;
}

.profile-header h2 {
  color: #fff;
  font-size: 24px;
  font-weight: 500;
  margin: 0;
}

.profile-content {
  background-color: rgba(10, 26, 59, 0.5);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.profile-sidebar {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(25, 186, 255, 0.1);
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.avatar-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 10px;
  border: 2px solid rgba(25, 186, 255, 0.5);
  cursor: pointer;
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.avatar-overlay i {
  color: #fff;
  font-size: 24px;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.user-info {
  text-align: center;
}

.username {
  font-size: 18px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 5px;
}

.role {
  font-size: 14px;
  color: #1890ff;
}

.user-stats {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
  padding: 15px 0;
  border-top: 1px solid rgba(25, 186, 255, 0.1);
  border-bottom: 1px solid rgba(25, 186, 255, 0.1);
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 18px;
  font-weight: 500;
  color: #fff;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #919bb0;
}

.action-buttons {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.profile-detail {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 20px;
  min-height: 500px;
  border: 1px solid rgba(25, 186, 255, 0.1);
}

.section-title {
  position: relative;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title .text {
  font-size: 18px;
  font-weight: 500;
  color: #fff;
  padding-right: 15px;
}

.section-title .line {
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, rgba(25, 186, 255, 0.5), rgba(25, 186, 255, 0.1));
}

.info-row {
  margin-bottom: 20px;
}

.info-item {
  padding: 10px 15px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  border-left: 3px solid #1890ff;
}

.info-label {
  font-size: 14px;
  color: #919bb0;
  margin-bottom: 5px;
}

.info-value {
  font-size: 16px;
  color: #fff;
}

::v-deep .el-table {
  background-color: transparent !important;
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

::v-deep .el-input__inner {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(25, 186, 255, 0.3);
  color: #fff;
}

::v-deep .el-input.is-disabled .el-input__inner {
  background-color: rgba(0, 0, 0, 0.4);
  color: #919bb0;
}

::v-deep .el-form-item__label {
  color: #fff;
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