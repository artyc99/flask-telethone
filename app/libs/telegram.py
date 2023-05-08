from queue import Queue
from threading import Thread


class TelethonThread(Thread):
    def __init__(self, commands_queue: Queue):
        Thread.__init__(self)
        self.__commands_queue = commands_queue

    def run(self) -> None:
        while True:
            self.__commands_queue.get()
            self.__commands_queue.task_done()
