# meiduo_mall
美多商城项目学习笔记

## 项目准备

### 项目需求分析

#### 项目页面接收

1. 首页广告

    ![image-20230326174541197](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261745461.png)

2. 注册

    ![image-20230326174555670](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261745759.png)

3. 登录

    ![image-20230326175036331](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261750430.png)

4. QQ登录

    ![](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261750844.png)

5. 个人信息

    ![image-20230326175008906](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261750979.png)

6. 收货地址

    ![image-20230326174959870](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749924.png)

7. 我的订单

    ![image-20230326174950620](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749684.png)

8. 修改密码

    ![image-20230326174939065](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749137.png)

9. 商品列表

    ![image-20230326174930918](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749001.png)

10. 商品搜素

    ![image-20230326174922055](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749119.png)

11. 商品详情

    ![image-20230326174913169](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749249.png)

12. 购物车

    ![image-20230326174901643](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261749733.png)

13. 结算订单

    ![image-20230326174851939](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261748006.png)

14. 提交订单

    ![image-20230326174842075](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261748128.png)

15. 支付宝支付

    ![](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261748867.png)

16. 支付结果处理

    ![image-20230326174813749](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261748810.png)

17. 订单商品评价

    ![image-20230326174806229](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261748297.png)

#### 归纳主要模块

|    模块    |                       功能                       |
| :--------: | :----------------------------------------------: |
|    验证    |                图形验证，短信验证                |
|    用户    |               注册、登录、用户中心               |
| 第三方登录 |                      QQ登录                      |
|  首页广告  |                     首页广告                     |
|    商品    |           商品列表、商品搜索、商品详情           |
|   购物车   |              购物车管理、购物车合并              |
|    订单    |                确认订单、提交订单                |
|    支付    |             支付宝支付、订单商品评价             |
|  MIS系统   | 数据统计、用户管理、权限管理、商品管理、订单管理 |

### 项目架构设计

#### 项目开发模式

| 选项     | 技术选型              |
| -------- | --------------------- |
| 开发模式 | 前后端不分离          |
| 后端框架 | Django+jinja2模板引擎 |
| 前端框架 | Vue.js                |

#### 项目运行机制

![image-20230326175510848](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261755976.png)

#### 知识要点

1. 项目开发模式
    1. 前后端不分离，方便SEO
    2. 采用Django+jinja2模板引擎+Vue.js实现前后端逻辑
2. 项目运行机制
    1. 代理服务：Nginx服务器（反向代理）
    2. 静态服务：Nginx服务器（静态首页，商品详情页等）
    3. 动态服务：uwsgi服务器（美多商城业务场景）
    4. 后端服务：MySQL、Redis、Celery、RabbitMQ、Docker、FastDFS、ElasticSearch、Contab
    5. 外部接口：容联云、QQ互联、支付宝

### 工程创建和配置

#### 新建配置文件

1. 准备配置文件目录
    1. 新建包。命名为settings，作为配置目录
2. 准备开发和生产环境配置文件
    1. 在新建包settings中，新建开发和生产环境配置文件
3. 准备开发环境配置内容
    1. 将默认的配置文件`settings.py`中内容拷贝至`settings-dev.py`中

![image-20230326181141385](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261811528.png)

#### 指定开发环境配置文件

![image-20230326181252615](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261812762.png)

#### 配置jinja2模板引擎

##### 安装jinja2扩展包

~~~shell
pip install jinja2==2.0.1
~~~

##### 配置Jinja2模板引擎

~~~Python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',  # 配置jinja2模板引擎
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 配置模板文件路径
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 补充jinja2模板环境
            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment'
        },
    },
]
~~~

##### 补充Jinja2模板引擎环境

1. 在utils包中新建`jinja2_env.py`文件

    ~~~python 
    from django.contrib.staticfiles.storage import staticfiles_storage
    from django.urls import reverse
    from jinja2 import Environment
    
    
    def jinja2_environment(**options):
        env = Environment(**options)
        env.globals.update({
            'static': staticfiles_storage.url,
            'url': reverse,
        })
        return env
    
    """
    确保可以使用模板引擎中的{{ url('') }} {{ static('') }}这类语句 
    """
    ~~~

#### 配置MySQL数据库

1. 配置MySQL数据库

    ~~~Python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
            'NAME': 'meiduo',  # 你要存储数据的库名，事先要创建
            'USER': 'root',  # 数据库用户名
            'PASSWORD': 'zhouwei1997',  # 密码
            'HOST': 'localhost',  # 主机
            'PORT': '3306',  # 数据库使用的端口
        }
    }
    ~~~

2. 安装PyMySQL扩展包

    ~~~shell
    pip install PyMySQL
    ~~~

3. 在工程同名的子目录的`__init__.py`文件中，添加如下代码

    ~~~Python
    # 配置mysql数据库
    import pymysql
    
    pymysql.install_as_MySQLdb()
    ~~~

#### 配置redis数据库

1. 安装djang-redis扩展包

    ~~~shell
    pip install django-redis
    ~~~

2. 配置Redis数据库

    ~~~Python
    # 配置redis缓存
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # "PASSWORD":
            }
        },
        # session
        "session": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # "PASSWORD":
            }
        },
        # 验证码
        "verify_code": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # "PASSWORD":
            }
        }
    }
    # 配置session的引擎
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "session"
    ~~~

    | 参数配置            | 说明                                              |
    | ------------------- | ------------------------------------------------- |
    | default             | 默认的Redis配置项，采用0号Redis库                 |
    | session             | 状态保持的Redis配置项，采用1号Redis库             |
    | verify_code         | 验证码的Redis配置项，采用2号Redis库               |
    | SESSION_ENGINE      | 修改`session存储机制`使用Redis保存                |
    | SESSION_CACHE_ALIAS | 使用名为"session"的Redis配置项存储`session数据`。 |

    #### 配置工程日志

##### 配置工程日志

~~~Python
"""
配置日志
"""
cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s]' '%(message)s'
        },
        'simple': {  # 简单格式
            'format': '[%(levelname)s] [%(module)s:%(funcName)s]' '%(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [%(module)s:%(funcName)s]' '%(message)s'
        },
    },
    # 过滤
    'filters': {
        # django在debug模式下才输出日志
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    # 定义具体处理日志的方式
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(log_path, 'meiduo_mall-{}.log'.format(time.strftime('%Y-%m-%d'))),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,  # 文件大小  300M
            'backupCount': 10,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
~~~

##### 日志记录器的使用

~~~Python
import logging

# 创建日志记录器
logger = logging.getLogger('django')
# 输出日志
logger.debug('测试logging模块debug')
logger.info('测试logging模块info')
logger.error('测试logging模块error')
~~~

##### 知识要点

1. 本项目最低日志几杯设置为：INFO

2. 创建日志记录器的方式

    ~~~Python
    # django   日志记录器的名称
    logger = logging.getLogger('django')
    ~~~

3. 日志记录器的使用

    ~~~Python
    logger.info('测试logging模块info')
    ~~~

4. 在日志`loggers`选项中可以指定多个日志记录器

#### 配置前端静态文件

##### 准备静态文件

在项目根目录新建`static`目录，将静态文件`js`、`css`、`images`存放在该目录中

![image-20230326183420227](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261834298.png)

##### 指定静态文件加载路径

~~~Python
STATIC_URL = '/static/'
# 配置静态文件位置
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
~~~

#### 配置时区和语言

~~~Python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
~~~

## 用户注册



### 展示用户注册页面

#### 创建用户模块子应用

1. 准备`apps`包，并mark为`namespace Package`

    ![image-20230326184118894](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261841026.png)

    ![image-20230326184138433](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261841504.png)

2. 在`apps`包下创建子应用`user`

    ~~~shell 
    cd ~/projects/meiduo_project/meiduo_mall/meiduo_mall/apps
    python ../../manage.py startapp users
    ~~~

    ![image-20230326184250512](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261842576.png)

3. 注册用户模块子应用

    ~~~Python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'users',  # 用户模块
    ]
    ~~~

#### 追加导包路径

    ~~~Python
    sys.path.append(os.path.join(BASE_DIR, 'apps'))
    ~~~

#### 展示用户注册页面

##### 准备用户注册模板文件

在项目根目录新建`templates`目录，并mark为`Template Folder`

![image-20230326184559639](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261845701.png)

​    ![image-20230326184702147](https://zhouwei-images.oss-cn-hangzhou.aliyuncs.com/202303261847220.png)

##### 加载页面静态文件

~~~HTML
<head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <title>美多商城-注册</title>
    <link rel="stylesheet" type="text/css" href="{{ static('css/reset.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ static('css/main.css') }}">
    <script type="text/javascript" src="{{ static('js/vue-2.5.16.js') }}"></script>
    <script type="text/javascript" src="{{ static('js/axios-0.18.0.min.js') }}"></script>
</head>
~~~

##### 定义用户注册视图

~~~Python
class RegisterView(View):
    """用户注册"""

    def get(self, request):
        """
        提供注册界面
        :param request: 请求对象
        :return: 注册界面
        """
        return render(request, 'register.html')
~~~

##### 定义用户注册路由

###### 总路由

~~~Python
urlpatterns = [
    # users
    url(r'^', include('users.urls', namespace='users')),
]
~~~

###### 子路由

~~~Python
urlpatterns = [
    # 用户注册   reverse(user:register) == '/register/'
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
]
~~~

### 定义用户模型类

#### Django默认用户认证系统

- Django自带用户认证系统
    - 它处理用户账号、组、权限以及基于cookie的用户会话
- Django认证系统位置
    - `django.contrib.auth`包含认证框架的核心和默认的模型
    - `django.contrib.contenttypes`是Django内容类型系统，它允许权限与创建的模型关联
- Django认证系统同时处理认证和授权
    - 认证：验证一个用户是否它声称的那个人，可用于账号登录。
    - 授权：授权决定一个通过了认证的用户被允许做什么。
- Django认证系统包含的内容
    - 用户：**用户模型类**、用户认证。
    - 权限：标识一个用户是否可以做一个特定的任务，MIS系统常用到。
    - 组：对多个具有相同权限的用户进行统一管理，MIS系统常用到。
    - 密码：一个可配置的密码哈希系统，设置密码、密码校验。
