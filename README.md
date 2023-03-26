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

    
