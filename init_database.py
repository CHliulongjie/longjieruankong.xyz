#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙解软控 - XYZ服务器 数据库初始化脚本
首次部署时运行此脚本创建数据库
"""

import sqlite3
import os

# 路径配置
base_dir = os.path.dirname(os.path.abspath(__file__))
accounts_dir = os.path.join(base_dir, 'accounts')
permissions_dir = os.path.join(base_dir, 'permissions')
data_dir = os.path.join(base_dir, 'data')

# 确保目录存在
os.makedirs(accounts_dir, exist_ok=True)
os.makedirs(permissions_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

def init_admin_database():
    """初始化管理员数据库"""
    db_path = os.path.join(accounts_dir, 'admin.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建管理员表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            uid TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            admin_level TEXT DEFAULT 'admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 检查是否已有数据
    cursor.execute('SELECT COUNT(*) FROM admins')
    if cursor.fetchone()[0] == 0:
        # 插入超级管理员
        cursor.execute('''
            INSERT INTO admins (uid, username, password, admin_level)
            VALUES (?, ?, ?, ?)
        ''', ('LJRK-SFQD-0000000000', 'admin201030', 'Lyx20081107abc', 'super_admin'))

        # 插入测试管理员
        cursor.execute('''
            INSERT INTO admins (uid, username, password, admin_level)
            VALUES (?, ?, ?, ?)
        ''', ('LJRK-SFQD-2503270001', '刘懿旭', 'Lyx20081107abc', 'admin'))

        print("✓ 管理员数据库初始化完成")
    else:
        print("ℹ 管理员数据库已存在，跳过初始化")

    conn.commit()
    conn.close()

def init_user_database():
    """初始化普通用户数据库"""
    db_path = os.path.join(accounts_dir, 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 检查是否已有数据
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # 插入测试用户
        test_users = [
            ('LJRK-SFQD-2503270002', 'heidi', '20250327'),
            ('LJRK-SFQD-2503270003', '汤文博', 'Rhodes_Island'),
            ('LJRK-SFQD-2503270004', '吴菲涵', 'wfh123456'),
            ('LJRK-SFQD-2503270005', '测试员1', 'text1'),
            ('LJRK-SFQD-2503270006', '胡雨辰', '112358'),
            ('LJRK-SFQD-2503270007', 'jimmy', '277412'),
            ('LJRK-SFQD-2503270008', '杨子轩', '123456'),
        ]

        for uid, username, password in test_users:
            cursor.execute('''
                INSERT INTO users (uid, username, password)
                VALUES (?, ?, ?)
            ''', (uid, username, password))

        print("✓ 普通用户数据库初始化完成")
    else:
        print("ℹ 普通用户数据库已存在，跳过初始化")

    conn.commit()
    conn.close()

def init_permissions_database():
    """初始化作业管理系统权限数据库"""
    app_name = 'homework'
    db_path = os.path.join(permissions_dir, f'{app_name}_permissions.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建权限表
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {app_name}_permissions (
            uid TEXT PRIMARY KEY,
            permissions TEXT DEFAULT '.',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 检查是否已有数据
    cursor.execute(f'SELECT COUNT(*) FROM {app_name}_permissions')
    if cursor.fetchone()[0] == 0:
        # 插入超级管理员权限
        cursor.execute(f'''
            INSERT INTO {app_name}_permissions (uid, permissions)
            VALUES (?, ?)
        ''', ('LJRK-SFQD-0000000000', '*'))

        # 插入管理员权限
        cursor.execute(f'''
            INSERT INTO {app_name}_permissions (uid, permissions)
            VALUES (?, ?)
        ''', ('LJRK-SFQD-2503270001', '*'))

        print("✓ 作业管理系统权限数据库初始化完成")
    else:
        print("ℹ 作业管理系统权限数据库已存在，跳过初始化")

    conn.commit()
    conn.close()

def main():
    print("=" * 50)
    print("龙解软控 - XYZ服务器 数据库初始化")
    print("=" * 50)
    print()

    try:
        init_admin_database()
        init_user_database()
        init_permissions_database()

        print()
        print("=" * 50)
        print("✓ 所有数据库初始化完成！")
        print("=" * 50)
        print()
        print("默认账户信息：")
        print("  超级管理员：admin201030 / Lyx20081107abc")
        print("  管理员：     刘懿旭 / Lyx20081107abc")
        print("  测试用户：   heidi / 20250327")
        print()

    except Exception as e:
        print(f"✗ 初始化失败: {e}")
        raise

if __name__ == '__main__':
    main()
