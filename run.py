#!/usr/bin/python
# -*- coding: utf-8 -*-
from blessed import Terminal
from PIL import Image
import sys
import os
import time
import random
import cv2
import logging
import pygame
import subprocess

sys.tracebacklimit = 0

term = Terminal()

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', ' ']
TIPS = ['Set scrollback limit to 2,000,000 lines to fix stutter problem (on Linux).', 'Turn off all background and/or foreground processes that makes CPU load > 10% for proper frame timing.']

isusingsong = None

audio = "bad-apple-xp-7-audio.wav" # Audio location (leave empty for no audio)
video = "BadApple.mp4" # Video location (don't delete this)
size = 200 # Command line render video size
waitKey = 20 # waitKey (for video and audio synchronization) (Windows only)
frame_interval = 1 / 31 # Frame interval for syncing audio with video (0.0329)

if os.name == 'nt':
    subprocess.Popen(["mode", "con:", "cols=75", "lines=200"])
    time.sleep(0.1)
else:
    print("\x1b[8;75;200t")
    time.sleep(0.1)

os.system(('cls' if os.name == 'nt' else 'clear'))

print(term.home + term.clear)
print(term.center('\033[90m----------------------------------------------\033[37m'))
print(term.center('\033[34mBad Apple!! on CMD using OpenCV and Pygame\033[37m'))
print(term.center('\033[94mBy MinhCrafters\033[37m'))
print(term.center('\033[34mLinux and Windows only.\033[37m'))
print(term.center('\033[90m----------------------------------------------\033[37m\n'))

print(term.center('\033[91mTIP: ' + random.choice(TIPS) + '\033[37m\n'))

try:
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    print(term.center('\033[92mAudio found. Enabling audio...\033[37m'))
    isusingsong = True
    print(term.center('\033[92mAudio enabled. Proceeding to animation...\033[37m'))
except:
    print(term.center('\033[91mAudio not found. Disabling audio...\033[37m'))
    isusingsong = False
    print(term.center('\033[92mAudio disabled. Proceeding to animation...\033[37m'))

if isusingsong == True:
    time.sleep(5)
    os.system(('cls' if os.name == 'nt' else 'clear'))
    pygame.mixer.music.play()
else:
    time.sleep(5)
    os.system(('cls' if os.name == 'nt' else 'clear'))

def resized_gray_image(image, new_width = size):
    (width, height) = image.size
    width = width * 2
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    resized_gray_image = image.resize((new_width, new_height)).convert('L')
    return resized_gray_image


def pix2chars(image):
    pixels = image.getdata()
    characters = ''.join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters


def generate_frame(image, new_width = size):
    new_image_data = pix2chars(resized_gray_image(image))
    total_pixels = len(new_image_data)
    ascii_image = '\n'.join([new_image_data[index:index + new_width] for index in range(0, total_pixels, new_width)])
    sys.stdout.write('\n' * 20 + ascii_image + '\n')

cap = cv2.VideoCapture(video)

try:
    if (os.name == 'nt'):
        os.system('color F0')
        while True:
            (ret, frame) = cap.read()
            start_time = time.time()
            generate_frame(Image.fromarray(frame))
            cv2.waitKey(waitKey)
    else:
        while True:
            (ret, frame) = cap.read()
            time.sleep(0.00021) # General Linux OpenCV waitKey
            start_time = time.time()
            generate_frame(Image.fromarray(frame))
            compute_delay = float(time.time() - start_time)
            delay_duration = frame_interval - compute_delay
            logging.info(str(delay_duration))
            if delay_duration < 0:
                delay_duration = 0
            time.sleep(delay_duration)
except:
    if (os.name == 'nt'):
        os.system('color')
        os.system('cls')
        print(term.center('\n\033[91mSTOPPED\033[37m\n'))
        exit
    else:
        print('\033[49m')
        os.system('clear')
        print(term.center('\n\033[91mSTOPPED\033[37m\n'))
        exit
