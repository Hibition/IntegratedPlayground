from flask import Blueprint, render_template, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import emit
from datetime import datetime, timedelta
import time

from app import socketio
from login.login import checkLogin

chat_bp = Blueprint('chat', __name__, template_folder='templates')

messages = []
scheduler = BackgroundScheduler()
scheduler.start()

def delete_message(index):
    """删除消息"""
    if index < len(messages):
        print(f"Deleting message: {messages[index]}")
        del messages[index]

@chat_bp.route('/')
def chatRoom():
    checkLogin()
    """渲染聊天页面"""
    return render_template('chat.html')

@socketio.on('send_message')
def handle_message(data):
    checkLogin()
    username = session.get('username', 'Anonymous')  # 默认使用 'Anonymous'

    message = {
        'user': username,
        'msg': data['msg'],
        'timestamp': time.time()
    }
    messages.append(message)

    # 广播消息给所有用户
    emit('receive_message', message, broadcast=True)

    # 安排10分钟后删除该消息
    index = len(messages) - 1
    run_date = datetime.now() + timedelta(minutes=10)  # 计算10分钟后的时间
    scheduler.add_job(func=delete_message, trigger="date", run_date=run_date, args=[index])


@socketio.on('connect')
def handle_connect():
    checkLogin()
    """用户连接时，发送历史消息"""
    emit('load_messages', messages)