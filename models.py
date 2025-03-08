from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """用户账号和权限的数据库模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名（唯一）
    password = db.Column(db.String(120), nullable=False)              # 密码
    role = db.Column(db.String(20), nullable=False)                   # 角色：admin/teacher/student
    permissions = db.Column(db.String(200))                           # 权限：班级:学科（如 "高一（6）班:物理"）

    def __repr__(self):
        return f'<User {self.username} (Role: {self.role})>'
