import sys
import requests
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QFileDialog, QLineEdit, QLabel
)

class TeacherClient(QWidget):
    def __init__(self):
        super().__init__()
        self.server_ip = '121.43.233.248'
        self.current_class = ''
        self.current_subject = ''
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('课代表教师端')
        self.setGeometry(100, 100, 1000, 800)
        layout = QVBoxLayout()

        # 班级和学科选择
        self.class_combo = QComboBox()
        self.class_combo.currentTextChanged.connect(self.load_subjects)
        self.subject_combo = QComboBox()
        self.subject_combo.currentTextChanged.connect(self.load_assignments)
        layout.addWidget(QLabel("选择班级和学科"))
        layout.addWidget(self.class_combo)
        layout.addWidget(self.subject_combo)

        # 作业操作
        self.assignment_combo = QComboBox()
        self.create_btn = QPushButton("新建作业", clicked=self.create_assignment)
        self.export_btn = QPushButton("导出Excel", clicked=self.export_excel)
        layout.addWidget(QLabel("作业操作"))
        layout.addWidget(self.assignment_combo)
        layout.addWidget(self.create_btn)
        layout.addWidget(self.export_btn)

        # 学生状态表格
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # 初始化数据
        self.load_classes()
        self.setLayout(layout)

    def load_classes(self):
        response = requests.get(f'http://{self.server_ip}:5000/get_classes')
        if response.status_code == 200:
            self.class_combo.clear()
            self.class_combo.addItems(response.json().get('classes', []))

    def load_subjects(self, class_name):
        self.current_class = class_name
        response = requests.get(f'http://{self.server_ip}:5000/get_subjects?class={class_name}')
        if response.status_code == 200:
            self.subject_combo.clear()
            self.subject_combo.addItems(response.json().get('subjects', []))

    def load_assignments(self, subject):
        self.current_subject = subject
        response = requests.get(
            f'http://{self.server_ip}:5000/assignments?class={self.current_class}&subject={subject}'
        )
        if response.status_code == 200:
            self.assignment_combo.clear()
            self.assignment_combo.addItems(response.json().get('assignments', []))
            self.update_table()

    def create_assignment(self):
        assignment_name, ok = QInputDialog.getText(self, "新建作业", "输入作业名称:")
        if ok and assignment_name:
            response = requests.post(
                f'http://{self.server_ip}:5000/create_assignment',
                json={
                    'class': self.current_class,
                    'subject': self.current_subject,
                    'assignment_name': assignment_name
                }
            )
            if response.status_code == 200:
                self.load_assignments(self.current_subject)
            else:
                QMessageBox.critical(self, "错误", "创建失败")

    def update_table(self):
        # 从服务器加载学生和作业数据
        response = requests.get(
            f'http://{self.server_ip}:5000/assignments?class={self.current_class}&subject={self.current_subject}'
        )
        if response.status_code == 200:
            assignments = response.json().get('assignments', [])
            students = requests.get(
                f'http://{self.server_ip}:5000/students?class={self.current_class}&subject={self.current_subject}'
            ).json().get('students', [])

            self.table.setRowCount(len(students))
            self.table.setColumnCount(2 + len(assignments))
            headers = ['学号', '姓名'] + assignments
            self.table.setHorizontalHeaderLabels(headers)

            for row, student in enumerate(students):
                self.table.setItem(row, 0, QTableWidgetItem(str(student['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(student['name']))
                for col, assignment in enumerate(assignments):
                    status = student.get(assignment, '')
                    self.table.setItem(row, col + 2, QTableWidgetItem(status))

    def export_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "Excel Files (*.xlsx)")
        if file_path:
            response = requests.get(
                f'http://{self.server_ip}:5000/download?class={self.current_class}&subject={self.current_subject}'
            )
            with open(file_path, 'wb') as f:
                f.write(response.content)
            QMessageBox.information(self, "成功", "文件已导出")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeacherClient()
    window.show()
    sys.exit(app.exec_())
