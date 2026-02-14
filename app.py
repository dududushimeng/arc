from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# 配置上传
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'psd', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 30MB

# 允许的文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 首页路由（动态展示作品）
@app.route('/')
def index():
    upload_dir = app.config['UPLOAD_FOLDER']
    files = []
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.psd', '.zip')):
                file_path = os.path.join(upload_dir, filename)
                file_stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'url': f'/static/uploads/{filename}',
                    'time': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'size': file_stat.st_size
                })
    return render_template('index.html', files=files)

# 番剧页面路由
@app.route('/fanju')
def fanju():
    return render_template('fanju.html')

# 上传页面路由
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# 兔子页面路由（如果需要）
@app.route('/tuzi')
def tuzi():
    return render_template('tuzi.html')

# 上传接口
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # 接收参数
        title = request.form.get('title', '')
        category = request.form.get('category', '')
        tags = request.form.get('tags', '')
        file = request.files.get('file')

        if not file or file.filename == '':
            return jsonify({'code': 400, 'msg': '请选择文件'})

        if not allowed_file(file.filename):
            return jsonify({'code': 400, 'msg': '只支持 png/jpg/psd/zip 等格式'})

        # 确保上传目录存在
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # 重命名防止重名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # 保存文件
        file.save(save_path)

        return jsonify({
            'code': 200,
            'msg': '上传成功！',
            'url': f'/static/uploads/{filename}'
        })

    except Exception as e:
        return jsonify({'code': 500, 'msg': f'上传失败：{str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
