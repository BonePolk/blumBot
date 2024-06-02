from random import random
from threading import Thread
import math

import cv2


from Blum.DataBridge import DataBridge
from Blum.ScreenCapturer import ScreenCapturer
from Blum.BlumObjectsDetector import BlumObjectsDetector, HitBox
from Blum.Output import Output


class BlumBotThread(Thread):
    def __init__(self, data_bridge: DataBridge, output: Output):
        super().__init__()
        self.data_bridge = data_bridge
        self.output = output
        self.start()

    def get_safe_rect(self):
        space = 15
        return [
            self.data_bridge.rect[0],
            self.data_bridge.rect[1],
            self.data_bridge.rect[2],
            self.data_bridge.rect[3]
        ]

    def run(self):
        while not self.data_bridge.ui_stopped:
            if self.data_bridge.working:
                img_np = ScreenCapturer.capture_screen(*self.get_safe_rect())
                result_image_with_circles = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                hitboxes = BlumObjectsDetector.detect_green(img_np)

                for hitbox in hitboxes:
                    hit = hitbox
                    center = (hitbox.x, hitbox.y)
                    cv2.circle(result_image_with_circles, center, hitbox.radius, (0, 0, 250), 1)

                cv2.imshow("Detected Green Snowflakes", result_image_with_circles)
                cv2.waitKey(1)

                self.output.handle_clicks(hitboxes)

            else:
                cv2.destroyAllWindows()
