from flask import Blueprint, render_template, request, redirect, url_for

from ... import admin

registration = Blueprint('/registration', __name__, url_prefix='/registration')


@registration.route('/')
def registration_user_page():
    return render_template('registration.html')


@registration.route('/', methods=['POST'])
def registration_user():

    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        if admin.login == '' and admin.password == '':
            admin.login = login
            admin.password = password
        else:
            return f'Пользователь уже существует {admin.login}'
    else:
        return f'Не найденны регистрационные данные'

    return redirect('/auth')
