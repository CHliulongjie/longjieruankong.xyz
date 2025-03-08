from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from utils import read_student_list, update_student_status, read_assignment_list, create_assignment
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/users.db'  # 数据库文件保存到 data 目录
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    permissions = db.Column(db.String(200))  # 格式：班级:学科（如 "高一（6）班:物理"）

# 初始化管理员账号（仅首次运行生效）
def init_admin():
    if not User.query.filter_by(username='admin201030').first():
        admin = User(
            username='admin201030',
            password='Lyx20081107abc',
            role='admin',
            permissions='*:*'  # 所有权限
        )
        db.session.add(admin)
        db.session.commit()

# 新增接口：备份数据库
@app.route('/backup', methods=['GET'])
def backup():
    try:
        os.system('cp data/users.db data/users_backup.db')  # 备份数据库
        return jsonify({'message': '备份成功'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 其他接口保持不变

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('data'):
            os.makedirs('data')  # 创建 data 目录
        db.create_all()
        init_admin()  # 初始化管理员
    app.run(host='0.0.0.0', port=5000)
