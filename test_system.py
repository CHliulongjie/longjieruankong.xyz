"""
作业管理系统模拟测试
"""
import requests
import json
import time

BASE_URL = 'http://localhost:8000'

def print_step(step, message):
    print(f"\n{'='*60}")
    print(f"步骤 {step}: {message}")
    print('='*60)

def test_admin_flow():
    """测试管理员流程"""
    print_step(1, "管理端测试")
    
    # 1. 注册管理员账户
    print("\n1.1 注册管理员账户")
    register_data = {
        'username': 'test_admin',
        'password': 'admin123',
        'account_type': 'admin'
    }
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print(f"注册响应: {response.json()}")
    
    # 2. 登录
    print("\n1.2 管理员登录")
    login_data = {
        'username': 'test_admin',
        'password': 'admin123',
        'app_name': 'homework'
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    result = response.json()
    print(f"登录响应: {result}")
    
    if result.get('success'):
        uid = result.get('uid')
        print(f"\n✓ 管理员登录成功，UID: {uid}")
        
        # 3. 获取用户列表
        print("\n1.3 获取用户列表")
        response = requests.get(f'{BASE_URL}/users')
        print(f"用户列表: {response.json()}")
        
        # 4. 设置权限
        print("\n1.4 设置权限")
        perm_data = {
            'uid': uid,
            'permissions': '*',
            'app_name': 'homework'
        }
        response = requests.post(f'{BASE_URL}/set_permissions', json=perm_data)
        print(f"权限设置响应: {response.json()}")
        
        # 5. 修改密码
        print("\n1.5 修改密码")
        pwd_data = {
            'uid': uid,
            'new_password': 'newpass123'
        }
        response = requests.post(f'{BASE_URL}/change_password', json=pwd_data)
        print(f"密码修改响应: {response.json()}")
        
        return True
    else:
        print(f"✗ 管理员登录失败: {result.get('message')}")
        return False

def test_teacher_flow():
    """测试教师流程"""
    print_step(2, "教师端测试")
    
    # 1. 注册教师账户
    print("\n2.1 注册教师账户")
    register_data = {
        'username': 'test_teacher',
        'password': 'teacher123',
        'account_type': 'user'
    }
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print(f"注册响应: {response.json()}")
    
    # 2. 登录
    print("\n2.2 教师登录")
    login_data = {
        'username': 'test_teacher',
        'password': 'teacher123',
        'app_name': 'homework'
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    result = response.json()
    print(f"登录响应: {result}")
    
    if result.get('success'):
        print(f"\n✓ 教师登录成功")
        
        # 3. 获取班级列表
        print("\n2.3 获取班级列表")
        response = requests.get(f'{BASE_URL}/classes')
        print(f"班级列表: {response.json()}")
        
        # 4. 获取科目列表
        print("\n2.4 获取科目列表")
        response = requests.get(f'{BASE_URL}/subjects')
        print(f"科目列表: {response.json()}")
        
        # 5. 创建作业
        print("\n2.5 创建作业")
        assignment_data = {
            'class_name': '高一(1)班',
            'subject': '数学',
            'assignments': [
                {
                    '作业名称': '第一次作业',
                    '布置日期': '2026-05-23',
                    '截止日期': '2026-05-30',
                    '没带': 0,
                    '没来': 0,
                    '没做': 0,
                    '补交': 0,
                    '备注': '测试作业'
                }
            ]
        }
        response = requests.post(f'{BASE_URL}/create_assignment', json=assignment_data)
        print(f"创建作业响应: {response.json()}")
        
        # 6. 获取作业列表
        print("\n2.6 获取作业列表")
        response = requests.get(f'{BASE_URL}/assignments?class=高一(1)班&subject=数学')
        print(f"作业列表: {response.json()}")
        
        # 7. 更新作业（标记学生完成情况）
        print("\n2.7 更新作业完成情况")
        update_data = {
            'class_name': '高一(1)班',
            'subject': '数学',
            'assignments': [
                {
                    '作业名称': '第一次作业',
                    '布置日期': '2026-05-23',
                    '截止日期': '2026-05-30',
                    '学生A': '已完成',
                    '学生B': '没带',
                    '学生C': '没做',
                    '备注': '已更新'
                }
            ]
        }
        response = requests.post(f'{BASE_URL}/update', json=update_data)
        print(f"更新作业响应: {response.json()}")
        
        return True
    else:
        print(f"✗ 教师登录失败: {result.get('message')}")
        return False

def test_student_flow():
    """测试学生流程"""
    print_step(3, "学生端测试")
    
    # 1. 注册学生账户
    print("\n3.1 注册学生账户")
    register_data = {
        'username': 'test_student',
        'password': 'student123',
        'account_type': 'user'
    }
    response = requests.post(f'{BASE_URL}/register', json=register_data)
    print(f"注册响应: {response.json()}")
    
    # 2. 登录
    print("\n3.2 学生登录")
    login_data = {
        'username': 'test_student',
        'password': 'student123',
        'app_name': 'homework'
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    result = response.json()
    print(f"登录响应: {result}")
    
    if result.get('success'):
        print(f"\n✓ 学生登录成功")
        
        # 3. 获取班级列表
        print("\n3.3 获取班级列表")
        response = requests.get(f'{BASE_URL}/classes')
        print(f"班级列表: {response.json()}")
        
        # 4. 获取科目列表
        print("\n3.4 获取科目列表")
        response = requests.get(f'{BASE_URL}/subjects')
        print(f"科目列表: {response.json()}")
        
        # 5. 获取作业列表
        print("\n3.5 查询作业")
        response = requests.get(f'{BASE_URL}/assignments?class=高一(1)班&subject=数学')
        print(f"作业列表: {response.json()}")
        
        return True
    else:
        print(f"✗ 学生登录失败: {result.get('message')}")
        return False

def main():
    print("\n" + "="*60)
    print("作业管理系统完整测试")
    print("="*60)
    
    try:
        # 测试管理员流程
        if test_admin_flow():
            print("\n✓ 管理员流程测试通过")
        else:
            print("\n✗ 管理员流程测试失败")
        
        time.sleep(1)
        
        # 测试教师流程
        if test_teacher_flow():
            print("\n✓ 教师流程测试通过")
        else:
            print("\n✗ 教师流程测试失败")
        
        time.sleep(1)
        
        # 测试学生流程
        if test_student_flow():
            print("\n✓ 学生流程测试通过")
        else:
            print("\n✗ 学生流程测试失败")
        
        print("\n" + "="*60)
        print("测试完成")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        print("请确保服务器正在运行: python app.py")

if __name__ == '__main__':
    main()