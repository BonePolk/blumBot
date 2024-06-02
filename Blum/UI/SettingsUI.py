import time
from threading import Thread
import json

import win32api
import win32con

from Blum.DataBridge import DataBridge
from Blum.UI.ResizableOverlay import ResizableOverlay
from Blum.UI.TkSlider import TkFloatSlider
import tkinter as tk


class SettingUI:
    def __init__(self, root: tk.Toplevel, data_bridge: DataBridge, overlay: ResizableOverlay):
        self.data_bridge = data_bridge
        self.overlay = overlay
        self.root = root
        self.root.title("Settings Window")
        self.frequency_slider = TkFloatSlider(self.root, "Frequency:", data_bridge, "frequency",
                                              from_=0, to=100, initial_value=50)
        self.start_btn = tk.Button(self.root, text="Start", command=self.start_btn_callback)
        self.start_btn.pack()
        self.save_cfg_btn = tk.Button(self.root, text="Save config", command=self.save_btn_callback)
        self.save_cfg_btn.pack()
        self.load_cfg_btn = tk.Button(self.root, text="Load config", command=self.load_btn_callback)
        self.load_cfg_btn.pack()

        self.start_hotkey_listener()

    def global_hotkey_listener(self):
        while True:
            s_pressed = win32api.GetAsyncKeyState(0x53) & 0x8000

            if s_pressed:
                self.start_btn_callback()
                time.sleep(0.5)

    def start_hotkey_listener(self):
        listener_thread = Thread(target=self.global_hotkey_listener)
        listener_thread.daemon = True
        listener_thread.start()

    def start_btn_callback(self):
        if self.data_bridge.working:
            self.start_btn.config(text="Start")
        else:
            self.start_btn.config(text="Stop")

        self.data_bridge.working = not self.data_bridge.working

    def save_btn_callback(self):
        config = {
            "rect": self.data_bridge.rect,
            "frequency": self.data_bridge.frequency
        }
        json.dump(config, open("config.json", "w+"), indent=4)

    def update(self):
        self.frequency_slider.on_slider_change(self.data_bridge.frequency)

    def load_btn_callback(self):
        config = json.load(open("config.json"))
        self.data_bridge.rect = config["rect"]
        self.data_bridge.frequency = config["frequency"]
        self.overlay.update_rect()
        self.update()

