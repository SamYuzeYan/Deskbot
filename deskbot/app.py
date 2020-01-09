import time
import win32gui
import pyautogui as py
import cv2
from deskbot import textdetection
from deskbot.common import constant
from PIL import Image

screen_coords = 0, 0, 0, 0


def find_window_coords():
    hwnd = win32gui.FindWindow(None, constant.DUEL_LINKS)
    if hwnd == 0:
        raise Exception("Duel Links is not running!")
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0] + constant.LEFT_MARGIN
    y = rect[1] + constant.TOP_MARGIN
    w = rect[2] - x - constant.RIGHT_MARGIN
    h = rect[3] - y - constant.BOTTOM_MARGIN
    win32gui.SetForegroundWindow(hwnd)
    # Sleep in order to guarantee that window is in foreground
    time.sleep(0.02)
    print("Window %s:" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\tSize: (%d, %d)" % (w, h))
    global screen_coords
    screen_coords = x, y, w, h
    return x, y, w, h


def run():

    coords = find_window_coords()
    take_screen_shot('image_cache/test1.png')
    match('templates/initiate_button.png', 'image_cache/test1.png')
    img = cv2.imread('image_cache/test1.png')
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # img = cv2.bitwise_not(img)
    cv2.imwrite("image_cache/cv2.png", img)
    opened = Image.open("image_cache/cv2.png")
    bw = convert_bw(opened)
    bw.save('image_cache/bw.png')
    text = textdetection.detect_text(bw)
    print(text)


def check_start():
    take_screen_shot("image_cache/initiate.png")
    start = Image.open(r"image_cache/initiate.png")
    initiate = start.crop((constant.INITIATE_LEFT, constant.INITIATE_TOP, constant.INITIATE_RIGHT, constant.INITIATE_BOTTOM))
    bw = convert_bw(initiate)
    text = textdetection.detect_text(bw)
    if "INITIATE" in text:
        click_at(constant.INITIATE_POS[0], constant.INITIATE_POS[1])


# Takes an image and returns a black and white version of it
def convert_bw(img):
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    return bw


# click at x, y position relative to the window
def click_at(x, y):
    py.moveTo(x + screen_coords[0], y + screen_coords[1])
    py.click()


def take_screen_shot(name):
    py.screenshot(name, region=screen_coords)


def match(template_file, image_file):
    img = cv2.imread(image_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    cv2.imwrite("image_cache/before.png", img2)
    template = cv2.imread(template_file)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_gray.shape[::-1]

    method = cv2.TM_SQDIFF_NORMED

    res = cv2.matchTemplate(img_gray, template_gray, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    threshold = 0.1
    if min_val <= threshold:
        print("max val = " + str(max_val))
        print("min val = " + str(min_val))
        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img2, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imwrite("image_cache/after.png", img2)
    else:
        print("Image doesn't have matching template")

# main()
