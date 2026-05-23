# 账户和权限系统重构文档

## 📁 新的目录结构

```
longjieruankong.xyz/
├── accounts/                      # 账户数据目录
│   ├── admin.db                  # 管理员账户数据库
│   └── users.db                  # 普通用户账户数据库
├── permissions/                   # 权限数据目录
│   ├── homework_permissions.db    # 作业管理系统权限
│   └── reservation_permissions.db # 场馆预约系统权限
└── data/                         # 旧数据目录（保留）
    ├── users.db                  # 旧用户数据库
    └── users_backup.db          # 备份
```

## 🎯 设计目标

1. **分离账户数据和权限数据**：账户信息和权限配置分开管理
2. **统一识别码**：每个账户拥有唯一的识别码（UID）
3. **独立权限管理**：每个应用有独立的权限数据库
4. **灵活的权限配置**：支持不同级别的权限设置

## 🔑 识别码（UID）格式

```
LJRK-SFQD-YYMMDDXXXX
```

- `LJRK-SFQD-`：固定前缀
- `YY`：注册年份（2位）
- `MM`：注册月份（2位）
- `DD`：注册日期（2位）
- `XXXX`：当日注册序号（4位）

### 特殊账号识别码

| 账号 | 识别码 | 说明 |
|------|--------|------|
| admin201030 | LJRK-SFQD-0000000000 | 超级管理员（万能权限） |
| 刘懿旭 | LJRK-SFQD-0000000001 | 系统管理员 |

## 📊 数据库表结构

### 1. 管理员账户数据库 (`accounts/admin.db`)

```sql
CREATE TABLE admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,     -- 用户名（唯一）
    password VARCHAR(120) NOT NULL,           -- 密码
    uid VARCHAR(50) UNIQUE NOT NULL,          -- 识别码
    admin_level VARCHAR(20) DEFAULT 'admin',  -- 管理员级别: super_admin, admin
    register_date TEXT,                       -- 注册日期 (YYYY-MM-DD)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP -- 创建时间
);
```

**管理员级别说明：**
- `super_admin`：超级管理员，拥有所有权限（识别码固定为 LJRK-SFQD-0000000000）
- `admin`：普通管理员，拥有部分管理权限

### 2. 普通用户账户数据库 (`accounts/users.db`)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,     -- 用户名（唯一）
    password VARCHAR(120) NOT NULL,            -- 密码
    uid VARCHAR(50) UNIQUE NOT NULL,          -- 识别码
    register_date TEXT,                       -- 注册日期 (YYYY-MM-DD)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP  -- 创建时间
);
```

### 3. 权限数据库（每个应用独立）

```sql
CREATE TABLE {app}_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(50) UNIQUE NOT NULL,          -- 用户识别码
    permissions TEXT NOT NULL DEFAULT '.',    -- 权限配置
    created_at TEXT DEFAULT CURRENT_TIMESTAMP, -- 创建时间
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP  -- 更新时间
);
```

**权限配置说明：**
- `*`：万能权限（所有权限）
- `.`：最低权限（无任何权限）
- 自定义权限：根据应用需求定义

### 当前权限数据库列表

| 应用 | 数据库文件 | 说明 |
|------|-----------|------|
| 作业管理系统 | `permissions/homework_permissions.db` | 管理作业相关的权限 |
| 场馆预约系统 | `permissions/reservation_permissions.db` | 管理场馆预约的权限 |

## 👥 现有账户迁移结果

### 管理员账户（3个）

| 用户名 | 识别码 | 级别 | 注册日期 |
|--------|--------|------|----------|
| admin201030 | LJRK-SFQD-0000000000 | super_admin | 2025-01-01 |
| admin | LJRK-SFQD-2503270005 | admin | 2025-03-27 |
| admin刘 | LJRK-SFQD-2503270006 | admin | 2025-03-27 |

### 普通用户账户（8个）

| 用户名 | 识别码 | 注册日期 |
|--------|--------|----------|
| 刘懿旭 | LJRK-SFQD-2503270001 | 2025-03-27 |
| heidi | LJRK-SFQD-2503270002 | 2025-03-27 |
| 汤文博 | LJRK-SFQD-2503270003 | 2025-03-27 |
| 吴菲涵 | LJRK-SFQD-2503270004 | 2025-03-27 |
| 测试员1 | LJRK-SFQD-2503270005 | 2025-03-27 |
| 胡雨辰 | LJRK-SFQD-2503270006 | 2025-03-27 |
| jimmy | LJRK-SFQD-2503270007 | 2025-03-27 |
| 杨子轩 | LJRK-SFQD-2503270008 | 2025-03-27 |

## ⚙️ 权限验证流程（待实现）

### 登录流程

```
1. 客户端提交登录信息（用户名、密码）
2. 服务器验证账号密码
   - 失败：返回错误信息（用户名不存在、密码错误等）
   - 成功：获取用户识别码（UID）
3. 服务器查询权限数据库
   - 如果权限存在：返回权限数据
   - 如果权限不存在：
     a. 将用户UID添加到权限数据库
     b. 设置默认权限为 "."（最低权限）
     c. 返回默认权限
```

### 权限检查流程（待实现）

```
1. 客户端请求需要权限的操作
2. 服务器检查用户识别码
3. 查询权限数据库获取权限配置
4. 根据权限配置决定是否允许操作
```

## 📝 待办事项

1. ✅ 创建数据库结构（已完成）
2. ✅ 迁移现有账户数据（已完成）
3. ⏳ 修改应用代码以使用新的数据库结构
4. ⏳ 实现权限验证逻辑
5. ⏳ 测试登录功能
6. ⏳ 测试权限验证功能

## 🛠️ 相关脚本

- `simple_migrate.py`：数据库迁移脚本（已执行）
- `verify_db.py`：验证数据库结构脚本

## 📌 注意事项

1. **识别码唯一性**：每个账户的识别码在整个系统中唯一
2. **权限分离**：不同应用的权限独立管理
3. **默认权限**：新用户首次访问某个应用时，默认权限为 "."（最低权限）
4. **数据备份**：建议在修改前备份原有数据

## 🔒 安全性说明

1. **密码存储**：当前为明文存储，建议后续加密存储
2. **识别码分配**：识别码由系统自动生成，不可重复
3. **权限控制**：通过识别码关联权限，支持细粒度控制

## 📞 联系方式

如有问题，请联系：刘懿旭
