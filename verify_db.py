"""
验证迁移结果
"""
import sqlite3
import os

BASE_DIR = r'd:\临时\代码重构工程\longjieruankong.xyz'

print("=" * 80)
print("验证新的数据库结构")
print("=" * 80)

# 管理员数据库
print("\n[1] 管理员数据库 (accounts/admin.db)")
print("-" * 80)
conn = sqlite3.connect(os.path.join(BASE_DIR, 'accounts', 'admin.db'))
cursor = conn.cursor()
cursor.execute("SELECT username, uid, admin_level, register_date FROM admins")
admins = cursor.fetchall()
print(f"共有 {len(admins)} 个管理员:")
for admin in admins:
    print(f"  用户名: {admin[0]}")
    print(f"    UID: {admin[1]}")
    print(f"    级别: {admin[2]}")
    print(f"    注册日期: {admin[3]}")
    print()
conn.close()

# 用户数据库
print("[2] 用户数据库 (accounts/users.db)")
print("-" * 80)
conn = sqlite3.connect(os.path.join(BASE_DIR, 'accounts', 'users.db'))
cursor = conn.cursor()
cursor.execute("SELECT username, uid, register_date FROM users")
users = cursor.fetchall()
print(f"共有 {len(users)} 个用户:")
for user in users:
    print(f"  用户名: {user[0]}, UID: {user[1]}, 注册日期: {user[2]}")
conn.close()

# 作业管理系统权限
print("\n[3] 作业管理系统权限 (permissions/homework_permissions.db)")
print("-" * 80)
conn = sqlite3.connect(os.path.join(BASE_DIR, 'permissions', 'homework_permissions.db'))
cursor = conn.cursor()
cursor.execute("SELECT uid, permissions FROM homework_permissions")
perms = cursor.fetchall()
print(f"共有 {len(perms)} 条权限记录:")
for perm in perms:
    print(f"  UID: {perm[0]}")
    print(f"    权限: {perm[1]}")
    print()
conn.close()

# 场馆预约系统权限
print("[4] 场馆预约系统权限 (permissions/reservation_permissions.db)")
print("-" * 80)
conn = sqlite3.connect(os.path.join(BASE_DIR, 'permissions', 'reservation_permissions.db'))
cursor = conn.cursor()
cursor.execute("SELECT uid, permissions FROM reservation_permissions")
perms = cursor.fetchall()
print(f"共有 {len(perms)} 条权限记录:")
for perm in perms:
    print(f"  UID: {perm[0]}")
    print(f"    权限: {perm[1]}")
    print()
conn.close()

print("=" * 80)
print("[OK] 验证完成")
print("=" * 80)
