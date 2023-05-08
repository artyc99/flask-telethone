import asyncio
import json
from flask import Blueprint, render_template, request, send_file, Response
from flask_login import login_required
from telethon.sync import TelegramClient
from telethon import events

from main import loop

settings = Blueprint('/settings', __name__, url_prefix='/settings')

__dialog_types = ['user_id', 'channel_id', 'chat_id']
__words = ['райс', 'асценки', 'асчет']

__client = None
__data = {
    'events': [],
    'status': 'setup'
}


@settings.route('/')
@login_required
def settings_profile():
    return render_template('settings.html', data=__data)


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

    return render_template('settings.html', data=__data)


async def __get_code(phone):
    global __client

    __client = TelegramClient('new_session', api_id=int(__data['api_id']), api_hash=__data['api_hash'], loop=loop)

    await __client.connect()
    try:
        test = await __client.get_me()
        if test:
            print('Me: ', test.to_dict())
            __data['status'] = 'connected'
            print('Telethone started')
        else:
            __data['status'] = 'waiting code'
            await __client.send_code_request(phone)
            print('Send Code')
    except Exception as ex:
        print(ex)


def __start_telethon(phone, code):
    if code:
        __client.start(phone=phone, code_callback=lambda: code)
        test = __client.get_me()
        if test:
            print(test.to_dict())
            __data['status'] = 'connected'
        else:
            print('Unlogin with code')
    else:
        __client.start(phone=phone)
        test = __client.get_me()
        if test:
            print(test.to_dict())
            __data['status'] = 'connected'
        else:
            print('Unlogin without code')


async def __get_dialogs():
    try:
        dialogs = __client.iter_dialogs()
    except Exception as ex:
        print(ex)
        return

    __data['dialogs'] = {}

    async for dialog in dialogs:
        dialog_json = dialog.message.peer_id.to_dict()

        for key in __dialog_types:
            if key in dialog_json.keys():
                __data['dialogs'][dialog_json[key]] = dialog.title


@settings.route('/login-telegram/', methods=['POST'])
@login_required
async def login_telegram():
    phone = request.form.get('phone')

    if phone:
        try:
            await __get_code(phone)

            __data['phone'] = phone
        except Exception as ex:
            print(ex)

    return render_template('settings.html', data=__data)


@settings.route('/confirm-code/', methods=['POST'])
@login_required
def confirm_code():
    code = request.form.get('code')

    if code and __client and 'phone' in __data.keys():
        try:
            __start_telethon(phone=__data['phone'], code=code)
            print('Start telethone')
        except Exception as ex:
            print(ex)

    return render_template('settings.html', data=__data)


@settings.route('/get-chats/', methods=['POST'])
@login_required
async def get_chats():
    await __get_dialogs()

    return render_template('settings.html', data=__data)


async def message_handler(event_):
    tasks = asyncio.all_tasks()
    # report all tasks
    for task in tasks:
        print(f'> {task.get_name()}, {task.get_coro()}')
    for word in __words:
        if word in event_.message.message:
            print(event_.message.to_dict())
            dialog_json = event_.message.peer_id.to_dict()

            for key in __dialog_types:
                if key in dialog_json.keys():
                    id_ = dialog_json[key]
                    for stored_event in __data['events']:
                        if stored_event['from_id'] == id_:
                            await __client.forward_messages(stored_event['to_id'], event_.message)

            __data['last_message'] = event_.message.to_dict()


@settings.route('/add-listener/', methods=['POST'])
@login_required
def add_listener():
    listen = int(request.form.get('listen'))
    recive = int(request.form.get('recive'))

    if listen != recive and listen and recive:
        event = events.NewMessage(chats=[listen])

        __client.add_event_handler(message_handler, event)

        __data['events'].append({
            'from_title': __data['dialogs'][listen],
            'to_title': __data['dialogs'][recive],
            'from_id': listen,
            'to_id': recive,
            'event': event
        })

    return render_template('settings.html', data=__data)


@settings.route('/delete-listener/', methods=['POST'])
@login_required
def delete_listener():
    index = int(request.form.get('index'))

    __client.remove_event_handler(message_handler, __data['events'][index]['event'])

    del __data['events'][index]

    return render_template('settings.html', data=__data)


@settings.route('/dump-listeners/', methods=['POST'])
@login_required
def dump_listeners():
    listeners_dump = {'listeners_dump': [{
        'from_title': event['from_title'],
        'to_title': event['to_title'],
        'from_id': event['from_id'],
        'to_id': event['to_id']
    } for event in __data['events']]}

    return Response(
        json.dumps(listeners_dump),
        mimetype="text/json",
        headers={"Content-disposition":
                 "attachment; filename=listeners_dump.json"})


@settings.route('/load-listeners/', methods=['POST'])
@login_required
def load_listeners():
    events_dump = json.loads(request.form.get('events-dump'))['listeners_dump']

    for index, event in enumerate(__data['events']):
        __client.remove_event_handler(message_handler, event)

        del __data['events'][index]

    for event_dump in events_dump:
        event = events.NewMessage(chats=[event_dump['to_id']])

        __client.add_event_handler(message_handler, event)

        __data['events'].append({
            'from_title': event_dump['from_title'],
            'to_title': event_dump['to_title'],
            'from_id': event_dump['from_id'],
            'to_id': event_dump['to_id'],
            'event': event
        })

    return render_template('settings.html', data=__data)
