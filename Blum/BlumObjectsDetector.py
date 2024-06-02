import cv2
import numpy as np
from matplotlib import pyplot as plt


class HitBox:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


class BlumObjectsDetector:
    @staticmethod
    def detect_colors_contours(img, color1, color2):
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image_hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

        lower_green = np.array(color1)
        upper_green = np.array(color2)

        mask_green = cv2.inRange(image_hsv, lower_green, upper_green)

        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours

    @staticmethod
    def detect_green(img_np) -> list[HitBox]:

        contours = BlumObjectsDetector.detect_colors_contours(img_np,
                                                              [40, 100, 100],
                                                              [70, 255, 255])

        hitboxes = []
        for contour in contours:
            # Get the minimum enclosing circle for each contour
            (x, y), radius = cv2.minEnclosingCircle(contour)

            if radius < 10:
                continue

            hitboxes.append(HitBox(int(x), int(y), int(radius)))

        return hitboxes
