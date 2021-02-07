# flask-register-login
flask-register-login
## 一、配置项目环境
```
1. 配置项目虚拟环境
2. 使用git管理代码
3. 项目框架搭建
```
## 二、创建项目入口文件，manager.py
## 三、项目基本配置
```python
# flask加载配置的三种方法，我们使用从配置对象中加载的方式
# 设置配置文件、文件夹  设置项目需要的配置项的位置
```
### 1 我们使用SQLAlchemy需要配置数据库的相关配置项
```python
# 数据库的配置信息,
# 配置MySQL数据库连接信息:真实开发中，要使用mysql数据库的真实IP
SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/restful"
# 不去追踪数据库的修改，节省开销
SQLALCHEMY_TRACK_MODIFICATIONS = False
```
- 在终端创建数据库，或者在navicat创建数据库，已备数据库迁移生成响应的数据库表
### 2 创建redis存储对象，并在配置中填写相关配置
```python
# 配置redis数据库:因为redis模块不是flask的扩展，所以就不会自动的从config中读取配置信息，只能自己读取
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
```
### 3 利用 flask-session扩展，将 session 数据保存到 Redis 中，加入session相关配置

- flask原本的session是保存在浏览器cookie中的，这样就产生了一个很重要的问题，如果我们在session中不存敏感信息还好，
如果存的是敏感信息那么信息安全是没有保障的，而flask_session可以让我们把session的值存储在redis/Memcached中。
```python
# flask_session的配置信息
SESSION_TYPE = "redis" # 指定 session 保存到 redis 中
SESSION_USE_SIGNER = True # 让 cookie 中的 session_id 被加密签名处理
SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT) # 使用 redis 的实例
PERMANENT_SESSION_LIFETIME = 24 * 60 * 60 # session 的有效期，单位是秒
# SESSION_COOKIE_NAME 设置session在浏览器中的key的值  默认是'session', 设置该配置可以修改对应的名字

```
- 需要配置SECRET_KEY,可以通过下面的方法取到相对强壮的密钥
```python
import os
os.urandom(24)
```
## 四 管理app
- 创建连接到数据库的对象
- 创建连接到redis的对象
- 创建Session对象,关联app

## 五 Flask-Script与数据库迁移扩展
```python
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)
```

## 六 代码抽取
- 目标：将特定逻辑代码抽取到指定的类中，各司其职，放便后续项目维护
#### 业务逻辑独立
在整个项目文件夹中，除了启动文件 manager.py 和配置文件 config 放在根目录，
其他具体业务逻辑文件都放在一个单独的文件夹内，与 manager.py 同级

- 创建 core Package，与 manager.py 同级
- manager.py 只做最基本的启动工作，将 app 的创建操作移动到 core 的`__init__.py`文件中

## 七 项目多种配置
一个web程序在开发阶段与生产阶段所需要的配置信息可能是不一样的，故此，为了实现解耦此功能，可以给不同开发情况创建不同的配置类，
比如咱们开发阶段使用的配置类名为 DevelopementConfig，生产阶段使用的配置类名为 ProdutionConfig，测试阶段使用的配置类名为 UnittestConfig

后期我们在不同的阶段可以加载不同的配置

## 八 工厂类方法创建应用实例
已经有了多种配置类，要在不同环境下去使用不同的配置，那么可以在 manager.py 文件中给 core 包传入不同的配置信息，这样根据传入指定配置再去创建 app，
所以可以在 info 的 `__init__.py` 文件中添加一个工厂方法，根据传入的配置不同创建其对应的应用实例
- 在 config.py 文件中添加以下代码
```python
# 定义配置字典
config = {
    "development": DevelopementConfig,
    "production": ProductionConfig,
    "test": UnittestConfig,
}
```
- 修改 core 文件夹下 `__init__.py`，添加 create_app 的工厂方法
- 修改 manager.py 文件中的代码
- 将 `__init__.py` 文件中创建 app 实例的方法移动到 create_app 方法中

## 九 日志
```python
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG) # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)
```
- 配置文件中，配置添加日志级别
- 在 core 目录下创建 utils 目录，在其下创建 log_utils.py 文件中添加日志配置的相关方法
- 在 create_app 方法中调用上一步创建的方法，并传入 config_name
- 在项目根目录下创建日志目录文件夹 logs，ignore忽略log文件，避免提交到git上

## 十 蓝图
- 创建蓝图对象
```python
admin=Blueprint('admin',__name__)
```
- 在这个蓝图对象上进行操作  注册路由
```python
@admin.route('/')
def admin_home():
    return 'admin_home'
```
- 在应用对象上注册这个蓝图对象
```python
app.register_blueprint(admin,url_prefix='/admin')
```

## 十一 设计数据库，数据库迁移，生成数据库表
- 创建models.py文件
- 数据库迁移，生成数据库表结构

## 十二 接口编写
### 注册接口
##### 接口功能
> 用户注册

##### URL
> http://127.0.0.1:5000/passport/register/

##### 支持格式
> JSON

##### HTTP请求方式
> POST

##### 请求参数
> | 参数名   | 是否必须 | 类型   | 说明   |
> | -------- | -------- | ------ | ------ |
> | mobile | True     | string | 手机号 |
> | password | True     | string | 密码   |

##### 返回字段
> | 返回字段    | 字段类型 | 说明                               |
> | ----------- | -------- | ---------------------------------- |
> | code  | string   | 返回结果状态。0：正常；-1：错误,。 |
> | msg         | string   | 状态说明                           |

##### 接口示例

> 地址：http://127.0.0.1:5000/passport/register/
```python
{"code": "0",  "msg": "success"} 
```
......

## 十三 接口控制，用户登陆状态才能访问  状态保持
- 接口控制，写入判断，查询用户是否登陆
```python
# 获取用户编号, 登陆之后会在session中存储，我们在session中取出userid查询是否存在该用户
# 如果查不到该用户，即用户没有登陆，用户不存在，不能访问接口
user_id = session.get("user_id")
# 查询用户对象
user = None
if user_id:
    try:
        user = UserLogin.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
if not user:
    return jsonify(response_code.user_not_exist)
```
- 采用装饰器，控制多个接口，避免多个接口都得写相同冗余的代码
    - 在utils创建common.py 编写装饰器函数，装饰需要验证登陆状态的接口
    - 装饰器函数, 用g变量保存登陆用户，如果接口需要可以直接通过应用上下文对象g变量拿到
        ```python
            def user_login_data(view_func):
                @wraps(view_func)
                def wrapper(*args, **kwargs):
                    # 获取用户编号
                    user_id = session.get("user_id")
                    # 查询用户对象
                    user = None
                    if user_id:
                        try:
                            from core.models import UserLogin
                            user = UserLogin.query.get(user_id)
                        except Exception as e:
                            current_app.logger.error(e)
            
                    # 使用g对象保存
                    g.user = user
            
                    return view_func(*args, **kwargs)
            
                return wrapper
        ```
## 十四 User中密码的明文问题
- 由于对密码要进行加密,并且不期望被外界调用,
所以,将密码设置为私有属性,利用@property和@password.setter设置两发方法为属性,以便外界调用(加密后,非明文)
    - Werkzeug中的security模块可以很方便的实现哈希值的计算，只需要两个函数，分别用于用户注册和用户验证阶段

        - generate_password_hash(password,method=pbkdf2:sha1,salt_length=8)：
        这个函数将原始密码作为输入，以字符串形式输出密码的哈希值。method和salt_length的默认值能满足大多数需求

        - check_password_hash(hash,password)：这个函数参数是哈希值和用户输入的密码。返回值为True表示密码正确

```python
    # 设置访问密码的方法,并用装饰器@property设置为属性,调用时不用加括号
    @property
    def password(self):
        return self._password
        # raise AttributeError("当前属性不可读")
	
    # 设置加密的方法,传入密码,对类属性进行操作
    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)
	
    # 设置验证密码的方法
    def check_password(self, user_pwd):
        return check_password_hash(self._password, user_pwd)

```
## 十五 状态保持

flask的session是基于cookie的会话保持。简单的原理即：

当客户端进行第一次请求时，客户端的HTTP request（cookie为空）到服务端，服务端创建session，视图函数根据form表单填写session，
请求结束时，session内容填写入response的cookie中并返回给客户端，客户端的cookie中便保存了用户的数据。

当同一客户端再次请求时， 客户端的HTTP request中cookie已经携带数据，视图函数根据cookie中值做相应操作（如已经携带用户名和密码就可以直接登陆）。

flask原本的session是保存在浏览器cookie中的，这样就产生了一个很重要的问题，如果我们在session中不存敏感信息还好，
如果存的是敏感信息那么信息安全是没有保障的，而flask_session可以让我们把session的值存储在redis/Memcached中。


REST 原则是，客户端和服务器之间的交互在请求之间是无状态的。

不能使用cookie，不能使用session了。restful api的风格不允许这样

token方式完成状态保持：

1. 首次登录，服务器可以拿到用户名，密码信息
2. 验证通过后，可以加密用户信息，生成token值
3. token存储在redis中，记录对应的用户，然后发送给客户端
4. 客户端收到token值，下次访问服务端任何接口的时候，直接携带token服务器端就知道是谁了
5. 客户端可以把token值放在header里或者body里都是可以的

## 十六 token方式接口编写
- 注册接口：
    - 生成token
    - 存储在redis
- 登陆接口：
    - 同注册接口，让前端能收到token值，服务器端也存储了。
- 其他接口，访问的时候携带着token就可以状态保持了

增加登陆验证装饰器，通过前端拿到的token验证接口是否处于登陆状态
```python
def login_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify(response_code.user_not_exist)

        user_id = redis_store.get('token:%s' % token)
        if not user_id or token != redis_store.hget('user:%s' % user_id, 'token'):
            return jsonify(response_code.check_data_error)

        return f(*args, **kwargs)

    return decorator
```
客户端每次请求都需要携带着token，设置应用上下文对象g变量存储用户信息，在请求钩子中做相应处理
```python
@app.before_request
def before_request():
    token = request.headers.get('token')
    user_id = redis_store.get('token:%s' % token)
    if user_id:
        from core.models import UserLogin
        g.current_user = UserLogin.query.get(user_id)
        g.token = token
    return
```

## 生成token的方法
- hashlib.md5() md5加密算法
    - 没有加盐
    ```python
    import hashlib
    
    md5_obj = hashlib.md5()
    md5_obj.update('123456'.encode('utf-8'))
    print(md5_obj.hexdigest())
    ```
    - 加盐
    ```python
    import hashlib

    salt = '1234'
    md5_obj = hashlib.md5(salt.encode('utf-8'))
    md5_obj.update('123456'.encode('utf-8'))
    print(md5_obj.hexdigest())
    ```
- jwt
    - 增加auth模块
    - 优化模型方法，方便去除冗余代码
    - 添加Auth类，增加生成token，验证token，用户登录，用户鉴权方法
- flask_jwt_extended

## 增加反爬机制，简单去除一般爬虫的侵袭
- 请求头无UA
- 请求过于频繁