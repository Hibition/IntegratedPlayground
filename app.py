from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_socketio import SocketIO
from flask import Blueprint
import os


app = Flask(__name__)
app.secret_key = '2024/09/28TheDayThisWebBirth'  # 用于加密会话数据

# 聊天应用：
socketio = SocketIO(app)


# 注册 blueprint
from chat.chat import chat_bp
from login.login import login_bp, checkLogin
from fileManage.fileManage import fileManage_bp

app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(fileManage_bp, url_prefix='/fileManage')


@app.route('/')
def index():
    checkLogin()
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', username=session['username'])


@app.route('/error')
def error_page():
    error_text = request.args.get('error_text', 'Unknown error occurred.')
    return render_template('error.html', error=error_text)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
