from threading import Thread
import tkinter as tk
from Blum.UI.ResizableOverlay import ResizableOverlay
from Blum.UI.SettingsUI import SettingUI
from Blum.DataBridge import DataBridge
from Blum.InputThread import InputThread


class MainUI:
    def __init__(self, data_bridge: DataBridge, input_thr: InputThread):
        self.running = True
        self.data_bridge = data_bridge
        self.input = input_thr

        self.overlay_root = tk.Tk()
        self.overlay = ResizableOverlay(self.overlay_root, data_bridge)

        self.settings_root = tk.Toplevel(self.overlay_root)
        self.settings = SettingUI(self.settings_root, data_bridge, self.overlay)

        self.overlay_root.protocol("WM_DELETE_WINDOW", self.stop)
        self.settings_root.protocol("WM_DELETE_WINDOW", self.stop)

    def mainloop(self):
        self.overlay_root.mainloop()

    def stop(self):
        self.data_bridge.ui_stopped = True
        self.running = False
        self.settings_root.destroy()
        self.overlay_root.destroy()



if __name__ == "__main__":
    app = MainUI()
