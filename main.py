import tkinter as tk

from Blum.UI.MainUI import MainUI
from Blum.BlumBotThread import BlumBotThread
from Blum.DataBridge import DataBridge
from Blum.InputThread import InputThread
from Blum.Output import Output


def main():
    data_bridge = DataBridge()

    output = Output(data_bridge)
    input_thr = InputThread()

    ui = MainUI(data_bridge, input_thr)

    bot_thread = BlumBotThread(data_bridge, output)
    ui.mainloop()

    # plt.imshow(ScreenCapturer().capture_screen(100, 100, 1000, 1010))
    # plt.axis('off')
    # plt.show()


if __name__ == "__main__":
    main()
