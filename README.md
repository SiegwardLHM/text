# 胶囊模具数字化检测系统

这是一个基于 Vue.js 开发的胶囊模具数字化检测系统，用于实现胶囊模具的生产过程监控、缺陷检测等功能。

## 功能特点

- 溶胶蘸胶过程可视化
- 工业相机实时监控
- 模具缺陷自动检测
- 生产数据统计分析
- 设备状态监控
- 人员管理系统

## 技术栈

- 前端：
  - Vue.js 2.x
  - Element UI
  - ECharts
  - Vuex
  - Vue Router
  - Axios

- 后端：
  - Node.js
  - json-server
  - RESTful API

## 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0

## 安装和运行

1. **克隆项目**：
```bash
git clone [项目地址]
cd [项目目录]
```

2. **安装依赖**：
```bash
# 安装项目依赖
npm install

# 安装 json-server
npm install json-server@0.17.4 --save
```

3. **启动后端服务**：
```bash
# 启动 json-server
node server.js
```

4. **启动前端服务**：
```bash
# 在新的终端窗口中运行
npm run serve
```

5. **访问系统**：
- 打开浏览器访问 `http://localhost:8080`
- 默认管理员账号：
  - 用户名：`admin`
  - 密码：`123456`

## 项目结构

```
├── src/                    # 源代码目录
│   ├── assets/            # 静态资源
│   ├── components/        # 公共组件
│   ├── router/           # 路由配置
│   ├── store/            # Vuex状态管理
│   ├── views/            # 页面视图
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── public/                # 公共资源目录
├── server.js             # 后端服务配置
├── db.json               # 数据存储文件
└── vue.config.js         # Vue CLI 配置文件
```

## 主要功能模块

1. **溶胶蘸胶过程动画**
   - 模拟展示整个蘸胶工艺流程
   - 工艺参数实时显示
   - 操作步骤指导

2. **模具缺陷检测**
   - 工业相机实时采集
   - 自动缺陷识别
   - 检测结果可视化
   - 数据统计分析

3. **生产监控**
   - 设备状态监控
   - 生产数据采集
   - 报警信息处理
   - 视频监控

4. **人员管理**
   - 用户在岗管理
   - 权限控制
   - 操作日志

## API 接口

- POST `/login` - 用户登录
- POST `/register` - 用户注册
- GET `/users` - 获取所有用户
- GET `/users/:id` - 获取单个用户
- PUT `/users/:id` - 更新用户信息
- DELETE `/users/:id` - 删除用户

## 开发团队

- 前端开发
- 后端开发
- 算法工程师
- 测试工程师

## 注意事项

1. 开发环境要求：
   - Node.js >= 16.0.0
   - npm >= 8.0.0

2. 配置要求：
   - 需要配置工业相机SDK
   - 需要配置后端服务API地址

3. 数据存储：
   - 用户数据存储在 `db.json` 文件中
   - 支持数据持久化

## 版权信息

© 2024 胶囊模具数字化检测系统 