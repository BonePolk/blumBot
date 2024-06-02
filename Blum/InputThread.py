import time
from threading import Thread

import win32api
import win32con


class InputThread(Thread):
    def __init__(self):
        super().__init__()
        self.running = False
        self.start()

    def run(self):
        while self.running:
            pass

