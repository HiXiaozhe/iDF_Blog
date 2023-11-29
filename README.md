# RChain-iDF_Blog：RChain私人社交网络

<hr/>

## 一、项目文件说明

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
│   ├── config.py  # 配置文件
│   ├── data_helper.py  # 数据处理文件
│   └── rho_deploy.py  # rchain交互文件
├── README.md  # 项目说明文件
├── requirements.txt  # 依赖文件
├── scripts  # 脚本文件夹
│   ├── deploy.py  # 部署智能合约
│   ├── deploy.sh  # 部署智能合约脚本
│   └── run_rnode.sh  # 运行rnode节点脚本
├── session  # 服务端session存储文件夹
├── SNS  # 项目文件夹
│   ├── asgi.py  # 异步服务网关接口
│   ├── __init__.py  # 初始化文件
│   ├── settings.py  # 配置文件
│   ├── urls.py  # 路由配置文件
│   └── wsgi.py  # Web服务网关接口
└──

```

## 二、运行
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