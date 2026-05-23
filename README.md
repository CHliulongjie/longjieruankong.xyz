# 龙解软控 - XYZ 服务器

> **⚠️ 测试版本** - 此版本为测试版本，不代表最终结果。

## 项目简介

龙解软控 XYZ 服务器，专注于作业管理系统 API 服务。

## 当前版本修改内容

1. 合并了 `/login` 和 `/login1` 接口为统一登录接口
2. 重构了账户和权限系统
3. 分离了管理员和普通用户数据库
4. 实现了基于识别码(UID)的权限管理
5. 删除了已迁移到 top 服务器的 web 服务代码

## 技术栈

- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite
- Waitress

## 快速开始

```bash
pip install -r requirements.txt
python app.py
```

## 项目结构

```
├── app.py              # 主应用入口
├── accounts/           # 账户数据库
│   ├── admin.db        # 管理员数据库
│   └── users.db        # 普通用户数据库
├── permissions/        # 权限数据库
│   ├── homework_permissions.db
│   └── reservation_permissions.db
├── data/               # 作业数据
└── README.md           # 项目说明
```

## 核心 API

| 接口 | 方法 | 描述 |
|------|------|------|
| `/login` | POST | 用户登录 |
| `/register` | POST | 用户注册 |
| `/users` | GET | 获取用户列表 |
| `/classes` | GET | 获取班级列表 |
| `/assignments` | GET | 获取作业列表 |
| `/upload` | POST | 上传作业文件 |

## 许可证

MIT License