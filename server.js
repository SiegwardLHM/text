const jsonServer = require('json-server');
console.log('json-server loaded');

const server = jsonServer.create();
console.log('server created');

const router = jsonServer.router('db.json');
console.log('router created');

const middlewares = jsonServer.defaults();
console.log('middlewares created');

// 设置默认中间件
server.use(middlewares);
console.log('middlewares applied');

// 添加请求体解析中间件
server.use(jsonServer.bodyParser);
console.log('body parser applied');

// 添加自定义路由
server.use((req, res, next) => {
  console.log('Request:', req.method, req.path);
  console.log('Request body:', req.body);
  
  try {
    if (req.method === 'POST' && req.path === '/login') {
      const { username, password } = req.body;
      const users = router.db.get('users').value();
      const user = users.find(u => u.username === username && u.password === password);
      
      if (user) {
        res.json({
          success: true,
          user: {
            id: user.id,
            username: user.username,
            realname: user.realname,
            department: user.department,
            avatar: user.avatar,
            role: user.role,
            token: 'mock-token-' + Date.now()
          }
        });
      } else {
        res.status(401).json({
          success: false,
          message: '用户名或密码错误'
        });
      }
    } else if (req.method === 'POST' && req.path === '/register') {
      const { username, password, realname, department } = req.body;
      console.log('Register data:', { username, realname, department });
      
      if (!username || !password || !realname || !department) {
        res.status(400).json({
          success: false,
          message: '请填写所有必填字段'
        });
        return;
      }
      
      const users = router.db.get('users').value();
      
      if (users.some(u => u.username === username)) {
        res.status(400).json({
          success: false,
          message: '用户名已存在'
        });
        return;
      }
      
      const newUser = {
        id: Date.now(),
        username,
        password,
        realname,
        department,
        avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        role: 'user'
      };
      
      users.push(newUser);
      router.db.set('users', users).write();
      
      res.json({
        success: true,
        user: {
          ...newUser,
          token: 'mock-token-' + Date.now()
        }
      });
    } else {
      next();
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      message: '服务器内部错误',
      error: error.message
    });
  }
});
console.log('custom routes added');

// 使用默认路由
server.use(router);
console.log('default router applied');

// 启动服务器
server.listen(3000, () => {
  console.log('Server is running on port 3000');
  console.log('Resources available at:');
  console.log('http://localhost:3000/users');
}); 