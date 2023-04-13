import asyncio

from flask import Blueprint, render_template, request
from flask_login import login_required
from telethon import TelegramClient

settings = Blueprint('/settings', __name__, url_prefix='/settings')


__client = None
__data = {}

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)


@settings.route('/')
@login_required
def settings_profile():
    return render_template('settings.html')


@settings.route('/app-registration/', methods=['POST'])
@login_required
def app_registration():

    api_id = request.form.get('api_id')
    api_hash = request.form.get('api_hash')

    if api_id and api_hash:
        try:
            __data['api_id'] = api_id
            __data['api_hash'] = api_hash
        except Exception as ex:
            print(ex)

    print(__data, not api_id, not api_hash)

    return render_template('settings.html')


async def __get_code(phone):
    global __client

    __client = TelegramClient('new_session', api_id=int(__data['api_id']), api_hash=__data['api_hash'])
    await __client.connect()
    await __client.send_code_request(phone)


async def __start_telethon(phone, code):
    await __client.start(phone=phone, code=code)


async def __get_dialogs():

    dialogs = __client.iter_dialogs()

    __data['dialogs'] = []

    async for dialog in dialogs:
        __data['dialogs'].append(dialog.title)


@settings.route('/login-telegram/', methods=['POST'])
@login_required
def login_telegram():

    phone = request.form.get('phone')

    if phone:
        try:
            loop.run_until_complete(__get_code(phone))

            __data['phone'] = phone
        except Exception as ex:
            print(ex)

    print('Not Here', __client, not __client)

    return render_template('settings.html')


@settings.route('/confirm-code/', methods=['POST'])
@login_required
def confirm_code():

    code = request.form.get('code')

    if not code and __client and 'phone' in __data.keys():
        try:
            loop.run_until_complete(__start_telethon(phone=__data['phone'], code=code))

        except Exception as ex:
            print(ex)

    return render_template('settings.html')


@settings.route('/get-chats/', methods=['POST'])
@login_required
def get_chats():
    loop.run_until_complete(__get_dialogs())
