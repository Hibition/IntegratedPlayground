from flask import Blueprint, render_template, redirect, url_for, session, request
from flask import flash


login_bp = Blueprint('login', __name__, template_folder='templates')

users = {
    'hibition',
    'mashiro',
}

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # 检查用户名和密码
        if username in users:
            session['username'] = username  # 存储登录状态
            return redirect(url_for('index'))
        else:
            flash('您并不是成员')  # 显示错误信息
    return render_template('login.html')

# 注销
@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login.login'))

def checkLogin():
    if 'username' not in session:
        return redirect(url_for('login.login'))  # 未登录时跳转到登录页面
