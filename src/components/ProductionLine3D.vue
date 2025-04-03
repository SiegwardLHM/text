<template>
  <div class="production-line-3d" ref="container">
    <div class="loading-overlay" v-if="!isInitialized">
      <span>加载中...</span>
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <!-- 数字孪生监控面板 -->
    <div class="digital-twin-panel" v-if="isInitialized && !error && showPanel">
      <div class="panel-section">
        <h3>实时生产参数</h3>
        <div class="param-item">
          <span class="param-label">温度:</span>
          <span class="param-value" :class="{'alarm': temperature > 85}">{{ temperature }}°C</span>
        </div>
        <div class="param-item">
          <span class="param-label">溶胶粘度:</span>
          <span class="param-value" :class="{'alarm': viscosity < 180 || viscosity > 220}">{{ viscosity }} mPa·s</span>
        </div>
        <div class="param-item">
          <span class="param-label">浸泡时间:</span>
          <span class="param-value">{{ soakingTime }}s</span>
        </div>
        <div class="param-item">
          <span class="param-label">传送带速度:</span>
          <span class="param-value">{{ conveyorSpeed }} m/min</span>
        </div>
        <div class="param-item">
          <span class="param-label">设备运行状态:</span>
          <span class="param-value" :class="{'status-normal': deviceStatus === '正常', 'status-warning': deviceStatus === '注意', 'status-error': deviceStatus === '异常'}">{{ deviceStatus }}</span>
        </div>
      </div>
      
      <div class="panel-section">
        <h3>生产预测</h3>
        <div class="prediction-item">
          <span class="prediction-label">预计良品率:</span>
          <span class="prediction-value" :class="{'good': qualityPrediction > 95, 'warning': qualityPrediction <= 95 && qualityPrediction > 90, 'bad': qualityPrediction <= 90}">{{ qualityPrediction }}%</span>
        </div>
        <div class="prediction-item">
          <span class="prediction-label">预计完成时间:</span>
          <span class="prediction-value">{{ estimatedCompletionTime }}</span>
        </div>
        <div class="prediction-item">
          <span class="prediction-label">能耗预测:</span>
          <span class="prediction-value">{{ energyConsumption }} kWh</span>
        </div>
      </div>
      
      <div class="panel-section">
        <h3>设备状态监控</h3>
        <div class="device-status-grid">
          <div v-for="(status, index) in componentStatus" :key="index"
               class="device-status-item" :class="getStatusClass(status.status)">
            <div class="status-icon"></div>
            <span class="status-name">{{ status.name }}</span>
            <span class="status-value">{{ status.status }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加控制按钮 -->
    <div class="panel-toggle" @click="togglePanel">
      <span v-if="showPanel">隐藏面板</span>
      <span v-else>显示面板</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductionLine3D',
  data() {
    return {
      THREE: null,
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      conveyor: null,
      molds: [],
      inspectionDevice: null,
      animationFrameId: null,
      isInitialized: false,
      error: null,
      conveyorGroup: null,
      moldGroup: null,
      isInspecting: false,
      inspectionLight: null,
      inspectionBeam: null,
      inspectionProgress: 0,
      lastInspectionTime: 0,
      processStep: 0, // 0: 初始, 1: 溶胶, 2: 蘸胶, 3: 干燥, 4: 检测
      dippingTank: null,
      dryingChamber: null,
      processTimer: null,
      moldStartPosition: { x: -20, y: 0.6, z: 0 },
      isProcessing: false,
      animationDurations: {
        moveToTank: 3000,    // 移动到溶胶槽的时间
        dipping: 2000,       // 下降到溶胶中的时间
        soaking: 3000,       // 浸泡时间
        rising: 2000,        // 上升时间
        moveToDrying: 3000,  // 移动到干燥室的时间
        drying: 5000,        // 干燥时间
        moveToInspection: 3000, // 移动到检测区的时间
        inspection: 2000     // 检测时间
      },
      currentAnimation: null,
      animationQueue: [], // 动画队列
      isAnimating: false,  // 动画执行状态
      isAnimationComplete: false, // 添加动画完成状态标志
      emitAnimationComplete: false, // 添加是否已发送完成事件的标志
      
      // 数字孪生相关数据
      temperature: 75,           // 实时温度
      viscosity: 200,            // 溶胶粘度
      soakingTime: 3.0,          // 浸泡时间
      conveyorSpeed: 8.5,        // 传送带速度
      deviceStatus: '正常',      // 设备运行状态
      qualityPrediction: 97.5,   // 预计良品率
      estimatedCompletionTime: '14:30:00', // 预计完成时间
      energyConsumption: 12.8,   // 能耗预测
      componentStatus: [         // 设备组件状态
        { name: '溶胶泵', status: '正常' },
        { name: '液压系统', status: '正常' },
        { name: '干燥系统', status: '正常' },
        { name: '传送装置', status: '正常' },
        { name: '检测相机', status: '正常' },
        { name: '控制系统', status: '正常' }
      ],
      sensorData: {},            // 传感器数据
      maintenancePrediction: {}, // 维护预测
      dataUpdateInterval: null,   // 数据更新计时器
      inspectionTime: 2.0, // 检测时间，单位秒
      showPanel: true, // 控制面板显示状态
    };
  },
  async created() {
    try {
      // 预加载Three.js模块并保存引用
      const [THREE] = await Promise.all([
        import('three'),
        import('three/examples/jsm/controls/OrbitControls')
      ]);
      this.THREE = THREE; // 保存THREE引用
    } catch (error) {
      this.error = '3D组件加载失败，请刷新页面重试';
      console.error('Three.js模块加载失败:', error);
    }
  },
  async mounted() {
    if (this.error) return;
    
    try {
      const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls');
      
      await this.$nextTick();
      
      if (!this.$refs.container) {
        throw new Error('渲染容器未找到');
      }
      
      // 使用已保存的THREE引用
      this.scene = new this.THREE.Scene();
      this.scene.background = new this.THREE.Color(0x001428);

      // 创建相机
      this.camera = new this.THREE.PerspectiveCamera(
        75,
        this.$refs.container.clientWidth / this.$refs.container.clientHeight,
        0.1,
        1000
      );
      // 调整相机位置，能够看到整个传送带
      this.camera.position.set(0, 20, 30);
      this.camera.lookAt(0, 0, 0);

      // 创建渲染器
      this.renderer = new this.THREE.WebGLRenderer({ 
        antialias: true,
        alpha: true
      });
      this.renderer.setSize(
        this.$refs.container.clientWidth,
        this.$refs.container.clientHeight
      );
      this.renderer.setPixelRatio(window.devicePixelRatio);
      this.renderer.shadowMap.enabled = true;
      this.renderer.shadowMap.type = this.THREE.PCFSoftShadowMap;
      this.$refs.container.appendChild(this.renderer.domElement);

      // 添加轨道控制器
      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.enableDamping = true;
      this.controls.dampingFactor = 0.05;
      this.controls.screenSpacePanning = false;
      this.controls.minDistance = 10;
      this.controls.maxDistance = 50;
      this.controls.maxPolarAngle = Math.PI / 2;

      // 添加灯光
      const ambientLight = new this.THREE.AmbientLight(0xffffff, 0.5);
      this.scene.add(ambientLight);

      const directionalLight = new this.THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(15, 15, 15);
      directionalLight.castShadow = true;
      directionalLight.shadow.mapSize.width = 2048;
      directionalLight.shadow.mapSize.height = 2048;
      this.scene.add(directionalLight);

      // 创建传送带组
      this.conveyorGroup = new this.THREE.Group();
      
      // 主传送带 - 增加长度，覆盖从溶胶槽到检测位置的距离
      const conveyorGeometry = new this.THREE.BoxGeometry(35, 0.5, 8);
      const conveyorMaterial = new this.THREE.MeshStandardMaterial({ 
        color: 0x888888,
        metalness: 0.7,
        roughness: 0.3
      });
      this.conveyor = new this.THREE.Mesh(conveyorGeometry, conveyorMaterial);
      this.conveyor.receiveShadow = true;
      this.conveyorGroup.add(this.conveyor);

      // 添加传送带导轨 - 增加长度匹配主传送带
      const conveyorRailGeometry = new this.THREE.BoxGeometry(35, 0.2, 0.3);
      const conveyorRailMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x444444,
        metalness: 0.8,
        roughness: 0.2
      });
      
      const leftRail = new this.THREE.Mesh(conveyorRailGeometry, conveyorRailMaterial);
      leftRail.position.set(0, 0.3, 3.5);
      leftRail.castShadow = true;
      this.conveyorGroup.add(leftRail);
      
      const rightRail = new this.THREE.Mesh(conveyorRailGeometry, conveyorRailMaterial);
      rightRail.position.set(0, 0.3, -3.5);
      rightRail.castShadow = true;
      this.conveyorGroup.add(rightRail);

      // 添加齿轮传动系统
      const gearGeometry = new this.THREE.CylinderGeometry(0.8, 0.8, 0.3, 32);
      const gearMaterial = new this.THREE.MeshPhongMaterial({
        color: 0x666666,
        shininess: 70
      });
      
      // 调整齿轮位置到传送带两端
      const gearPositions = [
        [-17, -0.5, 3.5], [-17, -0.5, -3.5],
        [17, -0.5, 3.5], [17, -0.5, -3.5]
      ];
      
      gearPositions.forEach(pos => {
        const gear = new this.THREE.Mesh(gearGeometry, gearMaterial);
        gear.position.set(...pos);
        gear.rotation.x = Math.PI / 2;
        gear.castShadow = true;
        this.conveyorGroup.add(gear);
      });

      // 添加支撑结构
      const supportGeometry = new this.THREE.BoxGeometry(0.8, 4, 0.8);
      const supportMaterial = new this.THREE.MeshPhongMaterial({
        color: 0x444444,
        shininess: 50
      });
      
      // 调整支撑结构位置到传送带两端
      const conveyorSupportPositions = [
        [-17, -2, 3.5], [-17, -2, -3.5],
        [17, -2, 3.5], [17, -2, -3.5]
      ];
      
      conveyorSupportPositions.forEach(pos => {
        const support = new this.THREE.Mesh(supportGeometry, supportMaterial);
        support.position.set(...pos);
        support.castShadow = true;
        this.conveyorGroup.add(support);
      });

      this.scene.add(this.conveyorGroup);

      // 创建模具阵列组
      this.moldGroup = new this.THREE.Group();
      
      // 创建单个模具几何体 - 修改为竖直放置的圆柱体（增加高度，修改为竖直放置）
      const moldGeometry = new this.THREE.CylinderGeometry(0.15, 0.15, 0.8, 16);
      const moldMaterial = new this.THREE.MeshStandardMaterial({ 
        color: 0xC0C0C0,
        metalness: 0.8,
        roughness: 0.2
      });

      // 创建36x36模具阵列
      const spacing = 0.35;
      for (let i = 0; i < 36; i++) {
        for (let j = 0; j < 36; j++) {
          const mold = new this.THREE.Mesh(moldGeometry, moldMaterial);
          mold.position.set(
            (i - 17.5) * spacing,
            0.6, // 调整Y轴位置，使模具竖直安置在传送带上
            (j - 17.5) * spacing
          );
          // 移除水平旋转，让圆柱体保持竖直
          // mold.rotation.x = Math.PI / 2;
          mold.castShadow = true;
          mold.receiveShadow = true;
          this.moldGroup.add(mold);
          this.molds.push(mold);
        }
      }
      
      this.scene.add(this.moldGroup);

      // 创建检测设备组
      const inspectionGroup = new this.THREE.Group();
      // 将检测设备移至传送带右端
      inspectionGroup.position.set(12, 8, 0); // 移至传送带右端位置且保持较高位置
      
      // 创建主框架结构 - 参考照片中的金属框架
      const frameGeometry = new this.THREE.BoxGeometry(4, 1.2, 5);
      const frameMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x444444,
        metalness: 0.7,
        roughness: 0.3
      });
      const frame = new this.THREE.Mesh(frameGeometry, frameMaterial);
      frame.castShadow = true;
      inspectionGroup.add(frame);

      // 添加底部框架 - 参考照片中的下层金属支架
      const bottomFrameGeometry = new this.THREE.BoxGeometry(4, 0.8, 5);
      const bottomFrame = new this.THREE.Mesh(bottomFrameGeometry, frameMaterial);
      bottomFrame.position.set(0, -12, 0); // 位于底部
      bottomFrame.castShadow = true;
      inspectionGroup.add(bottomFrame);

      // 添加支撑杆，参考照片中的4根圆柱形支撑
      const supportPoleGeometry = new this.THREE.CylinderGeometry(0.3, 0.3, 12, 16);
      const supportPoleMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xCCCCCC, // 银色
        metalness: 0.9,
        roughness: 0.2
      });
      
      // 添加四根支撑柱，对应照片中的位置
      const machineSupportPositions = [
        [-1.5, -6, 2], [-1.5, -6, -2],
        [1.5, -6, 2], [1.5, -6, -2]
      ];
      
      machineSupportPositions.forEach(pos => {
        const supportPole = new this.THREE.Mesh(supportPoleGeometry, supportPoleMaterial);
        supportPole.position.set(...pos);
        supportPole.castShadow = true;
        inspectionGroup.add(supportPole);
      });

      // 添加液压缸 - 参考照片中央的液压装置
      const hydraulicCylinderGeometry = new this.THREE.CylinderGeometry(0.4, 0.4, 3, 16);
      const hydraulicCylinderMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x888888,
        metalness: 0.8,
        roughness: 0.2
      });
      const hydraulicCylinder = new this.THREE.Mesh(hydraulicCylinderGeometry, hydraulicCylinderMaterial);
      hydraulicCylinder.position.set(0, -8, 0);
      hydraulicCylinder.castShadow = true;
      inspectionGroup.add(hydraulicCylinder);

      // 添加液压杆 - 较细的活塞杆
      const hydraulicRodGeometry = new this.THREE.CylinderGeometry(0.2, 0.2, 3, 16);
      const hydraulicRodMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xDDDDDD,
        metalness: 0.9,
        roughness: 0.1
      });
      const hydraulicRod = new this.THREE.Mesh(hydraulicRodGeometry, hydraulicRodMaterial);
      hydraulicRod.position.set(0, -5.5, 0);
      hydraulicRod.castShadow = true;
      inspectionGroup.add(hydraulicRod);

      // 添加上部导轨结构 - 参考照片中的横向金属导轨
      const machineRailGeometry = new this.THREE.BoxGeometry(4.2, 0.4, 0.4);
      const machineRailMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x666666,
        metalness: 0.8, 
        roughness: 0.2
      });
      
      // 顶部横向导轨
      const topRails = [];
      const machineRailPositions = [
        [0, -2, 2], [0, -2, -2]
      ];
      
      machineRailPositions.forEach(pos => {
        const rail = new this.THREE.Mesh(machineRailGeometry, machineRailMaterial);
        rail.position.set(...pos);
        rail.castShadow = true;
        inspectionGroup.add(rail);
        topRails.push(rail);
      });

      // 添加运动滑块部分 - 参考照片中的可移动部件
      const sliderGeometry = new this.THREE.BoxGeometry(1.2, 0.6, 5);
      const sliderMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x333333,
        metalness: 0.7,
        roughness: 0.3
      });
      const slider = new this.THREE.Mesh(sliderGeometry, sliderMaterial);
      slider.position.set(0, -2.5, 0);
      slider.castShadow = true;
      inspectionGroup.add(slider);

      // 添加精密导向轴 - 参考照片中的光亮金属杆
      const guideRodGeometry = new this.THREE.CylinderGeometry(0.1, 0.1, 5.5, 16);
      const guideRodMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xDDDDDD,
        metalness: 0.95,
        roughness: 0.05
      });
      
      // 添加两根水平导向轴
      const guideRodPositions = [
        [0.7, -2.2, 0], [-0.7, -2.2, 0]
      ];
      
      guideRodPositions.forEach(pos => {
        const guideRod = new this.THREE.Mesh(guideRodGeometry, guideRodMaterial);
        guideRod.position.set(...pos);
        guideRod.rotation.z = Math.PI / 2; // 水平放置
        guideRod.castShadow = true;
        inspectionGroup.add(guideRod);
      });

      // 添加圆形连接件 - 参考照片中的圆形接头
      const connectorGeometry = new this.THREE.CylinderGeometry(0.25, 0.25, 0.3, 16);
      const connectorMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xAAAAAA,
        metalness: 0.8,
        roughness: 0.2
      });
      
      // 添加连接件到四个支撑柱顶部和底部
      machineSupportPositions.forEach(pos => {
        // 顶部连接件
        const topConnector = new this.THREE.Mesh(connectorGeometry, connectorMaterial);
        topConnector.position.set(pos[0], pos[1] - 6, pos[2]);
        topConnector.castShadow = true;
        inspectionGroup.add(topConnector);
        
        // 底部连接件
        const bottomConnector = new this.THREE.Mesh(connectorGeometry, connectorMaterial);
        bottomConnector.position.set(pos[0], pos[1] + 6, pos[2]);
        bottomConnector.castShadow = true;
        inspectionGroup.add(bottomConnector);
      });

      // 添加螺丝和紧固件 - 增加细节
      const screwGeometry = new this.THREE.CylinderGeometry(0.08, 0.08, 0.2, 6);
      const screwMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x888888,
        metalness: 0.8,
        roughness: 0.3
      });
      
      // 添加螺丝到框架边角
      const screwPositions = [
        [-1.8, -0.5, 2.3], [-1.8, -0.5, -2.3],
        [1.8, -0.5, 2.3], [1.8, -0.5, -2.3],
        [-1.8, -11.5, 2.3], [-1.8, -11.5, -2.3],
        [1.8, -11.5, 2.3], [1.8, -11.5, -2.3]
      ];
      
      screwPositions.forEach(pos => {
        const screw = new this.THREE.Mesh(screwGeometry, screwMaterial);
        screw.position.set(...pos);
        screw.castShadow = true;
        inspectionGroup.add(screw);
      });

      // 添加电气连接线缆 - 参考照片中的黑色线缆
      const cableGeometry = new this.THREE.TubeGeometry(
        new this.THREE.CatmullRomCurve3([
          new this.THREE.Vector3(0, -3, -3),
          new this.THREE.Vector3(0.5, -4, -3),
          new this.THREE.Vector3(1, -6, -2),
          new this.THREE.Vector3(1.5, -8, -1),
          new this.THREE.Vector3(1.8, -10, 0)
        ]),
        20, 0.05, 8, false
      );
      
      const cableMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x111111,
        roughness: 0.9,
        metalness: 0.1
      });
      
      const cable = new this.THREE.Mesh(cableGeometry, cableMaterial);
      cable.castShadow = true;
      inspectionGroup.add(cable);

      // 添加气动/液压管道 - 参考照片中的白色/透明管
      const tubingGeometry = new this.THREE.TubeGeometry(
        new this.THREE.CatmullRomCurve3([
          new this.THREE.Vector3(0, -5.5, 0),
          new this.THREE.Vector3(0.3, -6, 0.5),
          new this.THREE.Vector3(0.6, -8, 1),
          new this.THREE.Vector3(1, -10, 1.5)
        ]),
        20, 0.04, 8, false
      );
      
      const tubingMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xDDDDDD,
        roughness: 0.3,
        metalness: 0.2,
        transparent: true,
        opacity: 0.7
      });
      
      const tubing = new this.THREE.Mesh(tubingGeometry, tubingMaterial);
      tubing.castShadow = true;
      inspectionGroup.add(tubing);

      // 添加传感器模块 - 参考照片中的小型传感器设备
      const sensorGeometry = new this.THREE.BoxGeometry(0.4, 0.3, 0.4);
      const sensorMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x444444,
        metalness: 0.6,
        roughness: 0.4
      });
      
      const sensorPositions = [
        [1.5, -2, 1.5], [-1.5, -2, 1.5],
        [0, -3, -2.5]
      ];
      
      sensorPositions.forEach(pos => {
        const sensor = new this.THREE.Mesh(sensorGeometry, sensorMaterial);
        sensor.position.set(...pos);
        sensor.castShadow = true;
        inspectionGroup.add(sensor);
        
        // 添加传感器指示灯
        const sensorLedGeometry = new this.THREE.BoxGeometry(0.1, 0.1, 0.1);
        const sensorLedMaterial = new this.THREE.MeshBasicMaterial({
          color: 0xff0000,
          emissive: 0xff0000,
          emissiveIntensity: 0.5
        });
        const sensorLed = new this.THREE.Mesh(sensorLedGeometry, sensorLedMaterial);
        sensorLed.position.set(0, 0.1, 0.15);
        sensor.add(sensorLed);
      });

      // 添加机械臂结构 - 连接相机部分
      const armGeometry = new this.THREE.BoxGeometry(0.6, 1.8, 0.6);
      const armMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x222222,
        metalness: 0.7, 
        roughness: 0.3
      });
      const arm = new this.THREE.Mesh(armGeometry, armMaterial);
      arm.position.set(0, -3.5, -2);
      arm.castShadow = true;
      inspectionGroup.add(arm);

      // 添加绿色LED指示灯 - 参考照片中的指示灯
      const indicatorGeometry = new this.THREE.BoxGeometry(0.3, 0.3, 0.3);
      const indicatorMaterial = new this.THREE.MeshBasicMaterial({
        color: 0x00ff00,
        emissive: 0x00ff00,
        emissiveIntensity: 0.5
      });
      const indicator = new this.THREE.Mesh(indicatorGeometry, indicatorMaterial);
      indicator.position.set(-1.5, -0.2, -2);
      inspectionGroup.add(indicator);

      // 添加控制盒 - 参考照片中的黑色控制盒
      const controlBoxGeometry = new this.THREE.BoxGeometry(1, 2, 0.8);
      const controlBoxMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x111111,
        metalness: 0.7,
        roughness: 0.3
      });
      const controlBox = new this.THREE.Mesh(controlBoxGeometry, controlBoxMaterial);
      controlBox.position.set(0, -2, 2.5);
      controlBox.castShadow = true;
      inspectionGroup.add(controlBox);

      // 先创建相机装置外观
      // 相机外壳 - 参考照片中的黑色相机模块
      const cameraHousingGeometry = new this.THREE.BoxGeometry(1.5, 1.0, 1.2);
      const cameraHousingMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x222222,
        metalness: 0.8,
        roughness: 0.2
      });
      const cameraHousing = new this.THREE.Mesh(cameraHousingGeometry, cameraHousingMaterial);
      cameraHousing.position.set(0, -3.5, -3);
      cameraHousing.castShadow = true;
      inspectionGroup.add(cameraHousing);

      // 现在可以安全地修改相机位置
      cameraHousing.position.set(0, -1.5, -1);
      
      // 镜头 - 更专业的工业镜头
      const lensGeometry = new this.THREE.CylinderGeometry(0.5, 0.4, 0.8, 32);
      const lensMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x111111,
        metalness: 0.9,
        roughness: 0.1
      });
      const lens = new this.THREE.Mesh(lensGeometry, lensMaterial);
      lens.position.set(0, -1, 0);
      lens.rotation.x = Math.PI / 2;
      lens.castShadow = true;
      cameraHousing.add(lens);

      // 镜头内部玻璃
      const lensGlassGeometry = new this.THREE.CylinderGeometry(0.35, 0.35, 0.05, 32);
      const lensGlassMaterial = new this.THREE.MeshPhongMaterial({
        color: 0x88ccff,
        shininess: 100,
        transparent: true,
        opacity: 0.7
      });
      const lensGlass = new this.THREE.Mesh(lensGlassGeometry, lensGlassMaterial);
      lensGlass.position.set(0, -1.4, 0);
      lensGlass.rotation.x = Math.PI / 2;
      cameraHousing.add(lensGlass);

      // 添加闪光灯组
      const flashGroupGeometry = new this.THREE.BoxGeometry(0.8, 0.3, 0.8);
      const flashGroupMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x333333,
        metalness: 0.7,
        roughness: 0.3
      });
      const flashGroup = new this.THREE.Mesh(flashGroupGeometry, flashGroupMaterial);
      flashGroup.position.set(0.8, -0.6, 0);
      cameraHousing.add(flashGroup);

      // 闪光灯灯管
      const flashGeometry = new this.THREE.CylinderGeometry(0.15, 0.15, 0.1, 16);
      const flashMaterial = new this.THREE.MeshPhongMaterial({
        color: 0xffffff,
        emissive: 0xffffff,
        emissiveIntensity: 0.1,
        transparent: true,
        opacity: 0.9
      });
      this.flashBulb = new this.THREE.Mesh(flashGeometry, flashMaterial);
      this.flashBulb.position.set(0, -0.15, 0);
      this.flashBulb.rotation.x = Math.PI / 2;
      flashGroup.add(this.flashBulb);

      // 增加扫描线效果
      const scanLineGeometry = new this.THREE.PlaneGeometry(12, 0.1);
      const scanLineMaterial = new this.THREE.MeshBasicMaterial({
        color: 0x00ff88,
        transparent: true,
        opacity: 0.8,
        side: this.THREE.DoubleSide
      });
      this.scanLine = new this.THREE.Mesh(scanLineGeometry, scanLineMaterial);
      this.scanLine.rotation.x = Math.PI / 2;
      this.scanLine.position.set(0, 0, 0);
      this.scanLine.visible = false;
      cameraHousing.add(this.scanLine);

      // 添加检测光束
      const beamGeometry = new this.THREE.BoxGeometry(12, 0.05, 12);
      const beamMaterial = new this.THREE.MeshBasicMaterial({
        color: 0x00ff22,
        transparent: true,
        opacity: 0.3
      });
      this.inspectionBeam = new this.THREE.Mesh(beamGeometry, beamMaterial);
      this.inspectionBeam.position.set(0, -4, 0); // 位置下移
      this.inspectionBeam.visible = false;
      cameraHousing.add(this.inspectionBeam);

      // 修改扫描光束位置，使其能正确照射竖直放置的模具
      if (this.inspectionBeam) {
        this.inspectionBeam.position.set(0, -4, 0);
      }
      if (this.scanLine) {
        this.scanLine.position.set(0, -4, 0);
      }

      // 添加检测指示灯
      const lightGeometry = new this.THREE.SphereGeometry(0.15, 16, 16);
      const lightMaterial = new this.THREE.MeshPhongMaterial({
        color: 0x00ff00,
        emissive: 0x00ff00,
        emissiveIntensity: 0.5
      });
      this.inspectionLight = new this.THREE.Mesh(lightGeometry, lightMaterial);
      this.inspectionLight.position.set(0.6, 0, 0);
      cameraHousing.add(this.inspectionLight);

      this.scene.add(inspectionGroup);

      // 添加地面
      const groundGeometry = new this.THREE.PlaneGeometry(50, 50);
      const groundMaterial = new this.THREE.MeshPhongMaterial({
        color: 0x222222,
        shininess: 30
      });
      const ground = new this.THREE.Mesh(groundGeometry, groundMaterial);
      ground.rotation.x = -Math.PI / 2;
      ground.position.y = -4;
      ground.receiveShadow = true;
      this.scene.add(ground);

      // 修改溶胶槽 - 更新为符合照片中的压制成型机
      const tankGeometry = new this.THREE.BoxGeometry(6, 3, 6);
      const tankMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x666666,
        metalness: 0.7,
        roughness: 0.3
      });
      this.dippingTank = new this.THREE.Mesh(tankGeometry, tankMaterial);
      // 修改溶胶槽位置到传送带左端
      this.dippingTank.position.set(-12, -0.5, 0);
      this.dippingTank.castShadow = true;
      this.scene.add(this.dippingTank);

      // 添加上下模具结构 - 参考照片中的压制成型设备
      const upperMoldGeometry = new this.THREE.BoxGeometry(4, 1, 4);
      const upperMoldMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x555555,
        metalness: 0.8,
        roughness: 0.2
      });
      const upperMold = new this.THREE.Mesh(upperMoldGeometry, upperMoldMaterial);
      upperMold.position.set(0, 1, 0);
      this.dippingTank.add(upperMold);

      // 添加模具导向柱 - 参考照片中的圆柱导向件
      const moldGuideGeometry = new this.THREE.CylinderGeometry(0.2, 0.2, 4, 16);
      const moldGuideMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xCCCCCC,
        metalness: 0.9,
        roughness: 0.1
      });
      
      const moldGuidePositions = [
        [-1.8, 0, 1.8], [-1.8, 0, -1.8],
        [1.8, 0, 1.8], [1.8, 0, -1.8]
      ];
      
      moldGuidePositions.forEach(pos => {
        const moldGuide = new this.THREE.Mesh(moldGuideGeometry, moldGuideMaterial);
        moldGuide.position.set(...pos);
        this.dippingTank.add(moldGuide);
      });

      // 添加液压缸 - 参考照片中的加压系统
      const pressCylinderGeometry = new this.THREE.CylinderGeometry(0.6, 0.6, 2, 16);
      const pressCylinderMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x444444,
        metalness: 0.7,
        roughness: 0.3
      });
      const pressCylinder = new this.THREE.Mesh(pressCylinderGeometry, pressCylinderMaterial);
      pressCylinder.position.set(0, 2.5, 0);
      this.dippingTank.add(pressCylinder);

      // 添加液压活塞杆
      const pressRodGeometry = new this.THREE.CylinderGeometry(0.3, 0.3, 1.5, 16);
      const pressRodMaterial = new this.THREE.MeshStandardMaterial({
        color: 0xDDDDDD,
        metalness: 0.9,
        roughness: 0.1
      });
      const pressRod = new this.THREE.Mesh(pressRodGeometry, pressRodMaterial);
      pressRod.position.set(0, 1, 0);
      pressCylinder.add(pressRod);

      // 添加控制面板和管道连接 - 参考照片中的控制装置
      const controlPanelGeometry = new this.THREE.BoxGeometry(1.5, 2, 0.6);
      const controlPanelMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x222222,
        metalness: 0.6,
        roughness: 0.4
      });
      const controlPanel = new this.THREE.Mesh(controlPanelGeometry, controlPanelMaterial);
      controlPanel.position.set(-2.5, 0, -2.5);
      this.dippingTank.add(controlPanel);

      // 添加按钮和指示灯
      const buttonGeometries = [
        new this.THREE.CylinderGeometry(0.1, 0.1, 0.05, 16),
        new this.THREE.CylinderGeometry(0.1, 0.1, 0.05, 16),
        new this.THREE.CylinderGeometry(0.1, 0.1, 0.05, 16)
      ];
      
      const buttonMaterials = [
        new this.THREE.MeshBasicMaterial({ color: 0x00ff00 }),
        new this.THREE.MeshBasicMaterial({ color: 0xff0000 }),
        new this.THREE.MeshBasicMaterial({ color: 0xffff00 })
      ];
      
      const buttonPositions = [
        [0, 0.5, 0.31],
        [0, 0, 0.31],
        [0, -0.5, 0.31]
      ];
      
      for (let i = 0; i < 3; i++) {
        const button = new this.THREE.Mesh(buttonGeometries[i], buttonMaterials[i]);
        button.position.set(...buttonPositions[i]);
        button.rotation.x = Math.PI / 2;
        controlPanel.add(button);
      }

      // 添加管道连接 - 参考照片中的连接管线
      const pipesGeometry = new this.THREE.CylinderGeometry(0.15, 0.15, 3, 16);
      const pipesMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x888888,
        metalness: 0.8,
        roughness: 0.2
      });
      
      const pipes = new this.THREE.Mesh(pipesGeometry, pipesMaterial);
      pipes.position.set(-3, -1, 0);
      pipes.rotation.z = Math.PI / 2;
      this.dippingTank.add(pipes);

      // 创建干燥室
      const chamberGeometry = new this.THREE.BoxGeometry(6, 4, 8);
      const chamberMaterial = new this.THREE.MeshStandardMaterial({
        color: 0x888888,
        metalness: 0.6,
        roughness: 0.4
      });
      this.dryingChamber = new this.THREE.Mesh(chamberGeometry, chamberMaterial);
      // 将干燥室放在传送带中部偏左位置
      this.dryingChamber.position.set(-4, 1, 0);
      this.dryingChamber.castShadow = true;
      this.scene.add(this.dryingChamber);

      // 添加干燥室通风口
      const ventGeometry = new this.THREE.CylinderGeometry(0.3, 0.3, 1, 16);
      const ventMaterial = new this.THREE.MeshPhongMaterial({
        color: 0x444444
      });
      const ventPositions = [
        [-2, 2, -3], [-2, 2, 3],
        [2, 2, -3], [2, 2, 3]
      ];
      ventPositions.forEach(pos => {
        const vent = new this.THREE.Mesh(ventGeometry, ventMaterial);
        vent.position.set(...pos);
        vent.rotation.x = Math.PI / 2;
        this.dryingChamber.add(vent);
      });

      // 初始化模具位置
      if (this.moldGroup) {
        this.moldGroup.position.set(
          this.moldStartPosition.x,
          this.moldStartPosition.y,
          this.moldStartPosition.z
        );
      }

      // 开始动画循环
      this.animate();
      window.addEventListener('resize', this.onWindowResize);
      this.isInitialized = true;
      
      // 启动数字孪生数据更新服务
      this.startDigitalTwinService();
      
    } catch (error) {
      this.error = '3D场景初始化失败，请刷新页面重试';
      console.error('3D场景初始化失败:', error);
    }
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onWindowResize);
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }
    if (this.renderer) {
      this.renderer.dispose();
    }
    this.disposeScene();
    
    // 清除数据更新计时器
    if (this.dataUpdateInterval) {
      clearInterval(this.dataUpdateInterval);
    }
  },
  methods: {
    // 数字孪生相关方法
    startDigitalTwinService() {
      // 模拟数据更新，实际应用中应连接实际设备API
      this.dataUpdateInterval = setInterval(() => {
        this.updateRealTimeData();
        this.updatePredictions();
        this.monitorDeviceStatus();
      }, 2000);
    },
    
    updateRealTimeData() {
      // 模拟实时数据波动
      this.temperature = Math.round((75 + Math.random() * 15) * 10) / 10;
      this.viscosity = Math.round((190 + Math.random() * 30) * 10) / 10;
      this.soakingTime = (3 + Math.random() * 0.5).toFixed(1);
      this.conveyorSpeed = (8 + Math.random()).toFixed(1);
      
      // 根据处理步骤调整参数
      if (this.processStep === 1) {
        this.temperature = Math.round((80 + Math.random() * 5) * 10) / 10;
      }
      else if (this.processStep === 3) {
        this.temperature = Math.round((65 + Math.random() * 5) * 10) / 10;
      }
      
      // 更新传感器数据
      this.sensorData = {
        humidity: Math.round((45 + Math.random() * 15) * 10) / 10,
        pressure: Math.round((101 + Math.random() * 3) * 10) / 10,
        airflow: Math.round((20 + Math.random() * 5) * 10) / 10
      };
    },
    
    updatePredictions() {
      // 模拟预测计算
      // 根据当前参数进行良品率预测
      const tempFactor = this.temperature > 85 ? 0.9 : 1;
      const viscosityFactor = (this.viscosity < 180 || this.viscosity > 220) ? 0.95 : 1;
      this.qualityPrediction = Math.round(98 * tempFactor * viscosityFactor * 10) / 10;
      
      // 更新预计完成时间
      const now = new Date();
      const completion = new Date(now.getTime() + 30 * 60 * 1000); // 预计30分钟后完成
      this.estimatedCompletionTime = `${completion.getHours()}:${String(completion.getMinutes()).padStart(2, '0')}:${String(completion.getSeconds()).padStart(2, '0')}`;
      
      // 更新能耗预测
      this.energyConsumption = (12 + Math.random() * 2).toFixed(1);
      
      // 设备维护预测
      this.maintenancePrediction = {
        nextMaintenance: '2023-06-15',
        criticalComponents: ['传送带轴承', '干燥系统加热元件'],
        remainingLifetime: Math.round(500 + Math.random() * 100)
      };
    },
    
    monitorDeviceStatus() {
      // 模拟设备状态监控
      // 随机生成组件状态异常
      if (Math.random() < 0.1) {
        const componentIndex = Math.floor(Math.random() * this.componentStatus.length);
        const statusOptions = ['正常', '注意', '异常'];
        const newStatus = statusOptions[Math.floor(Math.random() * 3)];
        this.componentStatus[componentIndex].status = newStatus;
      } else {
        // 偶尔恢复正常状态
        for (let i = 0; i < this.componentStatus.length; i++) {
          if (this.componentStatus[i].status !== '正常' && Math.random() < 0.3) {
            this.componentStatus[i].status = '正常';
          }
        }
      }
      
      // 根据组件状态更新总体状态
      const hasError = this.componentStatus.some(comp => comp.status === '异常');
      const hasWarning = this.componentStatus.some(comp => comp.status === '注意');
      
      if (hasError) {
        this.deviceStatus = '异常';
      } else if (hasWarning) {
        this.deviceStatus = '注意';
      } else {
        this.deviceStatus = '正常';
      }
      
      // 根据设备状态发送通知
      if (this.deviceStatus !== '正常') {
        this.$emit('device-status-change', this.deviceStatus);
      }
    },
    
    getStatusClass(status) {
      switch (status) {
        case '正常': return 'status-normal';
        case '注意': return 'status-warning';
        case '异常': return 'status-error';
        default: return '';
      }
    },
    
    // 添加与物理设备交互的方法
    adjustParameters(params) {
      // 在实际应用中，此方法将与真实设备API通信
      if (params.temperature) this.temperature = params.temperature;
      if (params.viscosity) this.viscosity = params.viscosity;
      if (params.soakingTime) this.soakingTime = params.soakingTime;
      if (params.conveyorSpeed) this.conveyorSpeed = params.conveyorSpeed;
      
      // 向物理设备发送调整命令
      this.$emit('parameter-adjustment', params);
      
      // 调整3D模型中的相关参数
      this.updateModelParameters(params);
    },
    
    updateModelParameters(params) {
      // 根据参数调整3D模型中的特性
      if (params.soakingTime) {
        this.animationDurations.soaking = params.soakingTime * 1000;
      }
      
      if (params.conveyorSpeed) {
        // 调整传送带速度
        const speedFactor = params.conveyorSpeed / 8.5; // 基于默认速度计算因子
        this.animationDurations.moveToInspection = 3000 / speedFactor;
      }
    },

    // 添加动画队列控制方法
    async executeAnimationQueue() {
      if (this.isAnimating || this.animationQueue.length === 0) return;
      
      this.isAnimating = true;
      
      while (this.animationQueue.length > 0) {
        const animation = this.animationQueue[0];
        await animation();
        this.animationQueue.shift();
      }
      
      this.isAnimating = false;
    },

    // 添加到动画队列
    addToAnimationQueue(animation) {
      this.animationQueue.push(animation);
      this.executeAnimationQueue();
    },

    // 创建Promise包装的动画
    createAnimationPromise(current, target, duration) {
      return new Promise(resolve => {
        this.currentAnimation = this.animateMoldMovement(
          current,
          target,
          duration,
          () => {
            this.currentAnimation = null;
            resolve();
          }
        );
      });
    },

    // 创建延时Promise
    createDelayPromise(duration) {
      return new Promise(resolve => setTimeout(resolve, duration));
    },

    // 添加通知动画完成的方法
    notifyAnimationComplete() {
      if (!this.emitAnimationComplete) {
        this.isAnimationComplete = true;
        this.emitAnimationComplete = true;
        this.$emit('animation-complete', {
          processData: {
            temperature: this.temperature,
            viscosity: this.viscosity,
            soakingTime: this.soakingTime,
            conveyorSpeed: this.conveyorSpeed
          }
        });
        console.log('3D动画完成，发送完成事件');
      }
    },

    animate() {
      this.animationFrameId = requestAnimationFrame(this.animate);

      try {
        if (this.controls) {
          this.controls.update();
        }

        // 检测过程动画和事件控制
        if (this.isInspecting && this.processStep === 4) {
          const currentTime = Date.now() * 0.001;
          const elapsed = currentTime - this.lastInspectionTime;
          const totalDuration = this.animationDurations.inspection / 1000;
          
          if (elapsed > totalDuration) {
            // 检测完成 - 隐藏所有扫描效果
            this.isInspecting = false;
            this.inspectionTime = 0;
            
            if (this.inspectionBeam) this.inspectionBeam.visible = false;
            if (this.scanLine) this.scanLine.visible = false;
            if (this.flashBulb) this.flashBulb.material.emissiveIntensity = 0.1;
            if (this.inspectionLight) {
              this.inspectionLight.material.color.setHex(0x00ff00);
              this.inspectionLight.material.emissive.setHex(0x00ff00);
            }
            
            // 检测完成，但先不发送完成事件，等待结果分析
            this.isAnimationComplete = true;
            
            setTimeout(() => {
              if (!this.emitAnimationComplete) {
                this.notifyAnimationComplete();
              }
            }, 2000);
          } else {
            // 更新检测状态
            this.inspectionTime = totalDuration - elapsed;
            const scanProgress = elapsed / totalDuration; // 0到1之间的值
            
            // 计算当前扫描位置，从模具顶部到底部
            const startY = -5;  // 光束起始高度
            const scanDistance = 8; // 扫描总距离
            const currentY = startY + scanProgress * scanDistance;
            
            // 更新光束位置
            if (this.inspectionBeam) {
              this.inspectionBeam.visible = true;
              this.inspectionBeam.position.y = currentY;
              
              // 光束脉冲效果
              this.inspectionBeam.material.opacity = 0.3 + 0.1 * Math.sin(elapsed * 8);
            }
            
            // 更新扫描线位置
            if (this.scanLine) {
              this.scanLine.visible = true;
              this.scanLine.position.y = currentY;
              
              // 扫描线脉冲效果
              const pulsePhase = (Math.sin(elapsed * 20) + 1) / 2; // 0到1的脉冲
              this.scanLine.material.opacity = 0.6 + 0.4 * pulsePhase;
              this.scanLine.scale.x = 1 + 0.1 * pulsePhase;
            }
            
            // 拍照闪光效果 - 每秒闪4次
            if (Math.floor(elapsed * 4) !== Math.floor((elapsed - 0.016) * 4)) {
              if (this.flashBulb) {
                // 闪光灯闪烁
                this.flashBulb.material.emissiveIntensity = 1.0;
                setTimeout(() => {
                  if (this.flashBulb) {
                    this.flashBulb.material.emissiveIntensity = 0.1;
                  }
                }, 100);
              }
            }
          }
        }

        // 传送带运动
        if (this.conveyorGroup) {
          this.conveyorGroup.children.forEach(child => {
            if (child.geometry instanceof this.THREE.CylinderGeometry) {
              child.rotation.x += 0.02;
            }
          });
        }

        // 模具处理流程动画
        if (this.moldGroup && !this.isProcessing && !this.isAnimating) {
          switch(this.processStep) {
            case 0: // 初始状态，移动到溶胶槽
              this.isProcessing = true;
              this.addToAnimationQueue(async () => {
                await this.createAnimationPromise(
                  this.moldGroup.position,
                  { x: -12, y: 0.6, z: 0 }, // 调整Y轴高度适应竖直模具
                  this.animationDurations.moveToTank
                );
                this.processStep = 1;
                this.isProcessing = false;
              });
              break;

            case 1: // 溶胶过程
              this.isProcessing = true;
              this.addToAnimationQueue(async () => {
                // 下降到溶胶中
                await this.createAnimationPromise(
                  this.moldGroup.position,
                  { x: -12, y: -0.8, z: 0 }, // 调整下降深度适应竖直模具
                  this.animationDurations.dipping
                );
                
                // 浸泡等待
                await this.createDelayPromise(this.animationDurations.soaking);
                
                // 上升
                await this.createAnimationPromise(
                  this.moldGroup.position,
                  { x: -12, y: 0.6, z: 0 }, // 调整Y轴高度适应竖直模具
                  this.animationDurations.rising
                );
                
                this.processStep = 2;
                this.isProcessing = false;
              });
              break;

            case 2: // 移动到干燥室
              this.isProcessing = true;
              this.addToAnimationQueue(async () => {
                await this.createAnimationPromise(
                  this.moldGroup.position,
                  { x: -4, y: 0.6, z: 0 }, // 调整Y轴高度适应竖直模具
                  this.animationDurations.moveToDrying
                );
                
                this.processStep = 3;
                
                // 干燥过程
                await this.createDelayPromise(this.animationDurations.drying);
                
                // 移动到检测区
                await this.createAnimationPromise(
                  this.moldGroup.position,
                  { x: 12, y: 0.6, z: 0 }, // 调整Y轴高度适应竖直模具
                  this.animationDurations.moveToInspection
                );
                
                this.processStep = 4;
                this.isProcessing = false;
              });
              break;

            case 4: // 检测过程
              if (!this.isInspecting) {
                this.isInspecting = true;
                this.lastInspectionTime = Date.now() * 0.001;
                this.emitAnimationComplete = false; // 重置发送状态
                this.inspectionTime = 2.0; // 重置检测时间
                if (this.inspectionBeam) {
                  this.inspectionBeam.visible = true;
                }
                if (this.inspectionLight) {
                  this.inspectionLight.material.color.setHex(0xff0000);
                  this.inspectionLight.material.emissive.setHex(0xff0000);
                }
                console.log('开始检测过程，预计持续2秒');
              }
              break;
          }
        }

        // 更新数字孪生数据可视化
        this.updateDigitalTwinVisualization();
        
        if (this.renderer && this.scene && this.camera) {
          this.renderer.render(this.scene, this.camera);
        }
      } catch (error) {
        console.error('动画更新失败:', error);
      }
    },

    // 改进的模具移动动画方法
    animateMoldMovement(current, target, duration, callback) {
      const startPosition = { x: current.x, y: current.y, z: current.z };
      const startTime = Date.now();
      let animationId;

      const animate = () => {
        const now = Date.now();
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const easeProgress = this.easeInOutCubic(progress);

        current.x = startPosition.x + (target.x - startPosition.x) * easeProgress;
        current.y = startPosition.y + (target.y - startPosition.y) * easeProgress;
        current.z = startPosition.z + (target.z - startPosition.z) * easeProgress;

        if (progress < 1) {
          animationId = requestAnimationFrame(animate);
        } else {
          if (callback) {
            callback();
          }
        }
      };

      animate();
      
      // 返回一个取消动画的函数
      return () => {
        if (animationId) {
          cancelAnimationFrame(animationId);
        }
      };
    },

    // 缓动函数
    easeInOutCubic(t) {
      return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
    },

    onWindowResize() {
      if (this.camera && this.renderer && this.$refs.container) {
        this.camera.aspect = this.$refs.container.clientWidth / this.$refs.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(
          this.$refs.container.clientWidth,
          this.$refs.container.clientHeight
        );
      }
    },

    disposeScene() {
      if (this.scene) {
        this.scene.traverse((object) => {
          if (object.geometry) {
            object.geometry.dispose();
          }
          if (object.material) {
            if (Array.isArray(object.material)) {
              object.material.forEach(material => material.dispose());
            } else {
              object.material.dispose();
            }
          }
        });
      }
    },

    // 重置动画状态
    resetAnimation() {
      this.isAnimationComplete = false;
      this.emitAnimationComplete = false;
      this.inspectionTime = 2.0;
      this.isInspecting = false;
      this.processStep = 0;
      this.isProcessing = false;
      this.isAnimating = false;
      this.animationQueue = [];
      if (this.moldGroup) {
        this.moldGroup.position.set(
          this.moldStartPosition.x,
          this.moldStartPosition.y,
          this.moldStartPosition.z
        );
      }
    },

    updateDigitalTwinVisualization() {
      // 根据数字孪生参数更新3D模型的视觉效果
      
      // 更新溶胶温度可视化（改变溶胶颜色）
      if (this.dippingTank && this.dippingTank.children[0]) {
        const liquid = this.dippingTank.children[0];
        if (this.temperature > 85) {
          // 温度过高时显示为红色
          liquid.material.color.setHex(0xff3300);
        } else if (this.temperature < 65) {
          // 温度过低时显示为浅蓝色
          liquid.material.color.setHex(0x88ccff);
        } else {
          // 温度正常时显示为正常蓝色
          liquid.material.color.setHex(0x00ffff);
        }
        
        // 根据温度调整透明度
        liquid.material.opacity = Math.min(0.6 + (this.temperature - 65) / 50, 0.8);
      }
      
      // 根据设备状态调整相关组件的颜色
      this.componentStatus.forEach((component, index) => {
        if (component.status !== '正常') {
          // 在3D模型中定位相应组件并改变其视觉样式
          // 这里仅为示例，需要针对具体设备组件进行实现
          switch (component.name) {
            case '溶胶泵':
              // 更新溶胶泵颜色
              break;
            case '液压系统':
              // 更新液压系统颜色
              break;
            case '干燥系统':
              if (this.dryingChamber) {
                const color = component.status === '异常' ? 0xff0000 : 0xffaa00;
                this.dryingChamber.material.emissive.setHex(color);
              }
              break;
            case '传送装置':
              if (this.conveyorGroup) {
                // 更新传送带颜色
              }
              break;
          }
        }
      });
    },

    // 添加面板切换方法
    togglePanel() {
      this.showPanel = !this.showPanel;
    },
  }
};
</script>

<style scoped>
.production-line-3d {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.2);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  font-size: 16px;
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ff4d4f;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

/* 数字孪生面板样式 */
.digital-twin-panel {
  position: absolute;
  bottom: 10px;
  left: 10px;
  width: 250px;
  background: rgba(0, 20, 40, 0.6);
  border-radius: 8px;
  color: #fff;
  font-size: 11px;
  padding: 8px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(24, 144, 255, 0.3);
  box-shadow: 0 0 15px rgba(24, 144, 255, 0.2);
  z-index: 10;
  max-height: calc(70% - 20px);
  overflow-y: auto;
  transition: opacity 0.3s ease;
}

.digital-twin-panel:hover {
  opacity: 1;
  background: rgba(0, 20, 40, 0.8);
}

.panel-section {
  margin-bottom: 10px;
}

.panel-section h3 {
  margin: 0 0 6px 0;
  font-size: 13px;
  color: #1890ff;
  border-bottom: 1px solid rgba(24, 144, 255, 0.5);
  padding-bottom: 3px;
}

.param-item, .prediction-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 3px;
  font-size: 11px;
}

.param-label, .prediction-label {
  color: rgba(255, 255, 255, 0.8);
}

.param-value, .prediction-value {
  font-weight: bold;
}

.alarm {
  color: #ff4d4f;
  animation: blink 1s infinite;
}

.good {
  color: #52c41a;
}

.warning {
  color: #faad14;
}

.bad {
  color: #ff4d4f;
}

.status-normal {
  color: #52c41a;
}

.status-warning {
  color: #faad14;
}

.status-error {
  color: #ff4d4f;
  animation: blink 1s infinite;
}

.device-status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5px;
}

.device-status-item {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  padding: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 10px;
}

.status-icon {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-bottom: 4px;
}

.status-normal .status-icon {
  background-color: #52c41a;
}

.status-warning .status-icon {
  background-color: #faad14;
}

.status-error .status-icon {
  background-color: #ff4d4f;
  animation: blink 1s infinite;
}

.status-name {
  font-size: 11px;
  margin-bottom: 2px;
}

.status-value {
  font-weight: bold;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* 添加面板切换按钮样式 */
.panel-toggle {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 20, 40, 0.7);
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  z-index: 11;
  border: 1px solid rgba(24, 144, 255, 0.5);
  transition: all 0.3s ease;
}

.panel-toggle:hover {
  background: rgba(24, 144, 255, 0.7);
}
</style> 