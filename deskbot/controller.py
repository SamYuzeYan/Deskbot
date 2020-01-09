import win32gui
import pyautogui as py
import time
from deskbot import constant


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

    # click at x, y position relative to the window
    def click(self, x, y):
        self.center()
        py.moveTo(x + self.coords[0], y + self.coords[1])
        py.click()

    def screen_shot(self, name):
        self.center()
        py.screenshot(name, region=self.coords)

    def __find_coords(self):
        self.hwnd = win32gui.FindWindow(None, self.name)
        if self.hwnd == 0:
            raise Exception("Duel Links is not running!")
        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0] + constant.LEFT_MARGIN
        y = rect[1] + constant.TOP_MARGIN
        w = rect[2] - x - constant.RIGHT_MARGIN
        h = rect[3] - y - constant.BOTTOM_MARGIN
        print("Window %s:" % win32gui.GetWindowText(self.hwnd))
        print("\tLocation: (%d, %d)" % (x, y))
        print("\tSize: (%d, %d)" % (w, h))
        self.coords = x, y, w, h

    def __bring(self):
        win32gui.SetForegroundWindow(self.hwnd)
        # Sleep to guarantee window is in foreground before returning
        time.sleep(0.02)


