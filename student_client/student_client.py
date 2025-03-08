import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class StudentClient(QWidget):
    def __init__(self):
        super().__init__()
        self.server_ip = '121.43.233.248'
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('学生端')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # 登录界面
        self.username_input = QLineEdit(placeholderText="用户名")
        self.password_input = QLineEdit(placeholderText="密码", echoMode=QLineEdit.Password)
        self.login_btn = QPushButton("登录", clicked=self.login)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        # 统计信息显示
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        response = requests.post(
            f'http://{self.server_ip}:5000/login',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200 and response.json().get('role') == 'student':
            self.load_stats(username)
        else:
            QMessageBox.critical(self, "错误", "登录失败")

    def load_stats(self, username):
        response = requests.get(f'http://{self.server_ip}:5000/get_permissions?username={username}')
        if response.status_code == 200:
            permissions = response.json().get('permissions', '')
            class_name, subject = permissions.split(':')
            students = requests.get(
                f'http://{self.server_ip}:5000/students?class={class_name}&subject={subject}'
            ).json().get('students', [])
            student_data = next((s for s in students if s['name'] == username), None)
            if student_data:
                stats = {
                    '没带': 0,
                    '没来': 0,
                    '没写': 0
                }
                for key, value in student_data.items():
                    if key not in ['id', 'name']:
                        if value == '没带':
                            stats['没带'] += 1
                        elif value == '没来':
                            stats['没来'] += 1
                        elif value == '没写':
                            stats['没写'] += 1
                self.stats_label.setText(
                    f"{subject}学科\n"
                    f"没带: {stats['没带']}\n"
                    f"没来: {stats['没来']}\n"
                    f"没写: {stats['没写']}"
                )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentClient()
    window.show()
    sys.exit(app.exec_())
