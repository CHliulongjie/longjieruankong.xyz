"""
简化的数据库创建脚本
"""
import sqlite3
import os

BASE_DIR = r'd:\临时\代码重构工程\longjieruankong.xyz'
OLD_DB_PATH = os.path.join(BASE_DIR, 'data', 'users.db')

# 创建目录
accounts_dir = os.path.join(BASE_DIR, 'accounts')
permissions_dir = os.path.join(BASE_DIR, 'permissions')
os.makedirs(accounts_dir, exist_ok=True)
os.makedirs(permissions_dir, exist_ok=True)

print("[OK] 目录创建完成")

# 创建用户数据库
users_db = os.path.join(accounts_dir, 'users.db')
conn = sqlite3.connect(users_db)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(120) NOT NULL,
        uid VARCHAR(50) UNIQUE NOT NULL,
        register_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print("[OK] 用户数据库创建完成")

# 创建管理员数据库
admin_db = os.path.join(accounts_dir, 'admin.db')
conn = sqlite3.connect(admin_db)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(120) NOT NULL,
        uid VARCHAR(50) UNIQUE NOT NULL,
        admin_level VARCHAR(20) DEFAULT 'admin',
        register_date TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print("[OK] 管理员数据库创建完成")

# 创建作业管理系统权限数据库
homework_perms_db = os.path.join(permissions_dir, 'homework_permissions.db')
conn = sqlite3.connect(homework_perms_db)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE homework_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid VARCHAR(50) UNIQUE NOT NULL,
        permissions TEXT NOT NULL DEFAULT '.',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print("[OK] 作业管理系统权限数据库创建完成")

# 创建场馆预约系统权限数据库
reservation_perms_db = os.path.join(permissions_dir, 'reservation_permissions.db')
conn = sqlite3.connect(reservation_perms_db)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE reservation_permissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid VARCHAR(50) UNIQUE NOT NULL,
        permissions TEXT NOT NULL DEFAULT '.',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()
print("[OK] 场馆预约系统权限数据库创建完成")

# 迁移管理员数据
print("\n迁移管理员数据...")
old_conn = sqlite3.connect(OLD_DB_PATH)
old_cursor = old_conn.cursor()
new_conn = sqlite3.connect(admin_db)
new_cursor = new_conn.cursor()

old_cursor.execute("SELECT username, password, roles FROM users WHERE roles LIKE '%admin%'")
admins = old_cursor.fetchall()

for username, password, roles in admins:
    if username == 'admin201030':
        uid = 'LJRK-SFQD-0000000000'
        admin_level = 'super_admin'
        register_date = '2025-01-01'
    elif username == '刘懿旭':
        uid = 'LJRK-SFQD-0000000001'
        admin_level = 'admin'
        register_date = '2025-01-01'
    else:
        uid = f'LJRK-SFQD-250327{len(username):04d}'
        admin_level = 'admin'
        register_date = '2025-03-27'

    try:
        new_cursor.execute(
            "INSERT INTO admins (username, password, uid, admin_level, register_date) VALUES (?, ?, ?, ?, ?)",
            (username, password, uid, admin_level, register_date)
        )
        print(f"  [OK] {username} -> {uid}")
    except:
        print(f"  ✗ {username} 已存在")

new_conn.commit()
new_conn.close()
old_conn.close()

# 迁移普通用户数据
print("\n迁移普通用户数据...")
old_conn = sqlite3.connect(OLD_DB_PATH)
old_cursor = old_conn.cursor()
new_conn = sqlite3.connect(users_db)
new_cursor = new_conn.cursor()

old_cursor.execute("SELECT username, password FROM users WHERE roles NOT LIKE '%admin%'")
users = old_cursor.fetchall()

for i, (username, password) in enumerate(users, start=1):
    uid = f'LJRK-SFQD-250327{i:04d}'
    register_date = '2025-03-27'

    try:
        new_cursor.execute(
            "INSERT INTO users (username, password, uid, register_date) VALUES (?, ?, ?, ?)",
            (username, password, uid, register_date)
        )
        print(f"  [OK] {username} -> {uid}")
    except:
        print(f"  ✗ {username} 已存在")

new_conn.commit()
new_conn.close()
old_conn.close()

# 添加超级管理员权限
print("\n添加超级管理员权限...")
super_admin_uid = 'LJRK-SFQD-0000000000'

conn = sqlite3.connect(homework_perms_db)
cursor = conn.cursor()
cursor.execute("INSERT OR IGNORE INTO homework_permissions (uid, permissions) VALUES (?, ?)", (super_admin_uid, '*'))
conn.commit()
conn.close()

conn = sqlite3.connect(reservation_perms_db)
cursor = conn.cursor()
cursor.execute("INSERT OR IGNORE INTO reservation_permissions (uid, permissions) VALUES (?, ?)", (super_admin_uid, '*'))
conn.commit()
conn.close()

print("[OK] 权限设置完成")

print("\n" + "=" * 80)
print("[OK] Migration completed!")
print("=" * 80)
