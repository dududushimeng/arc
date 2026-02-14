from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'psd', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        title = request.form.get('title', '')
        category = request.form.get('category', '')
        tags = request.form.get('tags', '')
        file = request.files.get('file')

        if not file or file.filename == '':
            return jsonify({'code': 400, 'msg': '请选择文件'})
        if not allowed_file(filename):
            return jsonify({'code': 400, 'msg': '只支持png/jpg/psd/zip'})

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        file.save(save_path)

        return jsonify({'code': 200, 'msg': '上传成功！', 'url': f'/static/uploads/{filename}'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': f'上传失败：{str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
