import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class Client(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('作业管理系统客户端')
        self.setGeometry(100, 100, 400, 200)

        # 主布局
        self.layout = QVBoxLayout()

        # 输入框
        self.class_name_input = QLineEdit(self)
        self.class_name_input.setPlaceholderText("请输入班级名称")
        self.layout.addWidget(self.class_name_input)

        self.subject_name_input = QLineEdit(self)
        self.subject_name_input.setPlaceholderText("请输入学科名称")
        self.layout.addWidget(self.subject_name_input)

        # 按钮
        self.get_list_button = QPushButton('获取班级名单', self)
        self.get_list_button.clicked.connect(self.get_class_list)
        self.layout.addWidget(self.get_list_button)

        # 设置布局
        self.setLayout(self.layout)

    def get_class_list(self):
        class_name = self.class_name_input.text()
        subject_name = self.subject_name_input.text()

        if class_name and subject_name:
            response = requests.get(
                "https://your-service.onrender.com/get_class_list",
                params={"class_name": class_name, "subject_name": subject_name}
            )
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, "班级名单", str(data))
            else:
                QMessageBox.critical(self, "错误", "获取班级名单失败！")
        else:
            QMessageBox.warning(self, "警告", "请输入班级名称和学科名称！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
