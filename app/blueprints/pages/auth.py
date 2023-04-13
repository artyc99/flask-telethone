from flask import Blueprint, render_template, request, redirect
from flask_login import login_user

from ... import admin

auth = Blueprint('/auth', __name__, url_prefix='/auth')


@auth.route('/')
def auth_user_page():
    return render_template('auth.html')


@auth.route('/', methods=['POST'])
def auth_user():

    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        if admin.login == login and admin.password == password:
            login_user(admin)
            return redirect('/settings/')
        else:
            return f'Неверные данные {admin.login}'
    else:
        return f'Не найденны регистрационные данные'
