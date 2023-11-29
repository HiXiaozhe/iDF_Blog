# iDF_Blog：私人社交网络平台

## 一、项目概述

&emsp;&emsp;iDF_Blog是一款基于python的Django框架开发的全栈私人社交网络平台，
前端使用Bootstrap框架搭建响应式用户界面，后端数据采用RChain区块链进行分布式部署。
本项目旨在开发一个去中心化的社交媒体平台，通过分布式技术、加密算法和区块链技术等现代信息技术，
实现传统社交媒体平台的去中心化，提供更安全、私密、去中心化的社交交互平台。
本软件可以提供类似微博或朋友圈的功能，基本功能包括但不限于注册登录、发送动态、点赞回复、动态浏览等此外还有包括数字货币交易和激励机制、关注和粉丝功能等，
最大程度上开发出让用户满意的安全的去中心化社交平台。

## 二、平台主页

访问以下地址以开启您的私人社交网络
```
http://182.92.119.200:8000/index/
```

## 三、项目文件说明

```
├── app  # 应用文件夹
│   ├── admin.py  # 后台管理
│   ├── apps.py  # 应用配置
│   ├── form.py  # 表单文件
│   ├── __init__.py  # 初始化文件
│   ├── middleware  # 中间件
│   ├── migrations  # 数据迁移文件
│   ├── models.py  # 数据模型
│   ├── static  # 静态文件
│   ├── templates  # 模板文件
│   ├── tests.py  # 单元测试文件
│   ├── utils  # 工具文件
│   └── views.py  # 视图函数
├── kumo.ttf  # 字体文件
├── manage.py  # 项目管理文件
├── RChain  # RChain文件夹
│   ├── config.conf  # rchain配置文件
│   ├── rchain-release  # rchain可执行文件
│   └── rnode0  # rnode数据存储文件夹
├── RChainAPI  # RChainAPI文件夹
│   ├── config.py  # RchainAPI配置文件
│   ├── data_helper.py  # 数据处理文件
│   └── rho_deploy.py  # rchain交互文件
├── README.md  # 项目说明文件
├── requirements.txt  # 项目依赖文件
├── scripts  # 脚本文件夹
│   ├── deploy.py  # 部署智能合约
│   ├── deploy.sh  # 部署智能合约脚本
│   └── run_rnode.sh  # 运行rnode节点脚本
├── session  # 服务端session存储文件夹
├── SNS  # 项目文件夹
│   ├── asgi.py  # 异步服务网关接口
│   ├── __init__.py  # 初始化文件
│   ├── settings.py  # 项目配置文件
│   ├── urls.py  # 路由配置文件
│   └── wsgi.py  # Web服务网关接口
└──

```

## 四、运行

- 安装依赖（按照个人情况配置）

```shell
pip install -r requirements.txt
```

- 运行rnode节点部署智能合约

```shell
cd ./scripts
bash run_rnode.sh
bash deploy.sh
```

- 运行项目（仅本地测试）

```shell
python manage.py runserver
# 本地进入网址使用：http://127.0.0.1:8000/
```

- 运行项目（服务器端运行）

```shell
python manage.py runserver 0.0.0.0:8000
# 客户端进入网址使用：http:// + 服务器公网IP + :8000/
```