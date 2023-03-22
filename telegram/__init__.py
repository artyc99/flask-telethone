from typing import List, Tuple

from telethon import events
from telethon.sync import TelegramClient


class TelephoneScrapper:

    def __init__(self, api_id: int, api_hash: str, phone_number: str):
        self.__phone_number = phone_number

        self.__client = TelegramClient('bot_session', api_id, api_hash)
        self.__client.connect()

        self.__code: int = 0

    def send_code(self) -> None:
        self.__client.send_code_request(self.__phone_number)

    def __get_code(self) -> int:
        return self.__code

    def __get_phone(self) -> str:
        return self.__phone_number

    def set_code(self, code) -> None:
        self.__code = code

    def start_connection(self) -> None:
        self.__client.start(phone=self.__get_phone, code_callback=self.__get_code)

    def get_dialogs_list(self) -> List[str]:
        return [dialog.to_dict for dialog in self.__client.iter_dialogs()]

    def add_event(self, chats_names: Tuple):
        @self.__client.on(events.NewMessage(chats=chats_names))
        async def message_handler(event):
            print(event.message.to_dict())



