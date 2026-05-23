"""
账户和权限管理系统模块
提供统一的账户验证和权限管理接口
"""

import sqlite3
import os
from datetime import datetime

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_DIR = os.path.join(BASE_DIR, 'accounts')
PERMISSIONS_DIR = os.path.join(BASE_DIR, 'permissions')

# 数据库路径
USERS_DB = os.path.join(ACCOUNTS_DIR, 'users.db')
ADMIN_DB = os.path.join(ACCOUNTS_DIR, 'admin.db')


class AccountManager:
    """账户管理器"""

    @staticmethod
    def _get_db_connection(db_path):
        """获取数据库连接"""
        return sqlite3.connect(db_path)

    @staticmethod
    def verify_user(username, password):
        """
        验证普通用户登录

        参数:
            username: 用户名
            password: 密码

        返回:
            成功: dict {
                'success': True,
                'username': str,
                'uid': str,
                'message': str
            }
            失败: dict {
                'success': False,
                'error': str,
                'message': str
            }
        """
        try:
            conn = AccountManager._get_db_connection(USERS_DB)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT uid, password FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            conn.close()

            if not result:
                return {
                    'success': False,
                    'error': 'USER_NOT_FOUND',
                    'message': '用户名不存在'
                }

            uid, stored_password = result

            if password != stored_password:
                return {
                    'success': False,
                    'error': 'INVALID_PASSWORD',
                    'message': '密码错误'
                }

            return {
                'success': True,
                'username': username,
                'uid': uid,
                'message': '登录成功'
            }

        except Exception as e:
            return {
                'success': False,
                'error': 'DATABASE_ERROR',
                'message': f'数据库错误: {str(e)}'
            }

    @staticmethod
    def verify_admin(username, password):
        """
        验证管理员登录

        参数:
            username: 用户名
            password: 密码

        返回:
            成功: dict {
                'success': True,
                'username': str,
                'uid': str,
                'admin_level': str,
                'message': str
            }
            失败: dict {
                'success': False,
                'error': str,
                'message': str
            }
        """
        try:
            conn = AccountManager._get_db_connection(ADMIN_DB)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT uid, password, admin_level FROM admins WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            conn.close()

            if not result:
                return {
                    'success': False,
                    'error': 'ADMIN_NOT_FOUND',
                    'message': '管理员账号不存在'
                }

            uid, stored_password, admin_level = result

            if password != stored_password:
                return {
                    'success': False,
                    'error': 'INVALID_PASSWORD',
                    'message': '密码错误'
                }

            return {
                'success': True,
                'username': username,
                'uid': uid,
                'admin_level': admin_level,
                'message': '登录成功'
            }

        except Exception as e:
            return {
                'success': False,
                'error': 'DATABASE_ERROR',
                'message': f'数据库错误: {str(e)}'
            }

    @staticmethod
    def get_user_by_uid(uid):
        """
        根据UID获取用户信息

        参数:
            uid: 用户识别码

        返回:
            dict: 用户信息 或 None
        """
        try:
            # 先查普通用户
            conn = AccountManager._get_db_connection(USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username, uid, register_date FROM users WHERE uid = ?", (uid,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'username': result[0],
                    'uid': result[1],
                    'register_date': result[2],
                    'account_type': 'user'
                }

            # 再查管理员
            conn = AccountManager._get_db_connection(ADMIN_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT username, uid, admin_level, register_date FROM admins WHERE uid = ?", (uid,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'username': result[0],
                    'uid': result[1],
                    'admin_level': result[2],
                    'register_date': result[3],
                    'account_type': 'admin'
                }

            return None

        except Exception as e:
            print(f"获取用户信息失败: {e}")
            return None


class PermissionManager:
    """权限管理器"""

    # 权限文件映射
    PERMISSION_FILES = {
        'homework': os.path.join(PERMISSIONS_DIR, 'homework_permissions.db'),
        'reservation': os.path.join(PERMISSIONS_DIR, 'reservation_permissions.db'),
    }

    # 权限文件对应的表名
    PERMISSION_TABLES = {
        'homework': 'homework_permissions',
        'reservation': 'reservation_permissions',
    }

    @staticmethod
    def _get_db_connection(db_path):
        """获取数据库连接"""
        return sqlite3.connect(db_path)

    @staticmethod
    def get_permission(uid, app_name):
        """
        获取用户在某个应用中的权限

        参数:
            uid: 用户识别码
            app_name: 应用名称 (homework, reservation)

        返回:
            dict: {
                'success': bool,
                'permissions': str,  # 权限配置
                'is_new': bool       # 是否是新添加的权限记录
            }
        """
        if app_name not in PermissionManager.PERMISSION_FILES:
            return {
                'success': False,
                'error': 'INVALID_APP',
                'message': f'无效的应用名称: {app_name}'
            }

        try:
            db_path = PermissionManager.PERMISSION_FILES[app_name]
            table_name = PermissionManager.PERMISSION_TABLES[app_name]

            conn = PermissionManager._get_db_connection(db_path)
            cursor = conn.cursor()

            cursor.execute(
                f"SELECT permissions FROM {table_name} WHERE uid = ?",
                (uid,)
            )
            result = cursor.fetchone()

            if result:
                conn.close()
                return {
                    'success': True,
                    'permissions': result[0],
                    'is_new': False
                }

            # 如果权限不存在，添加新记录
            cursor.execute(
                f"INSERT INTO {table_name} (uid, permissions) VALUES (?, ?)",
                (uid, '.')  # 默认最低权限
            )
            conn.commit()
            conn.close()

            return {
                'success': True,
                'permissions': '.',
                'is_new': True
            }

        except Exception as e:
            return {
                'success': False,
                'error': 'DATABASE_ERROR',
                'message': f'数据库错误: {str(e)}'
            }

    @staticmethod
    def set_permission(uid, app_name, permissions):
        """
        设置用户在某个应用中的权限

        参数:
            uid: 用户识别码
            app_name: 应用名称
            permissions: 权限配置

        返回:
            dict: {
                'success': bool,
                'message': str
            }
        """
        if app_name not in PermissionManager.PERMISSION_FILES:
            return {
                'success': False,
                'error': 'INVALID_APP',
                'message': f'无效的应用名称: {app_name}'
            }

        try:
            db_path = PermissionManager.PERMISSION_FILES[app_name]
            table_name = PermissionManager.PERMISSION_TABLES[app_name]

            conn = PermissionManager._get_db_connection(db_path)
            cursor = conn.cursor()

            # 更新或插入权限
            cursor.execute(
                f"""
                INSERT INTO {table_name} (uid, permissions, updated_at)
                VALUES (?, ?, datetime('now'))
                ON CONFLICT(uid) DO UPDATE SET
                    permissions = excluded.permissions,
                    updated_at = datetime('now')
                """,
                (uid, permissions)
            )

            conn.commit()
            conn.close()

            return {
                'success': True,
                'message': '权限设置成功'
            }

        except Exception as e:
            return {
                'success': False,
                'error': 'DATABASE_ERROR',
                'message': f'数据库错误: {str(e)}'
            }

    @staticmethod
    def check_permission(uid, app_name, required_permission):
        """
        检查用户是否有特定权限

        参数:
            uid: 用户识别码
            app_name: 应用名称
            required_permission: 需要的权限

        返回:
            bool: 是否有权限
        """
        result = PermissionManager.get_permission(uid, app_name)

        if not result['success']:
            return False

        user_permissions = result['permissions']

        # 万能权限
        if user_permissions == '*':
            return True

        # 最低权限（无权限）
        if user_permissions == '.':
            return False

        # TODO: 根据应用需求实现更复杂的权限检查逻辑
        return required_permission in user_permissions.split(',')

    @staticmethod
    def get_all_permissions(uid):
        """
        获取用户在所有应用中的权限

        参数:
            uid: 用户识别码

        返回:
            dict: 所有应用的权限
        """
        all_permissions = {}

        for app_name in PermissionManager.PERMISSION_FILES.keys():
            result = PermissionManager.get_permission(uid, app_name)
            if result['success']:
                all_permissions[app_name] = result['permissions']
            else:
                all_permissions[app_name] = None

        return all_permissions


# 测试代码
if __name__ == '__main__':
    print("测试账户管理器")
    print("-" * 80)

    # 测试管理员登录
    print("\n1. 测试管理员登录")
    result = AccountManager.verify_admin('admin201030', 'Lyx20081107abc')
    print(f"admin201030 登录结果: {result}")

    # 测试普通用户登录
    print("\n2. 测试普通用户登录")
    result = AccountManager.verify_user('刘懿旭', 'Lyx20081107abc')
    print(f"刘懿旭 登录结果: {result}")

    # 测试权限获取
    print("\n3. 测试权限获取")
    uid = 'LJRK-SFQD-0000000000'  # 超级管理员
    result = PermissionManager.get_permission(uid, 'homework')
    print(f"超级管理员在作业系统中的权限: {result}")

    # 测试新用户权限
    print("\n4. 测试新用户权限（自动添加）")
    uid = 'LJRK-SFQD-2503270003'  # 汤文博
    result = PermissionManager.get_permission(uid, 'reservation')
    print(f"汤文博在预约系统中的权限: {result}")

    # 测试权限检查
    print("\n5. 测试权限检查")
    uid = 'LJRK-SFQD-0000000000'
    has_perm = PermissionManager.check_permission(uid, 'homework', 'view')
    print(f"超级管理员是否有查看作业权限: {has_perm}")

    print("\n" + "-" * 80)
    print("测试完成")
