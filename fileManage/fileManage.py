from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory
from flask import flash
import os
from app import app
from login.login import checkLogin

fileManage_bp = Blueprint('fileManage', __name__, template_folder='templates')

# 设置上传文件的目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@fileManage_bp.route('/')
def fileManagePage():
    checkLogin()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('fileManagePage.html', files=files)

# 处理文件上传（需要登录）
@fileManage_bp.route('/upload', methods=['POST'])
def upload_file():
    checkLogin()
    if 'file' not in request.files:
        return redirect(url_for('error_page', error_text="No file part"))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('error_page', error_text="No selected file"))
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('fileManage.fileManagePage'))

# 下载文件（需要登录）
@fileManage_bp.route('/download/<filename>')
def download_file(filename):
    checkLogin()
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 删除文件（需要登录）
@fileManage_bp.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    checkLogin()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        return render_template('error.html', error="File does not exist!")
    return redirect(url_for('fileManage.fileManagePage'))
