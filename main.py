import asyncio
import time

from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser

from app import FlaskApplication

from secrets import api_id, api_hash, phone


def test(client) -> None:
    client.connect()

    time.sleep(2)

    sent = client.send_code_request(phone)
    print(sent)

    code = lambda: input("Code:")

    # client.start(phone=phone, code_callback=lambda: input('Please enter your phone (or bot token): '))
    #
    # print(client.get_me())
    #
    # for dialog in client.iter_dialogs():
    #     print(dialog.title)


def main():
    # app = FlaskApplication()
    #
    # app.run()

    client = TelegramClient('new_session', api_id=api_id, api_hash=api_hash)

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test(client))
    client.start(phone=phone)

    dialogs = client.iter_dialogs()

    for dialog in dialogs:
        print(dialog)

    # test(client)

    @client.on(events.NewMessage(chats=[807536654]))
    async def message_handler(event):
        print(event.message.to_dict())

    client.run_until_disconnected()

def flask():
    from app import FlaskApplication

    app = FlaskApplication(application_secret='test')
    app.run()


if __name__ == '__main__':
    main()
