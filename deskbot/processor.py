import cv2
import pytesseract
from deskbot import controller as ctr
from PIL import Image


def convert_bw(img):
    gray = img.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    return bw


def match(template, image):
    img = cv2.imread(image)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    cv2.imwrite("image_cache/before.png", img2)
    temp = cv2.imread(template)
    temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
    w, h = temp_gray.shape[::-1]

    method = cv2.TM_SQDIFF_NORMED

    res = cv2.matchTemplate(img_gray, temp_gray, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    threshold = 0.1
    if min_val <= threshold:
        print("max val = " + str(max_val))
        print("min val = " + str(min_val))
        top_left = min_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img2, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imwrite("image_cache/after.png", img2)
        return True
    else:
        print("Image doesn't have matching template")
        return False


def detect_text(img):
    pytesseract.pytesseract.tesseract_cmd = r'../bin/tesseract/tesseract.exe'
    text = pytesseract.image_to_string(img, config='--psm 6')
    print(text)
    return text

# def check_start():
#     take_screen_shot("image_cache/initiate.png")
#     start = Image.open(r"image_cache/initiate.png")
#     initiate = start.crop((constant.INITIATE_LEFT, constant.INITIATE_TOP, constant.INITIATE_RIGHT, constant.INITIATE_BOTTOM))
#     bw = convert_bw(initiate)
#     text = detect_text(bw)
#     if "INITIATE" in text:
#         click_at(constant.INITIATE_POS[0], constant.INITIATE_POS[1])


class Processor:

    def __init__(self, controller: ctr.Controller):
        self.ctr = controller

    def parse_text(self):
        self.ctr.screen_shot('image_cache/current.png')
        img = cv2.imread('image_cache/current.png')
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # img = cv2.bitwise_not(img)
        cv2.imwrite("image_cache/cv2.png", img)
        opened = Image.open("image_cache/cv2.png")
        bw = convert_bw(opened)
        bw.save('image_cache/bw.png')
        text = detect_text(bw)
        print(text)
        return text
