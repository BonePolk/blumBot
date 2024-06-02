import numpy as np
from PIL import ImageGrab
from matplotlib import pyplot as plt


class ScreenCapturer:
    @staticmethod
    def capture_screen(x1, y1, x2, y2):
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img_np = np.array(img)

        return img_np

