import win32gui
import pyautogui as py
import time
import math
from deskbot import constant as cs


class Controller:
    hwnd = None
    coords = 0, 0, 0, 0

    def __init__(self, name):
        self.name = name

    # recenter co-ordinates to the window and brings it forward
    # TODO maybe refactor find and bring into center
    def center(self):
        self.__find_coords()
        self.__bring()

    def click_within(self, top_left, bottom_right):
        total = tuple(map(sum, zip(top_left, bottom_right)))
        middle = tuple(math.floor(ti/2) for ti in total)
        print(middle)
        self.click(middle)

    # click at x, y position relative to the window
    def click(self, pos):
        self.center()
        py.moveTo(pos[0] + self.coords[0], pos[1] + self.coords[1])
        py.click()

    def screen_shot(self, name=cs.CURRENT_FRAME):
        self.center()
        py.screenshot(name, region=self.coords)

    def __find_coords(self):
        self.hwnd = win32gui.FindWindow(None, self.name)
        if self.hwnd == 0:
            raise Exception("Duel Links is not running!")
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0] + cs.LEFT_MARGIN
        y = rect[1] + cs.TOP_MARGIN
        w = rect[2] - x - cs.RIGHT_MARGIN
        h = rect[3] - y - cs.BOTTOM_MARGIN
        print("Window %s:" % win32gui.GetWindowText(self.hwnd))
        print("\tLocation: (%d, %d)" % (x, y))
        print("\tSize: (%d, %d)" % (w, h))
        self.coords = x, y, w, h

    def __bring(self):
        win32gui.SetForegroundWindow(self.hwnd)
        # Sleep to guarantee window is in foreground before returning
        time.sleep(0.02)


