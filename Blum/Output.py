import time
from random import random
import math
from queue import Queue
from threading import Thread
from Blum.BlumObjectsDetector import HitBox
from Blum.DataBridge import DataBridge

import win32api
import win32con


class OutputThread(Thread):
    def __init__(self, hitboxes: list[HitBox], data_bridge: DataBridge):
        super().__init__()
        self.running = True
        self.hitboxes = hitboxes
        self.db = data_bridge
        self.start()

    def stop(self):
        self.running = False

    def run(self):
        for hitbox in self.hitboxes:
            if not self.running:
                break

            if random() > self.db.frequency/100:
                continue

            hitbox.radius -= 5
            safe_space = 15

            cos = random()
            x = (cos * hitbox.radius)*(-1 if random() > 0.5 else 1)
            y = (random()*math.sin(math.acos(cos))*hitbox.radius)*(-1 if random() > 0.5 else 1)

            abs_x = hitbox.x + self.db.rect[0]
            if self.db.rect[2] + safe_space > abs_x + x > self.db.rect[0] - safe_space:
                abs_x += x

            abs_y = hitbox.y + self.db.rect[1]
            if self.db.rect[1] + safe_space > abs_y + y > self.db.rect[3] - safe_space:
                abs_y += y

            win32api.SetCursorPos((int(abs_x), int(abs_y)))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.001)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


class Output:
    def __init__(self, data_bridge: DataBridge):
        self.running = False
        self.prev_thr: OutputThread = None
        self.db = data_bridge

    def kill_prev(self):
        if self.prev_thr:
            self.prev_thr.stop()

    def handle_clicks(self, hitboxes: list[HitBox]):
        self.kill_prev()
        self.prev_thr = OutputThread(hitboxes, self.db)
