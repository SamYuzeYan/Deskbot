import cv2
import pytesseract
import argparse
import numpy as np
from PIL import Image


def detect_text(img):
    pytesseract.pytesseract.tesseract_cmd = r'../bin/tesseract/tesseract.exe'
    text = pytesseract.image_to_string(img, config='--psm 6')
    print(text)
    return text

