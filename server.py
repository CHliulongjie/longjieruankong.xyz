import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# LeanCloud 配置
LEANCLOUD_APP_ID = os.getenv('SiessoHsczaD2D07CHw2D4cN-gzGzoHsz')
LEANCLOUD_APP_KEY = os.getenv('3gJvfdkUFjCqlcfKuaIhuhjp')
LEANCLOUD_API_URL = f"https://siessohs.lc-cn-n1-shared.com"

# 设置请求头
headers = {
    "X-LC-Id": LEANCLOUD_APP_ID,
    "X-LC-Key": LEANCLOUD_APP_KEY,
    "Content-Type": "application/json"
}

# 更新作业状态
@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    class_id = data.get('class_id')
    subject_id = data.get('subject_id')
    student_id = data.get('student_id')
    status = data.get('status')

    # 保存到 LeanCloud
    payload = {
        "class_id": class_id,
        "subject_id": subject_id,
        "student_id": student_id,
        "status": status
    }
    response = requests.post(
        f"{LEANCLOUD_API_URL}/classes/Assignment",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        return jsonify({"message": "状态更新成功"})
    else:
        return jsonify({"message": "状态更新失败"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
