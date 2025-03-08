import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QListWidget, QStackedWidget, QInputDialog
)

class AdminClient(QWidget):
    def __init__(self):
        super().__init__()
        self.server_ip = '121.43.233.248'  # 服务器IP
        self.setWindowTitle('管理端')
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        # 登录界面
        self.login_ui()
        # 主功能界面
        self.main_ui()

        self.setLayout(self.layout)

    def login_ui(self):
        self.login_layout = QVBoxLayout()
        self.username_input = QLineEdit(placeholderText="用户名")
        self.password_input = QLineEdit(placeholderText="密码", echoMode=QLineEdit.Password)
        self.login_btn = QPushButton("登录", clicked=self.login)
        self.login_layout.addWidget(QLabel("管理员登录"))
        self.login_layout.addWidget(self.username_input)
        self.login_layout.addWidget(self.password_input)
        self.login_layout.addWidget(self.login_btn)
        self.layout.addLayout(self.login_layout)

    def main_ui(self):
        self.main_stack = QStackedWidget()
        # 创建账户界面
        self.create_account_ui()
        # 修改权限界面
        self.modify_permission_ui()
        # 备份数据库界面
        self.backup_ui()
        self.layout.addWidget(self.main_stack)

    def create_account_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.new_username = QLineEdit(placeholderText="新用户名")
        self.new_password = QLineEdit(placeholderText="新密码", echoMode=QLineEdit.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["teacher", "student"])
        self.create_btn = QPushButton("创建账户", clicked=self.create_account)
        layout.addWidget(QLabel("创建新账户"))
        layout.addWidget(self.new_username)
        layout.addWidget(self.new_password)
        layout.addWidget(self.role_combo)
        layout.addWidget(self.create_btn)
        widget.setLayout(layout)
        self.main_stack.addWidget(widget)

    def modify_permission_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.search_input = QLineEdit(placeholderText="输入用户名")
        self.search_btn = QPushButton("搜索", clicked=self.search_user)
        self.permission_list = QListWidget()
        self.set_teacher_btn = QPushButton("设置教师权限", clicked=lambda: self.set_permission('teacher'))
        self.set_student_btn = QPushButton("设置学生权限", clicked=lambda: self.set_permission('student'))
        self.reset_btn = QPushButton("重置权限", clicked=self.reset_permission)
        layout.addWidget(QLabel("修改权限"))
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.permission_list)
        layout.addWidget(self.set_teacher_btn)
        layout.addWidget(self.set_student_btn)
        layout.addWidget(self.reset_btn)
        widget.setLayout(layout)
        self.main_stack.addWidget(widget)

    def backup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.backup_btn = QPushButton("备份数据库", clicked=self.backup_database)
        layout.addWidget(QLabel("数据库备份"))
        layout.addWidget(self.backup_btn)
        widget.setLayout(layout)
        self.main_stack.addWidget(widget)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        response = requests.post(
            f'http://{self.server_ip}:5000/login',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200 and response.json().get('role') == 'admin':
            self.main_stack.setCurrentIndex(1)
        else:
            QMessageBox.critical(self, "错误", "登录失败或无权限")

    def create_account(self):
        username = self.new_username.text()
        password = self.new_password.text()
        role = self.role_combo.currentText()
        response = requests.post(
            f'http://{self.server_ip}:5000/register',
            json={'username': username, 'password': password, 'role': role}
        )
        if response.status_code == 201:
            QMessageBox.information(self, "成功", "账户创建成功")
        else:
            QMessageBox.critical(self, "错误", response.json().get('message'))

    def search_user(self):
        username = self.search_input.text()
        response = requests.get(
            f'http://{self.server_ip}:5000/get_permissions?username={username}'
        )
        if response.status_code == 200:
            self.permission_list.clear()
            self.permission_list.addItem(f"当前权限: {response.json().get('permissions')}")
        else:
            QMessageBox.critical(self, "错误", "用户不存在")

    def set_permission(self, role):
        class_name, ok1 = QInputDialog.getItem(self, "选择班级", "班级:", self.get_classes())
        subject, ok2 = QInputDialog.getItem(self, "选择学科", "学科:", self.get_subjects(class_name))
        if ok1 and ok2:
            permissions = f"{class_name}:{subject}"
            username = self.search_input.text()
            response = requests.post(
                f'http://{self.server_ip}:5000/set_permissions',
                json={'username': username, 'permissions': permissions}
            )
            if response.status_code == 200:
                QMessageBox.information(self, "成功", "权限设置成功")
            else:
                QMessageBox.critical(self, "错误", "设置失败")

    def reset_permission(self):
        username = self.search_input.text()
        response = requests.post(
            f'http://{self.server_ip}:5000/set_permissions',
            json={'username': username, 'permissions': ''}
        )
        if response.status_code == 200:
            QMessageBox.information(self, "成功", "权限已重置")
        else:
            QMessageBox.critical(self, "错误", "重置失败")

    def backup_database(self):
        response = requests.get(f'http://{self.server_ip}:5000/backup')
        if response.status_code == 200:
            QMessageBox.information(self, "成功", "数据库备份成功")
        else:
            QMessageBox.critical(self, "错误", "备份失败")

    def get_classes(self):
        response = requests.get(f'http://{self.server_ip}:5000/get_classes')
        return response.json().get('classes', []) if response.status_code == 200 else []

    def get_subjects(self, class_name):
        response = requests.get(f'http://{self.server_ip}:5000/get_subjects?class={class_name}')
        return response.json().get('subjects', []) if response.status_code == 200 else []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminClient()
    window.show()
    sys.exit(app.exec_())
